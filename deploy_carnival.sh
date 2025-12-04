#!/bin/bash

# Misfits Carnival Manager Deployment Script
# This script automates deployment to your EC2 server

set -e  # Exit on any error

# Configuration
SERVER_IP="13.201.15.180"
SSH_KEY="/Users/retalplaza/Downloads/cdk-key-staging.pem"
SERVER_USER="ec2-user"
LOCAL_FILE="/Users/retalplaza/Downloads/Misfits_Carnival_Manager.html"
WEB_DIR="/var/www/carnival"
BACKUP_DIR="/var/backups/carnival"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if local file exists
check_local_file() {
    if [[ ! -f "$LOCAL_FILE" ]]; then
        log_error "Local file not found: $LOCAL_FILE"
        exit 1
    fi
    log_info "Local file found: $LOCAL_FILE"
}

# Check SSH connection
check_ssh_connection() {
    log_info "Testing SSH connection to $SERVER_IP..."
    if ssh -i "$SSH_KEY" -o ConnectTimeout=10 -o BatchMode=yes "$SERVER_USER@$SERVER_IP" exit 2>/dev/null; then
        log_success "SSH connection successful"
    else
        log_error "SSH connection failed. Check your key and server."
        exit 1
    fi
}

# Create backup of current version
create_backup() {
    log_info "Creating backup of current version..."
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "
        sudo mkdir -p $BACKUP_DIR
        if [[ -f $WEB_DIR/index.html ]]; then
            sudo cp $WEB_DIR/index.html $BACKUP_DIR/index_backup_\$(date +%Y%m%d_%H%M%S).html
            echo 'Backup created successfully'
        else
            echo 'No existing file to backup'
        fi
    "
}

# Deploy new version
deploy_file() {
    log_info "Deploying new version..."

    # Copy file to temporary location
    scp -i "$SSH_KEY" "$LOCAL_FILE" "$SERVER_USER@$SERVER_IP:/tmp/new_carnival.html"

    # Move to web directory and set permissions
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "
        sudo mv /tmp/new_carnival.html $WEB_DIR/index.html
        sudo chown nginx:nginx $WEB_DIR/index.html
        sudo chmod 644 $WEB_DIR/index.html
    "

    log_success "File deployed successfully"
}

# Test nginx configuration
test_nginx() {
    log_info "Testing nginx configuration..."
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "sudo nginx -t" || {
        log_error "Nginx configuration test failed"
        exit 1
    }
    log_success "Nginx configuration is valid"
}

# Reload nginx
reload_nginx() {
    log_info "Reloading nginx..."
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "sudo systemctl reload nginx"
    log_success "Nginx reloaded successfully"
}

# Test website
test_website() {
    log_info "Testing website accessibility..."
    if curl -s -o /dev/null -w "%{http_code}" "http://$SERVER_IP" | grep -q "200"; then
        log_success "Website is accessible"
    else
        log_warning "Website test failed - check manually"
    fi
}

# Rollback function
rollback() {
    log_warning "Rolling back to previous version..."
    ssh -i "$SSH_KEY" "$SERVER_USER@$SERVER_IP" "
        LATEST_BACKUP=\$(sudo ls -t $BACKUP_DIR/index_backup_*.html 2>/dev/null | head -1)
        if [[ -n \"\$LATEST_BACKUP\" ]]; then
            sudo cp \"\$LATEST_BACKUP\" $WEB_DIR/index.html
            sudo chown nginx:nginx $WEB_DIR/index.html
            sudo systemctl reload nginx
            echo 'Rollback completed'
        else
            echo 'No backup found for rollback'
        fi
    "
}

# Main deployment process
main() {
    log_info "Starting Misfits Carnival Manager deployment..."
    echo "====================================================="

    # Pre-flight checks
    check_local_file
    check_ssh_connection

    # Deployment process
    create_backup
    deploy_file
    test_nginx
    reload_nginx
    test_website

    echo "====================================================="
    log_success "Deployment completed successfully!"
    echo ""
    log_info "Your app is now live at: http://carnival.misfits.net.in"
    log_info "You can also access via IP: http://$SERVER_IP"
    echo ""
    log_info "To rollback if needed, run: $0 --rollback"
}

# Handle command line arguments
case "${1:-}" in
    --rollback)
        log_info "Starting rollback process..."
        rollback
        log_success "Rollback completed"
        ;;
    --help)
        echo "Misfits Carnival Manager Deployment Script"
        echo ""
        echo "Usage:"
        echo "  $0           Deploy latest version"
        echo "  $0 --rollback  Rollback to previous version"
        echo "  $0 --help     Show this help"
        echo ""
        echo "Configuration:"
        echo "  Server IP: $SERVER_IP"
        echo "  SSH Key: $SSH_KEY"
        echo "  Local File: $LOCAL_FILE"
        ;;
    "")
        main
        ;;
    *)
        log_error "Unknown option: $1"
        echo "Use '$0 --help' for usage information"
        exit 1
        ;;
esac