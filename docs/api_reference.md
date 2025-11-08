# API Reference

## Core Utilities (`src/utils.py`)

### `get_device(prefer_cuda=True)`
Returns the appropriate PyTorch device for computation.

**Parameters:**
- `prefer_cuda` (bool): If True, returns CUDA device if available, otherwise CPU.

**Returns:**
- `torch.device`: The device to use for computations.

**Example:**
```python
from src.utils import get_device

device = get_device()
tensor = torch.randn(3, 3, device=device)
```

### `set_seed(seed=42)`
Sets random seeds for reproducibility across PyTorch, CUDA, and NumPy.

**Parameters:**
- `seed` (int): Random seed value.

**Example:**
```python
from src.utils import set_seed

set_seed(42)
# Now all random operations will be reproducible
```

### `print_model_summary(model)`
Prints a summary of model parameters including total and trainable parameters.

**Parameters:**
- `model` (torch.nn.Module): PyTorch model to summarize.

**Example:**
```python
from src.utils import print_model_summary
import torchvision.models as models

model = models.resnet18()
print_model_summary(model)
```

### `benchmark_gpu(size=(1000, 1000), iterations=100)`
Benchmarks GPU performance using matrix multiplication.

**Parameters:**
- `size` (tuple): Size of matrices to multiply (rows, cols).
- `iterations` (int): Number of iterations to run.

**Example:**
```python
from src.utils import benchmark_gpu

# Quick benchmark
benchmark_gpu(size=(1000, 1000), iterations=100)

# Intensive benchmark
benchmark_gpu(size=(4000, 4000), iterations=50)
```

## Configuration (`config/config.py`)

### GPU Settings
- `USE_GPU`: Enable/disable GPU usage
- `GPU_DEVICE_ID`: Which GPU to use (if multiple available)

### Model Settings
- `MODEL_NAME`: Default model architecture
- `BATCH_SIZE`: Training batch size
- `LEARNING_RATE`: Learning rate for optimization
- `NUM_EPOCHS`: Number of training epochs

### Data Settings
- `IMAGE_SIZE`: Input image size
- `DATA_DIR`: Directory for datasets

### Other Settings
- `RANDOM_SEED`: Random seed for reproducibility
- `LOG_LEVEL`: Logging verbosity
- `LOG_DIR`: Directory for log files

## Examples

### Image Classification (`examples/image_classification.py`)
Demonstrates how to:
- Load pre-trained models
- Preprocess images
- Make predictions with GPU acceleration

### GPU Benchmark (`examples/gpu_benchmark.py`)
Tests GPU performance with various matrix sizes.
