#!/bin/bash
# Medical Report System - Stop Script

echo "🛑 Stopping Medical Report Drafting System..."

# Find and kill the Motia server process
PIDS=$(pgrep -f "motia dev")

if [ -z "$PIDS" ]; then
    echo "   ℹ️  Server is not running"
    exit 0
fi

# Kill the processes
for PID in $PIDS; do
    echo "   Stopping process $PID..."
    kill -9 $PID 2>/dev/null
done

# Wait a moment
sleep 1

# Verify
if ! pgrep -f "motia dev" > /dev/null; then
    echo "   ✅ Server stopped successfully"
else
    echo "   ⚠️  Some processes may still be running"
    echo "   Run: ps aux | grep 'motia dev'"
fi
