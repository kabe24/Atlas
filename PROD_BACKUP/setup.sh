#!/bin/bash
# ─── Atlas Setup Script ───────────────────────────────────────
# This script installs dependencies and starts the tutor.
# Run it once to set up, and again anytime you want to start the tutor.

set -e

echo ""
echo "🎓 Atlas Setup"
echo "─────────────────────────────────────"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "   Download it from: https://python.org/downloads"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $PYTHON_VERSION found"

# Check for .env file
if [ ! -f .env ]; then
    echo ""
    echo "📋 First-time setup: I need your Anthropic API key."
    echo "   (Get one at https://console.anthropic.com)"
    echo ""
    read -p "   Paste your API key here: " API_KEY
    echo "ANTHROPIC_API_KEY=$API_KEY" > .env
    echo "✅ API key saved to .env"
else
    echo "✅ API key found"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet 2>/dev/null || python3 -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null
echo "✅ Dependencies installed"

# Create data directory
mkdir -p data/sessions

# Start the server
echo ""
echo "─────────────────────────────────────"
echo "🚀 Starting Atlas..."
echo ""
echo "   ➜  Open your browser to:"
echo ""
echo "       http://localhost:8000"
echo ""
echo "   Press Ctrl+C to stop the tutor."
echo "─────────────────────────────────────"
echo ""

python3 app.py
