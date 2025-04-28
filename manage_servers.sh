#!/bin/bash

echo "🔄 Cleaning up existing processes..."

# Kill any existing Flask processes
if pgrep -f "python.*app.py" > /dev/null; then
    echo "Stopping Flask processes..."
    pkill -f "python.*app.py"
    sleep 2
fi

# Stop Nginx service
if brew services list | grep -q "nginx.*started"; then
    echo "Stopping Nginx service..."
    brew services stop nginx
    sleep 2
fi

# Kill any remaining Nginx processes
if pgrep nginx > /dev/null; then
    echo "Stopping remaining Nginx processes..."
    sudo pkill nginx
    sleep 2
fi

echo "✨ Starting services fresh..."

# Start Flask application
echo "Starting Flask application..."
nohup python app.py > flask.log 2>&1 &
sleep 3

# Start Nginx
echo "Starting Nginx service..."
brew services start nginx
sleep 3

# Verify services
echo -e "\n🔍 Verifying services..."
echo "Checking Flask (port 8000):"
lsof -i :8000 || echo "⚠️  Flask not detected on port 8000"

echo -e "\nChecking Nginx (port 3000):"
lsof -i :3000 || echo "⚠️  Nginx not detected on port 3000"

echo -e "\n📝 Recent Flask logs:"
tail -n 5 flask.log

echo -e "\n📝 Recent Nginx error logs:"
tail -n 5 /opt/homebrew/var/log/nginx/error.log

echo -e "\n✅ Setup complete!"
echo "You can now access:"
echo "- Flask direct: http://127.0.0.1:8000"
echo "- Through Nginx: http://localhost:3000" 