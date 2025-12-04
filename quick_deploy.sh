#!/bin/bash

# Quick deployment script for Misfits Carnival Manager
# Use this for rapid development iterations

echo "🚀 Quick deploying Misfits Carnival Manager..."

# Configuration
SERVER_IP="13.201.15.180"
SSH_KEY="/Users/retalplaza/Downloads/cdk-key-staging.pem"
LOCAL_FILE="/Users/retalplaza/Downloads/Misfits_Carnival_Manager.html"

# Optimized quick deploy - combine operations to reduce SSH connections
scp -C -o Compression=yes -i "$SSH_KEY" "$LOCAL_FILE" ec2-user@$SERVER_IP:/tmp/carnival_update.html && \
ssh -o ControlMaster=auto -o ControlPath=/tmp/ssh_mux_%h_%p_%r -i "$SSH_KEY" ec2-user@$SERVER_IP "
    sudo mv /tmp/carnival_update.html /var/www/carnival/index.html && \
    sudo chown nginx:nginx /var/www/carnival/index.html && \
    sudo systemctl reload nginx
" && echo "✅ Deployment complete! 🌐 Visit: http://carnival.misfits.net.in"