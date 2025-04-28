#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then 
    print_warning "Please run this script with sudo"
    exit 1
fi

# Project directory
PROJECT_DIR="/Users/mike/Desktop/portfolio_project"
NGINX_CONF_DIR="/usr/local/etc/nginx/servers"
SUPERVISOR_CONF_DIR="/usr/local/etc/supervisor.d"

print_status "Starting deployment process..."

# Create necessary directories
print_status "Creating required directories..."
mkdir -p /var/log/nginx
mkdir -p /var/log/supervisor
mkdir -p "$NGINX_CONF_DIR"
mkdir -p "$SUPERVISOR_CONF_DIR"

# Install dependencies using Homebrew and pip
print_status "Installing dependencies..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

brew install nginx || print_warning "Nginx installation failed or already installed"

# Install Python dependencies
print_status "Installing Python packages..."
pip3 install gunicorn supervisor || {
    print_warning "Failed to install Python packages"
    exit 1
}

# Copy configuration files
print_status "Copying configuration files..."
cp "$PROJECT_DIR/nginx.conf" "$NGINX_CONF_DIR/task_manager.conf" || {
    print_warning "Failed to copy Nginx configuration"
    exit 1
}

cp "$PROJECT_DIR/supervisor.conf" "$SUPERVISOR_CONF_DIR/task_manager.ini" || {
    print_warning "Failed to copy Supervisor configuration"
    exit 1
}

# Set correct permissions
print_status "Setting permissions..."
chmod 644 "$NGINX_CONF_DIR/task_manager.conf"
chmod 644 "$SUPERVISOR_CONF_DIR/task_manager.ini"
chmod -R 755 "$PROJECT_DIR/app/static"

# Start/Restart services
print_status "Starting services..."

# Stop existing services if running
nginx -s stop 2>/dev/null || true
pkill supervisord 2>/dev/null || true

# Start Supervisor
print_status "Starting Supervisor..."
supervisord -c "$SUPERVISOR_CONF_DIR/task_manager.ini"
sleep 2
supervisorctl reread
supervisorctl update
supervisorctl start task_manager

# Start Nginx
print_status "Starting Nginx..."
nginx

# Verify services
print_status "Verifying services..."
if pgrep -x "nginx" > /dev/null; then
    print_status "Nginx is running"
else
    print_warning "Nginx failed to start"
fi

if pgrep -x "supervisord" > /dev/null; then
    print_status "Supervisor is running"
else
    print_warning "Supervisor failed to start"
fi

# Test the application
print_status "Testing the application..."
if curl -s http://localhost > /dev/null; then
    print_status "Application is accessible at http://localhost"
else
    print_warning "Application is not responding"
fi

print_status "Deployment complete!"
print_status "You can check the application at http://localhost"
print_status "Check logs at:"
print_status "- Nginx: /var/log/nginx/task_manager_error.log"
print_status "- Supervisor: /var/log/supervisor/task_manager.err.log" 