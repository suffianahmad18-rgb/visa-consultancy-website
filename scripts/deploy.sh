#!/bin/bash

# Deployment script for Visa Consultancy Website
set -e  # Exit on error

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f .env ]; then
    echo -e "${YELLOW}Loading environment variables...${NC}"
    export $(cat .env | grep -v '^#' | xargs)
fi

# Function to print status
print_status() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

print_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Backup database
print_status "Backing up database..."
BACKUP_FILE="backups/db_backup_$(date +'%Y%m%d_%H%M%S').sql"
python manage.py dumpdata > "$BACKUP_FILE"
print_status "Database backed up to $BACKUP_FILE"

# Pull latest changes
print_status "Pulling latest code..."
git pull origin main

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate  # Windows vs Linux

# Install dependencies
print_status "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
print_status "Running database migrations..."
python manage.py migrate

# Collect static files
print_status "Collecting static files..."
python manage.py collectstatic --noinput

# Clear cache
print_status "Clearing cache..."
python manage.py clear_cache || echo "Cache clear skipped"

# Run tests
print_status "Running tests..."
python manage.py test

if [ $? -eq 0 ]; then
    print_status "Tests passed! ✅"
else
    print_error "Tests failed! ❌"
    exit 1
fi

# Restart services
print_status "Restarting services..."
if command -v systemctl &> /dev/null; then
    sudo systemctl restart gunicorn
    sudo systemctl restart nginx
    sudo systemctl restart celery
    sudo systemctl restart celerybeat
else
    print_status "Systemctl not found, skipping service restart"
    # For development: restart Django server
    pkill -f runserver || true
    python manage.py runserver 0.0.0.0:8000 &
fi

# Health check
print_status "Running health check..."
python scripts/health_check.py

if [ $? -eq 0 ]; then
    print_status "Health check passed! ✅"
else
    print_error "Health check failed! ❌"
    exit 1
fi

print_status "✅ Deployment completed successfully!"