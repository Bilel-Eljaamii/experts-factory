# Utils Package

Shared utilities for the experts-factory project.

## 📦 Modules

### `training_logger.py`

Comprehensive logging system for training runs.

**Features:**

- ✅ Unique timestamped log files (`training_log_YYYYMMDD_HHMMSS.md`)
- ✅ Markdown format with emojis and formatting
- ✅ Structured sections for different training phases
- ✅ Configuration tables
- ✅ Metrics tracking
- ✅ Dual output (file + console)

**Usage:**

```python
from utils.training_logger import TrainingLogger

# Initialize logger
logger = TrainingLogger(log_dir="../logs", log_prefix="training")

# Log messages
logger.log("Starting process...", level="INFO")
logger.log("Success!", level="SUCCESS")

# Create sections
logger.log_section("Model Training")

# Log configurations
config = {"learning_rate": 0.0002, "batch_size": 2}
logger.log_config(config, "Training Configuration")

# Log metrics
metrics = {"loss": 1.234, "accuracy": 0.95}
logger.log_metrics(metrics, step=100)

# Finalize
logger.finalize()
```

**Log Levels:**

- `INFO` ℹ️ - General information
- `SUCCESS` ✅ - Successful operations
- `WARNING` ⚠️ - Warnings
- `ERROR` ❌ - Errors
- `STEP` 🔹 - Step markers

**Output Location:** Logs are saved to the root `logs/` directory with unique
timestamped filenames.

## 📖 Documentation

For detailed integration guides and examples, see:

- `docs/LOGGING_INTEGRATION_GUIDE.md` - Step-by-step integration
- `docs/LOGGER_QUICK_REFERENCE.md` - Quick reference card
- `notebooks/logging_snippets.py` - Ready-to-use code snippets
- `logs/example_training_log.md` - Example output

## 🔧 Adding New Utilities

When adding new utility modules:

1. Create the module file in `utils/`
2. Add imports to `__init__.py`
3. Update this README
4. Add documentation to `docs/` if needed

Example:

```python
# utils/my_utility.py
def my_function():
    pass

# utils/__init__.py
from .my_utility import my_function
__all__ = ['TrainingLogger', 'my_function']
```
