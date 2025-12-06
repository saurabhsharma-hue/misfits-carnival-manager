#!/bin/bash

# Super quick deployment for development iterations
# Uses rsync for incremental updates and persistent connections

echo "⚡ Super quick deploying..."

# Configuration
SERVER="ec2-user@13.201.15.180"
KEY="/Users/retalplaza/Downloads/cdk-key-staging.pem"
LOCAL="/Users/retalplaza/Downloads/Misfits_Carnival_Manager.html"

# Use rsync for faster incremental transfer and single command
rsync -avz --progress -e "ssh -i $KEY -o ControlMaster=auto -o ControlPath=/tmp/ssh_mux_%h_%p_%r" \
  "$LOCAL" "$SERVER:/tmp/carnival_update.html" && \
ssh -i "$KEY" -o ControlMaster=auto -o ControlPath=/tmp/ssh_mux_%h_%p_%r "$SERVER" \
  "sudo mv /tmp/carnival_update.html /var/www/carnival/index.html && sudo chown nginx:nginx /var/www/carnival/index.html" && \
echo "⚡ Done! http://carnival.misfits.net.in"