#!/bin/bash

# Misfits Carnival Manager - Production Deployment Script
# Server: 13.201.15.180
# Key: cdk-key-staging.pem

echo "🎪 Deploying Misfits Carnival Manager to Production"
echo "=================================================="

# Configuration
SERVER_IP="13.201.15.180"
KEY_FILE="~/Downloads/cdk-key-staging.pem"
SERVER_USER="ec2-user"
LOCAL_FILE="Misfits_Carnival_Manager_WORKING_FIXED.html"
REMOTE_PATH="/var/www/html/index.html"
BACKUP_PATH="/var/www/html/backup"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check if key file exists
if [ ! -f ~/Downloads/cdk-key-staging.pem ]; then
    echo -e "${RED}Error: Key file not found at ~/Downloads/cdk-key-staging.pem${NC}"
    exit 1
fi

# Check if source file exists
if [ ! -f "$LOCAL_FILE" ]; then
    echo -e "${RED}Error: Source file $LOCAL_FILE not found${NC}"
    echo "Make sure you're running this script from the Downloads directory"
    exit 1
fi

# Set key file permissions
chmod 600 ~/Downloads/cdk-key-staging.pem
echo -e "${GREEN}✓ Key file permissions set${NC}"

echo -e "${YELLOW}Step 2: Testing connection to server...${NC}"

# Test SSH connection
ssh -i ~/Downloads/cdk-key-staging.pem -o ConnectTimeout=10 $SERVER_USER@$SERVER_IP "echo 'Connection successful'" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${RED}Error: Cannot connect to server. Please check:${NC}"
    echo "  - Server IP: $SERVER_IP"
    echo "  - Key file: $KEY_FILE"
    echo "  - Network connectivity"
    exit 1
fi

echo -e "${YELLOW}Step 3: Preparing server environment...${NC}"

# Create backup directory and backup existing files
ssh -i ~/Downloads/cdk-key-staging.pem $SERVER_USER@$SERVER_IP << 'EOF'
    # Create backup directory
    sudo mkdir -p /var/www/html/backup

    # Backup existing index.html if it exists
    if [ -f /var/www/html/index.html ]; then
        sudo cp /var/www/html/index.html /var/www/html/backup/index_backup_$(date +%Y%m%d_%H%M%S).html
        echo "✓ Existing file backed up"
    fi

    # Ensure www-data owns the directory
    sudo chown -R www-data:www-data /var/www/html

    # Check if web server is running
    if systemctl is-active --quiet apache2; then
        echo "✓ Apache2 is running"
    elif systemctl is-active --quiet nginx; then
        echo "✓ Nginx is running"
    else
        echo "Warning: No web server detected"
    fi
EOF

echo -e "${GREEN}✓ Server environment prepared${NC}"

echo -e "${YELLOW}Step 4: Deploying application...${NC}"

# Upload the file
scp -i ~/Downloads/cdk-key-staging.pem "$LOCAL_FILE" $SERVER_USER@$SERVER_IP:/tmp/carnival_manager.html

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ File uploaded successfully${NC}"
else
    echo -e "${RED}Error: Failed to upload file${NC}"
    exit 1
fi

# Move file to final location and set permissions
ssh -i ~/Downloads/cdk-key-staging.pem $SERVER_USER@$SERVER_IP << 'EOF'
    # Move file to web directory
    sudo mv /tmp/carnival_manager.html /var/www/html/index.html

    # Set proper ownership and permissions
    sudo chown www-data:www-data /var/www/html/index.html
    sudo chmod 644 /var/www/html/index.html

    # Create a symbolic link for easier access
    sudo ln -sf /var/www/html/index.html /var/www/html/carnival-manager.html

    echo "✓ Application deployed to /var/www/html/index.html"
EOF

echo -e "${GREEN}✓ Application deployed successfully${NC}"

echo -e "${YELLOW}Step 5: Configuring web server...${NC}"

# Configure web server for optimal performance
ssh -i ~/Downloads/cdk-key-staging.pem $SERVER_USER@$SERVER_IP << 'EOF'
    # Check if we need to configure Apache or Nginx
    if systemctl is-active --quiet apache2; then
        # Configure Apache
        sudo tee /etc/apache2/sites-available/carnival-manager.conf > /dev/null << 'APACHE_EOF'
<VirtualHost *:80>
    ServerName carnival.misfits.net.in
    DocumentRoot /var/www/html

    # Enable compression
    LoadModule deflate_module modules/mod_deflate.so
    <Location />
        SetOutputFilter DEFLATE
        SetEnvIfNoCase Request_URI \
            \.(?:gif|jpe?g|png)$ no-gzip dont-vary
        SetEnvIfNoCase Request_URI \
            \.(?:exe|t?gz|zip|bz2|sit|rar)$ no-gzip dont-vary
    </Location>

    # Set cache headers
    <FilesMatch "\.(html|css|js)$">
        ExpiresActive On
        ExpiresDefault "access plus 1 hour"
    </FilesMatch>

    ErrorLog ${APACHE_LOG_DIR}/carnival_error.log
    CustomLog ${APACHE_LOG_DIR}/carnival_access.log combined
</VirtualHost>
APACHE_EOF

        # Enable the site
        sudo a2ensite carnival-manager
        sudo a2enmod expires
        sudo a2enmod deflate
        sudo systemctl reload apache2
        echo "✓ Apache configured"

    elif systemctl is-active --quiet nginx; then
        # Configure Nginx
        sudo tee /etc/nginx/sites-available/carnival-manager > /dev/null << 'NGINX_EOF'
server {
    listen 80;
    server_name carnival.misfits.net.in;
    root /var/www/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_types text/html text/css application/javascript application/json;

    # Cache headers
    location ~* \.(html|css|js)$ {
        expires 1h;
        add_header Cache-Control "public, must-revalidate";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;

    access_log /var/log/nginx/carnival_access.log;
    error_log /var/log/nginx/carnival_error.log;
}
NGINX_EOF

        # Enable the site
        sudo ln -sf /etc/nginx/sites-available/carnival-manager /etc/nginx/sites-enabled/
        sudo nginx -t && sudo systemctl reload nginx
        echo "✓ Nginx configured"
    fi
EOF

echo -e "${GREEN}✓ Web server configured${NC}"

echo -e "${YELLOW}Step 6: Testing deployment...${NC}"

# Test the deployment
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://$SERVER_IP)
if [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓ Application is accessible via HTTP${NC}"
    echo -e "${GREEN}✓ URL: http://$SERVER_IP${NC}"
else
    echo -e "${YELLOW}Warning: HTTP test returned status $RESPONSE${NC}"
fi

# Get server info
echo -e "${YELLOW}Step 7: Deployment summary...${NC}"

ssh -i ~/Downloads/cdk-key-staging.pem $SERVER_USER@$SERVER_IP << 'EOF'
    echo "================== DEPLOYMENT SUMMARY =================="
    echo "Server IP: $(curl -s ifconfig.me || hostname -I | awk '{print $1}')"
    echo "Deployment time: $(date)"
    echo "File location: /var/www/html/index.html"
    echo "File size: $(ls -lh /var/www/html/index.html | awk '{print $5}')"
    echo "Permissions: $(ls -l /var/www/html/index.html | awk '{print $1, $3, $4}')"

    if systemctl is-active --quiet apache2; then
        echo "Web server: Apache2 ($(systemctl is-active apache2))"
    elif systemctl is-active --quiet nginx; then
        echo "Web server: Nginx ($(systemctl is-active nginx))"
    fi

    echo "========================================================="
EOF

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL! 🎉${NC}"
echo ""
echo -e "${YELLOW}Access your application at:${NC}"
echo "  🌐 http://$SERVER_IP"
echo "  🌐 http://carnival.misfits.net.in (if DNS configured)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Configure DNS to point carnival.misfits.net.in to $SERVER_IP"
echo "  2. Set up SSL certificate for HTTPS"
echo "  3. Test all functionality with your team"
echo "  4. Monitor logs for any issues"
echo ""
echo -e "${YELLOW}Log locations:${NC}"
echo "  📁 Apache: /var/log/apache2/carnival_*.log"
echo "  📁 Nginx: /var/log/nginx/carnival_*.log"
echo ""
echo -e "${GREEN}Deployment completed successfully! ✨${NC}"
EOF

# Make the script executable
chmod +x /Users/retalplaza/Downloads/deploy_to_production.sh