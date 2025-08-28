#!/bin/bash

# Telegram Mini App Deployment Script

echo "🚀 Deploying Telegram Mini App..."

# Build and start containers
docker-compose -f docker-compose-miniapp.yml down
docker-compose -f docker-compose-miniapp.yml build
docker-compose -f docker-compose-miniapp.yml up -d

echo "✅ Mini App deployed successfully!"
echo "📋 Services status:"
docker-compose -f docker-compose-miniapp.yml ps

echo ""
echo "🌐 Mini App will be available at:"
echo "   Local: http://localhost:3000"
echo "   Cloudflare tunnel URL will appear in cloudflared-miniapp logs"

echo ""
echo "📱 To get the Cloudflare tunnel URL:"
echo "   docker-compose -f docker-compose-miniapp.yml logs cloudflared-miniapp"

echo ""
echo "🛠️  To stop the Mini App:"
echo "   docker-compose -f docker-compose-miniapp.yml down"