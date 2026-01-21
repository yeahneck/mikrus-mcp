#!/bin/bash
# Update Mikrus MCP Server with latest fixes

echo "🔄 Updating Mikrus MCP Server..."

# Pull latest code from production branch
cd /opt/mikrus-mcp-server
git checkout production
git pull origin production

# Rebuild
echo "🏗️  Building..."
npm run build

# Restart with PM2 (update environment variables)
echo "♻️  Restarting server..."
pm2 delete mikrus-mcp-server 2>/dev/null || true
PORT=40231 HOST='::' NODE_ENV=production pm2 start dist/server.js --name mikrus-mcp-server

# Show status
echo "✅ Done! Checking status..."
pm2 status
pm2 logs mikrus-mcp-server --lines 20

echo ""
echo "🧪 Testing connection..."
curl http://localhost:40231/health
