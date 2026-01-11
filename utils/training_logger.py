"""
Training Logger for Gemma 2 Fine-tuning

This module provides a comprehensive logging system that:
- Creates unique log files with timestamps
- Saves logs in markdown format for easy reading
- Tracks all major training steps and metrics
- Stores logs in the root 'logs/' directory
"""

from pathlib import Path
from datetime import datetime
import json


class TrainingLogger:
    """
    Custom logger that writes training progress to markdown files.
    
    Features:
    - Unique log file per training run (timestamped)
    - Markdown format for easy reading
    - Structured sections for different training phases
    - Automatic directory creation
    """
    
    def __init__(self, log_dir="../logs", log_prefix="training"):
        """
        Initialize logger with unique log file.
        
        Args:
            log_dir: Directory to store log files (default: '../logs' - root logs folder)
            log_prefix: Prefix for log filename (default: 'training')
        """
        # Get the absolute path to the logs directory
        self.log_dir = Path(log_dir).resolve()
        self.log_dir.mkdir(exist_ok=True)  # Create logs directory if it doesn't exist
        
        # Generate unique log filename with timestamp
        # Format: training_log_YYYYMMDD_HHMMSS.md
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"{log_prefix}_log_{timestamp}.md"
        
        # Initialize log file with header
        self._write_header()
        
        print(f"📝 Logging to: {self.log_file}")
    
    def _write_header(self):
        """Write initial header to log file."""
        header = f"""# Gemma 2 Cybersecurity Expert Training Log

**Training Started**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Model**: Gemma 2 9B (4-bit quantized)
**Dataset**: NIST Cybersecurity Training
**Method**: LoRA Fine-tuning

---

"""
        with open(self.log_file, 'w') as f:
            f.write(header)
    
    def log(self, message, level="INFO"):
        """
        Log a message with timestamp.
        
        Args:
            message: Message to log
            level: Log level (INFO, SUCCESS, WARNING, ERROR, STEP)
        """
        # Emoji mapping for different log levels
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "STEP": "🔹"
        }
        
        emoji = emoji_map.get(level, "📌")
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"\n**[{timestamp}]** {emoji} **{level}**: {message}\n"
        
        # Write to file
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
        # Also print to console
        print(f"{emoji} [{timestamp}] {message}")
    
    def log_section(self, title):
        """
        Start a new section in the log.
        
        Args:
            title: Section title
        """
        section = f"\n\n## {title}\n\n"
        with open(self.log_file, 'a') as f:
            f.write(section)
        print(f"\n{'='*60}\n{title}\n{'='*60}")
    
    def log_config(self, config_dict, title="Configuration"):
        """
        Log configuration parameters in a formatted table.
        
        Args:
            config_dict: Dictionary of configuration parameters
            title: Section title
        """
        self.log_section(title)
        
        # Create markdown table
        table = "\n| Parameter | Value |\n|-----------|-------|\n"
        for key, value in config_dict.items():
            table += f"| {key} | {value} |\n"
        
        with open(self.log_file, 'a') as f:
            f.write(table)
        
        # Print to console
        print(json.dumps(config_dict, indent=2))
    
    def log_metrics(self, metrics_dict, step=None):
        """
        Log training metrics.
        
        Args:
            metrics_dict: Dictionary of metrics
            step: Training step number (optional)
        """
        step_info = f" (Step {step})" if step else ""
        metrics_str = ", ".join([f"{k}: {v}" for k, v in metrics_dict.items()])
        self.log(f"Metrics{step_info}: {metrics_str}", level="INFO")
    
    def log_code_block(self, code, language="python", title=None):
        """
        Log a code block in markdown format.
        
        Args:
            code: Code to log
            language: Programming language for syntax highlighting
            title: Optional title for the code block
        """
        if title:
            self.log(title, level="INFO")
        
        code_block = f"\n```{language}\n{code}\n```\n"
        with open(self.log_file, 'a') as f:
            f.write(code_block)
    
    def log_output(self, output, title=None, max_lines=50):
        """
        Log command or cell output.
        
        Args:
            output: Output text to log
            title: Optional title for the output
            max_lines: Maximum number of lines to log (default: 50)
        """
        if title:
            self.log(title, level="INFO")
        
        # Truncate if too long
        lines = output.split('\n')
        if len(lines) > max_lines:
            truncated_output = '\n'.join(lines[:max_lines])
            truncated_output += f"\n... (truncated {len(lines) - max_lines} lines)"
        else:
            truncated_output = output
        
        output_block = f"\n```\n{truncated_output}\n```\n"
        with open(self.log_file, 'a') as f:
            f.write(output_block)
    
    def log_cell_output(self, cell_name, output, success=True):
        """
        Log notebook cell output with formatting.
        
        Args:
            cell_name: Name/description of the cell
            output: Cell output (can be string, dict, or list)
            success: Whether the cell executed successfully
        """
        level = "SUCCESS" if success else "ERROR"
        self.log(f"Cell: {cell_name}", level=level)
        
        # Handle different output types
        if isinstance(output, dict):
            output_str = json.dumps(output, indent=2)
        elif isinstance(output, list):
            output_str = '\n'.join(str(item) for item in output)
        else:
            output_str = str(output)
        
        # Log the output in a collapsible details block
        details_block = f"\n<details>\n<summary>📋 Output</summary>\n\n```\n{output_str}\n```\n\n</details>\n\n"
        with open(self.log_file, 'a') as f:
            f.write(details_block)
    
    def log_error(self, error_message, traceback=None):
        """
        Log an error with optional traceback.
        
        Args:
            error_message: Error message
            traceback: Optional traceback string
        """
        self.log(f"Error: {error_message}", level="ERROR")
        
        if traceback:
            error_block = f"\n<details>\n<summary>🔍 Traceback</summary>\n\n```python\n{traceback}\n```\n\n</details>\n\n"
            with open(self.log_file, 'a') as f:
                f.write(error_block)
    
    def log_training_progress(self, step, total_steps, loss, metrics=None):
        """
        Log training progress with progress bar visualization.
        
        Args:
            step: Current training step
            total_steps: Total number of steps
            loss: Current loss value
            metrics: Optional dictionary of additional metrics
        """
        # Calculate progress percentage
        progress = (step / total_steps) * 100
        
        # Create progress bar (20 characters wide)
        bar_length = 20
        filled = int(bar_length * step / total_steps)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Format message
        message = f"Step {step}/{total_steps} [{bar}] {progress:.1f}% | Loss: {loss:.4f}"
        
        if metrics:
            metrics_str = " | " + ", ".join([f"{k}: {v:.4f}" if isinstance(v, float) else f"{k}: {v}" 
                                             for k, v in metrics.items()])
            message += metrics_str
        
        self.log(message, level="STEP")

    
    def finalize(self):
        """Write final summary to log file."""
        footer = f"""

---

**Training Completed**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

✅ **All steps completed successfully!**

"""
        with open(self.log_file, 'a') as f:
            f.write(footer)
        
        print(f"\n✅ Complete log saved to: {self.log_file}")
