#!/bin/bash
# Quick setup script for APS Normative Graph System

echo "=========================================="
echo "APS Normative Graph System - Quick Setup"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✓ Virtual environment activated"

# Run Python setup script
echo ""
echo "Running setup script..."
python3 setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "To activate the virtual environment in the future:"
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "  venv\\Scripts\\activate"
    else
        echo "  source venv/bin/activate"
    fi
    echo ""
else
    echo ""
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi
