#!/usr/bin/env bash
# =============================================================================
# Hetzner Cloud Server Setup Script for flywithpeggs.com
# =============================================================================
# This script is meant to be run ON the Hetzner server after initial SSH login.
# It installs Docker, Docker Compose, sets up a firewall, and prepares the
# server for deployment.
#
# Usage:
#   1. SSH into your new Hetzner server: ssh root@YOUR_SERVER_IP
#   2. Upload and run this script:
#      scp hetzner-setup.sh root@YOUR_SERVER_IP:~/
#      ssh root@YOUR_SERVER_IP 'bash ~/hetzner-setup.sh'
# =============================================================================

set -euo pipefail

echo "==> Updating system packages..."
apt-get update && apt-get upgrade -y

echo "==> Installing essential packages..."
apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  ufw \
  fail2ban \
  unattended-upgrades

# ---- Docker Installation ----
echo "==> Installing Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "==> Starting Docker..."
systemctl enable docker
systemctl start docker

# ---- Firewall Setup ----
echo "==> Configuring firewall (UFW)..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 443/udp   # HTTP/3 (QUIC)
ufw --force enable

# ---- Fail2Ban ----
echo "==> Configuring Fail2Ban..."
systemctl enable fail2ban
systemctl start fail2ban

# ---- Create deploy user ----
echo "==> Creating deploy user..."
if ! id "deploy" &>/dev/null; then
  useradd -m -s /bin/bash -G docker deploy
  mkdir -p /home/deploy/.ssh
  cp /root/.ssh/authorized_keys /home/deploy/.ssh/authorized_keys
  chown -R deploy:deploy /home/deploy/.ssh
  chmod 700 /home/deploy/.ssh
  chmod 600 /home/deploy/.ssh/authorized_keys
  echo "deploy ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/deploy
  echo "    Created 'deploy' user with Docker access and your SSH key."
else
  echo "    'deploy' user already exists, skipping."
fi

# ---- Create app directory ----
echo "==> Creating app directory..."
mkdir -p /home/deploy/flywithpeggs.com
chown deploy:deploy /home/deploy/flywithpeggs.com

echo ""
echo "============================================="
echo "  Server setup complete!"
echo "============================================="
echo ""
echo "Next steps:"
echo "  1. Point your DNS (flywithpeggs.com AND www.flywithpeggs.com)"
echo "     to this server's IP address."
echo "  2. Deploy your site by running: ./deploy.sh YOUR_SERVER_IP"
echo ""
