#!/bin/bash
# =============================================================================
# Hostinger VPS Initial Setup
# Run this ONCE on the VPS to prepare it for deployments.
# Usage: ssh root@YOUR_VPS_IP 'bash -s' < hostinger-setup.sh
# =============================================================================

set -euo pipefail

echo "=== Hostinger VPS Setup ==="

# --- 1. Create deploy user ---
if id "deploy" &>/dev/null; then
    echo "[OK] User 'deploy' already exists"
else
    echo "[+] Creating 'deploy' user..."
    adduser --disabled-password --gecos "" deploy
    usermod -aG docker deploy
    echo "[OK] User 'deploy' created and added to docker group"
fi

# --- 2. Set up SSH key for deploy user ---
echo "[+] Setting up SSH keys for deploy user..."
mkdir -p /home/deploy/.ssh
chmod 700 /home/deploy/.ssh

if [ ! -f /home/deploy/.ssh/authorized_keys ]; then
    touch /home/deploy/.ssh/authorized_keys
fi
chmod 600 /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /home/deploy/.ssh

echo ""
echo ">>> IMPORTANT: Add your SSH public key to /home/deploy/.ssh/authorized_keys"
echo ">>> Run: echo 'YOUR_PUBLIC_KEY' >> /home/deploy/.ssh/authorized_keys"
echo ""

# --- 3. Install Docker (if not present) ---
if command -v docker &>/dev/null; then
    echo "[OK] Docker already installed: $(docker --version)"
else
    echo "[+] Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo "[OK] Docker installed"
fi

# --- 4. Install Docker Compose plugin (if not present) ---
if docker compose version &>/dev/null; then
    echo "[OK] Docker Compose already installed: $(docker compose version)"
else
    echo "[+] Installing Docker Compose plugin..."
    apt-get update && apt-get install -y docker-compose-plugin
    echo "[OK] Docker Compose installed"
fi

# --- 5. Create shared Docker network ---
if docker network inspect web &>/dev/null; then
    echo "[OK] Docker network 'web' already exists"
else
    echo "[+] Creating shared Docker network 'web'..."
    docker network create web
    echo "[OK] Network 'web' created"
fi

# --- 6. Create project directories ---
echo "[+] Creating project directories..."
mkdir -p /home/deploy/flywithpeggs.com
mkdir -p /home/deploy/clawdbot
chown -R deploy:deploy /home/deploy/flywithpeggs.com
chown -R deploy:deploy /home/deploy/clawdbot
echo "[OK] Directories created"

# --- 7. Install rsync (needed for GitHub Actions deploy) ---
if command -v rsync &>/dev/null; then
    echo "[OK] rsync already installed"
else
    echo "[+] Installing rsync..."
    apt-get update && apt-get install -y rsync
    echo "[OK] rsync installed"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Add your SSH public key to /home/deploy/.ssh/authorized_keys"
echo "  2. Set GitHub Secrets on BOTH repos (flywithpeggs.com & clawdbot):"
echo "     - SSH_PRIVATE_KEY  (the private key matching the public key above)"
echo "     - SERVER_IP        (this server's IP address)"
echo "  3. For the clawdbot repo, also add these secrets:"
echo "     - TELEGRAM_BOT_TOKEN"
echo "     - TELEGRAM_ALLOWED_CHATS (optional, comma-separated chat IDs)"
echo "     - ESSENCEM_URL (e.g. http://100.114.113.70:11445 if using Tailscale)"
echo "     - OLLAMA_MODEL (default: llama3.2:3b)"
echo "  4. Set DNS A records pointing to this server:"
echo "     - flywithpeggs.com      → $(curl -s ifconfig.me || echo 'YOUR_IP')"
echo "     - www.flywithpeggs.com  → $(curl -s ifconfig.me || echo 'YOUR_IP')"
echo "     - clawd.flywithpeggs.com → $(curl -s ifconfig.me || echo 'YOUR_IP')"
echo "  5. Push to main on both repos to trigger deployment!"
echo ""
