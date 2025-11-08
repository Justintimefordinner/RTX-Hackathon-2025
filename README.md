# RTX Hackathon 2025
**NCAT Hack Rangers** - RTX Hackathon 2025 Project

## 🚀 Overview
This is a starter project for the RTX Hackathon 2025, featuring a Python-based AI/ML framework with NVIDIA GPU acceleration support. The project is designed to help teams quickly get started with GPU-accelerated machine learning and deep learning applications.

## ✨ Features
- 🎯 **GPU-Accelerated Computing**: Full CUDA/RTX GPU support with PyTorch
- 🧠 **Pre-configured ML Framework**: Ready-to-use deep learning utilities
- 📊 **Example Projects**: Image classification and GPU benchmarking examples
- 🛠️ **Development Tools**: Testing framework, code formatting, and quality checks
- 📚 **Comprehensive Documentation**: Getting started guides and code examples

## 🏗️ Project Structure
```
RTX-Hackathon-2025/
├── src/                    # Main source code
│   ├── main.py            # Application entry point
│   └── utils.py           # Utility functions
├── examples/              # Example scripts
│   ├── image_classification.py
│   └── gpu_benchmark.py
├── tests/                 # Unit tests
├── config/                # Configuration files
├── docs/                  # Documentation
└── requirements.txt       # Python dependencies
```

## 🚦 Quick Start

### Prerequisites
- Python 3.8 or higher
- NVIDIA RTX GPU (optional, but recommended)
- CUDA Toolkit (for GPU acceleration)

### Installation
```bash
# Clone the repository
git clone https://github.com/Justintimefordinner/RTX-Hackathon-2025.git
cd RTX-Hackathon-2025

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For GPU support (CUDA 11.8)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Running the Application
```bash
# Run main application (checks system and GPU info)
python src/main.py

# Run GPU benchmark
python examples/gpu_benchmark.py

# Run tests
pytest tests/
```

## 📖 Documentation
For detailed documentation, see:
- [Getting Started Guide](docs/getting_started.md)
- Example scripts in the `examples/` folder
- Inline code documentation

## 🧪 Examples

### Check GPU Availability
```python
from src.utils import get_device

device = get_device()
print(f"Using device: {device}")
```

### Run GPU Benchmark
```python
from src.utils import benchmark_gpu

benchmark_gpu(size=(2000, 2000), iterations=100)
```

## 🔧 Development

### Code Quality
```bash
# Format code
black src/ tests/ examples/

# Check code style
flake8 src/ tests/ examples/

# Run tests
pytest tests/ -v
```

## 🤝 Team
**NCAT Hack Rangers** - RTX Hackathon 2025

## 📝 License
This project is created for educational purposes as part of the RTX Hackathon 2025.

## 🎯 Next Steps
1. Explore the example scripts in `examples/`
2. Read the [Getting Started Guide](docs/getting_started.md)
3. Start building your hackathon project!
4. Customize and extend the framework for your specific needs

## 💡 Resources
- [PyTorch Documentation](https://pytorch.org/docs/)
- [NVIDIA CUDA Documentation](https://docs.nvidia.com/cuda/)
- [RTX GPU Features](https://www.nvidia.com/en-us/geforce/rtx/)

---
Built with ❤️ for RTX Hackathon 2025
