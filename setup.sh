#!/bin/bash

# Setup script for RTX Hackathon 2025 project

echo "=================================="
echo "RTX Hackathon 2025 - Setup Script"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check for CUDA
echo ""
echo "Checking for CUDA availability..."
python3 -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the main application: python src/main.py"
echo "  3. Try the examples: python examples/gpu_benchmark.py"
echo ""
