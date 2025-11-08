"""
Example: GPU Benchmark

This example demonstrates GPU performance testing.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import benchmark_gpu, get_device  # noqa: E402


def main():
    """Run GPU benchmark."""
    print("=" * 60)
    print("GPU Benchmark Example")
    print("=" * 60)

    device = get_device()

    if device.type == "cuda":
        print("\n🚀 Running performance tests...")

        # Small matrices
        print("\n1. Small matrices (1000x1000):")
        benchmark_gpu(size=(1000, 1000), iterations=100)

        # Medium matrices
        print("\n2. Medium matrices (2000x2000):")
        benchmark_gpu(size=(2000, 2000), iterations=50)

        # Large matrices
        print("\n3. Large matrices (4000x4000):")
        benchmark_gpu(size=(4000, 4000), iterations=10)
    else:
        print("\n⚠️ No GPU available. Benchmark requires CUDA-enabled GPU.")
        print("Running a simple CPU test instead...")
        benchmark_gpu(size=(500, 500), iterations=10)

    print("\n✅ Benchmark completed!")


if __name__ == "__main__":
    main()
