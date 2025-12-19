#!/bin/bash
# Medical Report System - Quick Start Script

echo "🏥 Starting Medical Report Drafting System..."
echo ""

# Change to project directory
cd "$(dirname "$0")"

# Check if Redis is running
if ! systemctl is-active --quiet redis-server 2>/dev/null; then
    echo "⚠️  Starting Redis server..."
    sudo systemctl start redis-server 2>/dev/null || echo "   (Redis may already be running)"
fi

# Check if server is already running
if pgrep -f "motia dev" > /dev/null; then
    echo "⚠️  Server already running!"
    echo "   🌐 Access at: http://localhost:3000/medical"
    exit 0
fi

# Start the server
echo "🚀 Starting Motia server..."
npm run dev &

# Wait for server to be ready
echo "⏳ Waiting for server to start..."
sleep 8

# Check if server started successfully
if curl -s http://localhost:3000/medical > /dev/null 2>&1; then
    echo ""
    echo "✅ Server started successfully!"
    echo ""
    echo "════════════════════════════════════════════════"
    echo "   🏥 MEDICAL REPORT DRAFTING SYSTEM"
    echo "════════════════════════════════════════════════"
    echo ""
    echo "📱 Access Application:"
    echo "   🌐 http://localhost:3000/medical"
    echo ""
    echo "📚 Documentation:"
    echo "   📖 See USAGE.md for detailed instructions"
    echo ""
    echo "🛑 To Stop Server:"
    echo "   Run: ./stop.sh"
    echo "   Or press Ctrl+C in terminal"
    echo ""
else
    echo ""
    echo "❌ Server failed to start!"
    echo "   Check logs above for errors"
    exit 1
fi
