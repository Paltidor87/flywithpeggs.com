from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import datetime
import threading
import json
import re
import shutil
import urllib.parse
import urllib.request
import base64

app = Flask(__name__)
CORS(app)

def load_env_file(path: str) -> None:
    if not os.path.exists(path):
        return
    try:
        with open(path, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    continue
                if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                # Do not override already-exported env vars.
                if key not in os.environ:
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: failed to load env file {path}: {e}")

# Load local environment files (if present) before reading config values.
load_env_file(".env")
load_env_file(".env.local")

DESKTOP_PATH = "/Users/peggs/Desktop/ALTIDOR_LEADS"
if not os.path.exists(DESKTOP_PATH):
    os.makedirs(DESKTOP_PATH)

NOISE_PATTERNS = [
    r"^Starting chat with index .*$",
    r"^Using .*$",
    r"^The query took .*$",
    r"^\[read_HNSW.*$",
    r"^INFO: Skipping external storage loading.*$",
    r"^ZmqDistanceComputer initialized:.*$",
]

HOT_PATTERNS = [
    r"\burgent\b",
    r"\basap\b",
    r"\bimmediately\b",
    r"\bright now\b",
    r"\bbook\b",
    r"\bready\b",
    r"\bcall me\b",
    r"\bpayment\b",
]

REVIEW_PATTERNS = [
    r"\bconcern\b",
    r"\bconfused\b",
    r"\bnot sure\b",
    r"\bmaybe\b",
    r"\bquestion\b",
    r"\bthinking\b",
    r"\bconsidering\b",
]

ENABLE_DESKTOP_ALERT = os.getenv("ENABLE_DESKTOP_ALERT", "true").lower() == "true"
ENABLE_TWILIO_SMS = os.getenv("ENABLE_TWILIO_SMS", "false").lower() == "true"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
TWILIO_TO_NUMBER = os.getenv("TWILIO_TO_NUMBER", "")
NOTIFY_MIN_PRIORITY = os.getenv("NOTIFY_MIN_PRIORITY", "hot").lower()
NOTIFY_TIME_WINDOW = os.getenv("NOTIFY_TIME_WINDOW", "").strip()  # e.g. "08:00-20:00"
NOTIFY_MODE = os.getenv("NOTIFY_MODE", "priority").lower()  # priority | time | priority_or_time | priority_and_time | always


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", (value or "").strip())
    cleaned = cleaned.strip("_")
    return cleaned[:60] or "lead"


def clean_audit_output(stdout_text: str) -> str:
    if not stdout_text:
        return "No audit output returned."

    text = stdout_text.strip()
    if "LEANN:" in text:
        text = text.split("LEANN:", 1)[1].strip()

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append("")
            continue
        if any(re.match(pattern, stripped) for pattern in NOISE_PATTERNS):
            continue
        lines.append(line.rstrip())

    cleaned = "\n".join(lines).strip()
    return cleaned or "No clean audit content available."


def build_lead_folder(base_path: str, client_name: str, timestamp: str) -> str:
    day_folder = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_name = slugify(client_name)
    folder_name = f"{timestamp}_{safe_name}"
    lead_folder = os.path.join(base_path, day_folder, folder_name)
    os.makedirs(lead_folder, exist_ok=True)
    return lead_folder


def classify_priority(narrative: str) -> str:
    text = (narrative or "").lower()
    if any(re.search(pattern, text) for pattern in HOT_PATTERNS):
        return "hot"
    if any(re.search(pattern, text) for pattern in REVIEW_PATTERNS):
        return "review"
    return "low"

def parse_minutes(hhmm: str) -> int:
    parts = hhmm.split(":")
    if len(parts) != 2:
        raise ValueError("Invalid time format")
    hour = int(parts[0])
    minute = int(parts[1])
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError("Invalid time range")
    return hour * 60 + minute

def is_in_time_window(now_dt: datetime.datetime, window: str) -> bool:
    if not window:
        return True
    try:
        start_str, end_str = [x.strip() for x in window.split("-", 1)]
        start_min = parse_minutes(start_str)
        end_min = parse_minutes(end_str)
    except Exception:
        # Fail-open so malformed config doesn't silently suppress all alerts.
        print(f"Invalid NOTIFY_TIME_WINDOW '{window}', allowing notifications.")
        return True
    now_min = now_dt.hour * 60 + now_dt.minute
    if start_min <= end_min:
        return start_min <= now_min <= end_min
    # Overnight windows, e.g., 22:00-06:00
    return now_min >= start_min or now_min <= end_min

def should_send_notifications(priority: str, now_dt: datetime.datetime) -> bool:
    rank = {"low": 1, "review": 2, "hot": 3}
    min_rank = rank.get(NOTIFY_MIN_PRIORITY, 3)
    priority_ok = rank.get(priority, 1) >= min_rank
    time_ok = is_in_time_window(now_dt, NOTIFY_TIME_WINDOW)

    if NOTIFY_MODE == "always":
        return True
    if NOTIFY_MODE == "time":
        return time_ok
    if NOTIFY_MODE == "priority_or_time":
        return priority_ok or time_ok
    if NOTIFY_MODE == "priority_and_time":
        return priority_ok and time_ok
    # default: "priority"
    return priority_ok

def send_desktop_alert(title: str, message: str) -> None:
    if not ENABLE_DESKTOP_ALERT:
        return
    if os.uname().sysname != "Darwin":
        return
    if not shutil.which("osascript"):
        return
    try:
        safe_message = message.replace('"', "'")
        safe_title = title.replace('"', "'")
        script = f'display notification "{safe_message}" with title "{safe_title}"'
        subprocess.run(["osascript", "-e", script], check=False)
    except Exception as e:
        print(f"Desktop alert failed: {e}")

def send_twilio_sms(message: str) -> None:
    if not ENABLE_TWILIO_SMS:
        return
    missing = [
        not TWILIO_ACCOUNT_SID,
        not TWILIO_AUTH_TOKEN,
        not TWILIO_FROM_NUMBER,
        not TWILIO_TO_NUMBER,
    ]
    if any(missing):
        print("Twilio SMS skipped: missing required env vars.")
        return
    try:
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
        payload = urllib.parse.urlencode({
            "From": TWILIO_FROM_NUMBER,
            "To": TWILIO_TO_NUMBER,
            "Body": message,
        }).encode("utf-8")
        request = urllib.request.Request(url, data=payload, method="POST")
        auth = base64.b64encode(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode("utf-8")).decode("ascii")
        request.add_header("Authorization", f"Basic {auth}")
        request.add_header("Content-Type", "application/x-www-form-urlencoded")
        with urllib.request.urlopen(request, timeout=20) as response:
            if response.status >= 300:
                print(f"Twilio SMS failed: HTTP {response.status}")
    except Exception as e:
        print(f"Twilio SMS failed: {e}")


def process_audit_in_background(data):
    name = data.get('name') or 'Visionary'
    narrative = data.get('message') or data.get('significance') or 'No content.'
    category = data.get('category') or data.get('inquiry_type') or data.get('goal') or 'General Inquiry'
    status = data.get('status') or 'new'
    source = data.get('source') or 'unknown'
    priority = classify_priority(narrative)
    print(f"🧠 J'Son is auditing {name} in the background...")

    prompt = (
        "SYSTEM: You are J'Son reviewing an inbound lead for Altidor Wellness travel services. "
        "Respond in clear, concise business language. Focus on intent, urgency, tone, and next action. "
        "Do not discuss technical infrastructure unless explicitly requested. "
        "Format response as:\n"
        "1) Lead Intent\n2) Risk/Concern Flags\n3) Suggested Reply (2-4 lines)\n4) Next Best Action\n"
        f"INQUIRY: {narrative}"
    )
    cmd = ["leann", "ask", "altidor-audit", prompt, "--model", "travel-pro:latest", "--top-k", "1"]

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    lead_folder = build_lead_folder(DESKTOP_PATH, name, timestamp)

    raw_stdout = ""
    raw_stderr = ""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        raw_stdout = result.stdout or ""
        raw_stderr = result.stderr or ""
        audit_text = clean_audit_output(raw_stdout)
    except Exception as e:
        raw_stderr = str(e)
        audit_text = f"Audit failed: {str(e)}"

    files = {
        "lead.json": {
            "client": name,
            "category": category,
            "status": status,
            "source": source,
            "priority": priority,
            "narrative": narrative,
            "submitted_at": datetime.datetime.now().isoformat(),
            "payload": data,
        },
        "narrative.txt": narrative,
        "audit.txt": audit_text,
        "audit_raw.log": f"STDOUT:\n{raw_stdout}\n\nSTDERR:\n{raw_stderr}\n",
    }

    for filename, content in files.items():
        full_path = os.path.join(lead_folder, filename)
        with open(full_path, "w") as f:
            if filename.endswith(".json"):
                json.dump(content, f, indent=2)
                f.write("\n")
            else:
                f.write(content)

    manifest_row = {
        "client": name,
        "category": category,
        "status": status,
        "source": source,
        "priority": priority,
        "timestamp": timestamp,
        "folder": lead_folder,
        "narrative_preview": narrative[:180],
    }

    print(f"✅ Lead package created: {lead_folder}")
    notify_line = f"New lead: {name} [{priority}]"
    now_dt = datetime.datetime.now()
    notify_enabled = should_send_notifications(priority, now_dt)
    manifest_row["notification_sent"] = notify_enabled
    manifest_row["notify_mode"] = NOTIFY_MODE
    manifest_row["notify_window"] = NOTIFY_TIME_WINDOW
    if notify_enabled:
        send_desktop_alert("ALTIDOR LEAD", notify_line)
        send_twilio_sms(f"{notify_line}\nNarrative: {narrative[:240]}")
    else:
        print(
            f"Notification suppressed for {name} "
            f"(priority={priority}, mode={NOTIFY_MODE}, window='{NOTIFY_TIME_WINDOW}')."
        )
    manifest_path = os.path.join(DESKTOP_PATH, "manifest.jsonl")
    with open(manifest_path, "a") as f:
        f.write(json.dumps(manifest_row) + "\n")

@app.route('/new-lead', methods=['POST'])
def handle_lead():
    data = request.json
    threading.Thread(target=process_audit_in_background, args=(data,)).start()
    return jsonify({"status": "Success", "message": "J'Son is on it."}), 200

if __name__ == '__main__':
    app.run(port=5001)
