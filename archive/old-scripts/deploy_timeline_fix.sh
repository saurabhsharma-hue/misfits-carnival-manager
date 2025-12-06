#!/bin/bash

echo "🚀 Deploying Timeline Filter Fix to Production"
echo "============================================"

# Check if SSH key exists
if [ ! -f ~/Downloads/claude-control-key ]; then
    echo "❌ SSH key not found at ~/Downloads/claude-control-key"
    exit 1
fi

# Ensure proper permissions
echo "🔧 Setting SSH key permissions..."
chmod 600 ~/Downloads/claude-control-key

# Test SSH connection first
echo "🔍 Testing SSH connection..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -i ~/Downloads/claude-control-key claude-control@15.207.255.212 "echo 'SSH connection successful'"

if [ $? -ne 0 ]; then
    echo "❌ SSH connection failed. Please check:"
    echo "   - SSH key is valid"
    echo "   - Server is accessible"
    echo "   - Network connectivity"
    exit 1
fi

# Deploy the file
echo "📤 Deploying file to production..."
scp -o StrictHostKeyChecking=no -i ~/Downloads/claude-control-key \
    /Users/retalplaza/Downloads/Misfits_Carnival_Manager_WORKING_FIXED.html \
    claude-control@15.207.255.212:/var/www/carnival/index.html

if [ $? -eq 0 ]; then
    echo "✅ Deployment successful!"
    echo "🌐 Timeline filters are now live at: http://carnival.misfits.net.in"
    echo "💡 Clear browser cache (Ctrl+F5) to see the changes"
else
    echo "❌ Deployment failed!"
    exit 1
fi

echo ""
echo "🎯 What's been deployed:"
echo "   ✅ Timeline dropdown population fix"
echo "   ✅ Missing status filter fix"
echo "   ✅ Filter value preservation fix"
echo "   ✅ Dynamic filters from actual data"
echo ""
echo "🧪 Test the Timeline section filters at the production URL"