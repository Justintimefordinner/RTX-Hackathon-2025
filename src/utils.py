"""
Utility functions for the RTX Hackathon project.
"""

import torch
import numpy as np
from typing import Tuple


def get_device(prefer_cuda: bool = True) -> torch.device:
    """
    Get the appropriate device (CUDA/CPU) for PyTorch operations.

    Args:
        prefer_cuda: If True, use CUDA if available. Otherwise, use CPU.

    Returns:
        torch.device: The device to use for computations.
    """
    if prefer_cuda and torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = torch.device("cpu")
        print("Using CPU")
    return device


def set_seed(seed: int = 42):
    """
    Set random seeds for reproducibility.

    Args:
        seed: Random seed value.
    """
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    print(f"Random seed set to {seed}")


def print_model_summary(model: torch.nn.Module):
    """
    Print a summary of model parameters.

    Args:
        model: PyTorch model.
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    print("\nModel Summary:")
    print(f"  Total parameters: {total_params:,}")
    print(f"  Trainable parameters: {trainable_params:,}")
    print(f"  Non-trainable parameters: {total_params - trainable_params:,}")


def benchmark_gpu(size: Tuple[int, int] = (1000, 1000), iterations: int = 100):
    """
    Simple GPU benchmark using matrix multiplication.

    Args:
        size: Size of matrices to multiply.
        iterations: Number of iterations for the benchmark.
    """
    import time

    device = get_device()

    print(f"\nRunning GPU benchmark ({iterations} iterations)...")
    print(f"Matrix size: {size[0]}x{size[1]}")

    # Create random matrices
    a = torch.randn(size, device=device)
    b = torch.randn(size, device=device)

    # Warm-up
    for _ in range(10):
        _ = torch.matmul(a, b)

    if device.type == "cuda":
        torch.cuda.synchronize()

    # Benchmark
    start_time = time.time()
    for _ in range(iterations):
        _ = torch.matmul(a, b)

    if device.type == "cuda":
        torch.cuda.synchronize()

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Total time: {elapsed:.4f} seconds")
    print(f"Average time per iteration: {elapsed/iterations*1000:.4f} ms")
    print(f"Operations per second: {iterations/elapsed:.2f}")
