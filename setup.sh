#!/bin/bash

# Development setup script for Beszel MCP Server

set -e

echo "Setting up Beszel MCP Server development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install package in development mode with dev dependencies
echo "Installing package and dependencies..."
pip install -e ".[dev]"

echo ""
echo "Setup complete! To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "To run the server, set environment variables and execute:"
echo "  export BESZEL_URL='http://localhost:8090'"
echo "  export BESZEL_EMAIL='your-email@example.com'"
echo "  export BESZEL_PASSWORD='your-password'"
echo "  python -m beszel_mcp"
echo ""
echo "To run tests:"
echo "  pytest"
