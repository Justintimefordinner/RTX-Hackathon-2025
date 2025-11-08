"""
Unit tests for utility functions.
"""

import torch
from src.utils import get_device, set_seed


def test_get_device_returns_valid_device():
    """Test that get_device returns a valid PyTorch device."""
    device = get_device()
    assert isinstance(device, torch.device)
    assert device.type in ["cuda", "cpu"]


def test_get_device_cpu_fallback():
    """Test that CPU fallback works."""
    device = get_device(prefer_cuda=False)
    assert device.type == "cpu"


def test_set_seed_reproducibility():
    """Test that set_seed produces reproducible results."""
    set_seed(42)
    random_tensor1 = torch.rand(5)

    set_seed(42)
    random_tensor2 = torch.rand(5)

    assert torch.allclose(random_tensor1, random_tensor2)


def test_set_seed_different_results():
    """Test that different seeds produce different results."""
    set_seed(42)
    random_tensor1 = torch.rand(5)

    set_seed(123)
    random_tensor2 = torch.rand(5)

    assert not torch.allclose(random_tensor1, random_tensor2)
