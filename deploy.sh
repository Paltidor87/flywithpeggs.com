#!/usr/bin/env bash
# =============================================================================
# Deploy flywithpeggs.com to Hetzner Cloud
# =============================================================================
# Usage: ./deploy.sh [SERVER_IP_OR_HOSTNAME]
#
# Examples:
#   ./deploy.sh 49.12.345.67
#   ./deploy.sh flywithpeggs.com
# =============================================================================

set -euo pipefail

# ---- Configuration ----
REMOTE_USER="deploy"
REMOTE_DIR="/home/deploy/flywithpeggs.com"
SERVER="${1:?Usage: ./deploy.sh SERVER_IP_OR_HOSTNAME}"

echo "==> Deploying flywithpeggs.com to ${SERVER}..."

# ---- Sync files to server ----
echo "==> Syncing files..."
rsync -avz --delete \
  --exclude '.git' \
  --exclude '.gitignore' \
  --exclude '.DS_Store' \
  --exclude 'node_modules' \
  --exclude '*.docx' \
  --exclude '*.pdf' \
  --exclude 'hetzner-setup.sh' \
  --exclude 'deploy.sh' \
  --exclude 'README.md' \
  ./ "${REMOTE_USER}@${SERVER}:${REMOTE_DIR}/"

# ---- Build and restart on the server ----
echo "==> Building and starting containers..."
ssh "${REMOTE_USER}@${SERVER}" "cd ${REMOTE_DIR} && docker compose up -d --build --remove-orphans"

echo ""
echo "============================================="
echo "  Deployment complete!"
echo "============================================="
echo ""
echo "  Your site should be live at:"
echo "    https://www.flywithpeggs.com"
echo ""
echo "  To check logs:  ssh ${REMOTE_USER}@${SERVER} 'cd ${REMOTE_DIR} && docker compose logs -f'"
echo "  To stop:        ssh ${REMOTE_USER}@${SERVER} 'cd ${REMOTE_DIR} && docker compose down'"
echo ""
