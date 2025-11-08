"""
RTX Hackathon 2025 - Main Application Entry Point
NCAT Hack Rangers

This is the main entry point for the RTX Hackathon project.
"""

import sys
import torch
import platform


def check_gpu_availability():
    """Check if CUDA/GPU is available and display system information."""
    print("=" * 60)
    print("RTX Hackathon 2025 - System Information")
    print("=" * 60)
    print(f"Python Version: {sys.version}")
    print(f"PyTorch Version: {torch.__version__}")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor()}")

    # Check CUDA availability
    cuda_available = torch.cuda.is_available()
    print(f"\nCUDA Available: {cuda_available}")

    if cuda_available:
        print(f"CUDA Version: {torch.version.cuda}")
        print(f"Number of GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
            props = torch.cuda.get_device_properties(i)
            print(f"    Total Memory: {props.total_memory / 1e9:.2f} GB")
            print(f"    Compute Capability: {props.major}.{props.minor}")
    else:
        print("No GPU detected. Running on CPU.")

    print("=" * 60)


def main():
    """Main application function."""
    print("\n🚀 Welcome to RTX Hackathon 2025!")
    print("NCAT Hack Rangers Team\n")

    # Check system and GPU
    check_gpu_availability()

    print("\n✅ Application initialized successfully!")
    print("\nTo get started:")
    print("  1. Check the examples/ folder for sample code")
    print("  2. Read the documentation in docs/")
    print("  3. Start building your hackathon project!")
    print("\nGood luck! 🎉\n")


if __name__ == "__main__":
    main()
