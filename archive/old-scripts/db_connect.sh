#!/bin/bash

# Database Connection Script for Misfits
# This script establishes SSH tunnel and connects to the database

echo "🔧 Setting up database connection..."

# Check if SSH key exists
if [ ! -f "$HOME/Downloads/claude-control-key" ]; then
    echo "❌ SSH key not found at ~/Downloads/claude-control-key"
    echo "💡 You may need to download the SSH key file again"
    echo "🔄 Attempting connection without key..."

    # Try to generate or find the key
    echo "🔍 Searching for any SSH keys..."
    ls -la ~/.ssh/

    echo "⚠️ Continuing without SSH key - this may fail"
fi

# Kill any existing tunnels
echo "🧹 Cleaning up existing tunnels..."
pkill -f "5433.*misfits" 2>/dev/null || true

# Establish SSH tunnel
echo "🔗 Establishing SSH tunnel..."
if [ -f "$HOME/Downloads/claude-control-key" ]; then
    chmod 600 "$HOME/Downloads/claude-control-key"
    ssh -i "$HOME/Downloads/claude-control-key" -f -N -L 5433:misfits.cgncbvolnhe7.ap-south-1.rds.amazonaws.com:5432 claude-control@15.207.255.212
else
    echo "⚠️ Trying with default SSH key..."
    ssh -i ~/.ssh/id_rsa -f -N -L 5433:misfits.cgncbvolnhe7.ap-south-1.rds.amazonaws.com:5432 claude-control@15.207.255.212
fi

# Wait a moment for tunnel to establish
sleep 2

# Test connection
echo "🧪 Testing database connection..."
PGPASSWORD=postgres psql -h localhost -p 5433 -U dev misfits -c "SELECT 'Connection successful!' as status;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database connection established successfully!"
    echo "🚀 You can now run database queries"
else
    echo "❌ Connection failed. Please check:"
    echo "   1. SSH key exists at ~/Downloads/claude-control-key"
    echo "   2. SSH key has correct permissions (600)"
    echo "   3. Network connectivity to 15.207.255.212"
    echo "   4. Database server is running"
fi