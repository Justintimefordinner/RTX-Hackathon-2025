# Getting Started Guide

## Overview
Welcome to the RTX Hackathon 2025 project! This guide will help you get started with the codebase.

## Project Structure
```
RTX-Hackathon-2025/
├── src/                 # Main source code
│   ├── main.py         # Application entry point
│   └── utils.py        # Utility functions
├── examples/           # Example scripts
│   ├── image_classification.py
│   └── gpu_benchmark.py
├── tests/              # Unit tests
├── config/             # Configuration files
├── docs/               # Documentation
└── requirements.txt    # Python dependencies
```

## Quick Start

### 1. Environment Setup
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. GPU Setup (Optional but Recommended)
For NVIDIA RTX GPU support, install PyTorch with CUDA:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 3. Run the Application
```bash
python src/main.py
```

### 4. Try Examples
```bash
# GPU benchmark
python examples/gpu_benchmark.py

# Image classification (requires an image)
python examples/image_classification.py
```

### 5. Run Tests
```bash
pytest tests/
```

## Development Tips

### Check GPU Availability
The application automatically detects GPU availability. Run `python src/main.py` to see system information.

### Using the Utilities
```python
from src.utils import get_device, set_seed, benchmark_gpu

# Get the best available device (CUDA or CPU)
device = get_device()

# Set random seed for reproducibility
set_seed(42)

# Benchmark your GPU
benchmark_gpu(size=(2000, 2000), iterations=50)
```

## Common Tasks

### Adding New Features
1. Create new modules in `src/`
2. Add example usage in `examples/`
3. Write tests in `tests/`
4. Update documentation

### Running Code Quality Checks
```bash
# Format code
black src/ tests/ examples/

# Check code style
flake8 src/ tests/ examples/
```

## Resources
- [PyTorch Documentation](https://pytorch.org/docs/)
- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)
- [Python Best Practices](https://docs.python-guide.org/)

## Troubleshooting

### GPU Not Detected
- Ensure NVIDIA drivers are installed
- Install CUDA-enabled PyTorch
- Check `nvidia-smi` command output

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ recommended)

## Team
NCAT Hack Rangers - RTX Hackathon 2025
