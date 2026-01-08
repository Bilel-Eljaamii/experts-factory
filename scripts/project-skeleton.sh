#!/bin/bash

# --- Configuration ---
# Update this list if you want to add more expert domains
DOMAINS=("cybersecurity" "agriculture" "finance" "legal" "automotive")

echo "🔧 Retrofitting current directory into a uv Expert Factory..."

# 1. Check if uv is installed
if ! command -v uv &> /dev/null; then
  echo "❌ 'uv' is not installed. Please install it: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

# 2. Initialize uv project in the CURRENT directory
# This creates pyproject.toml and .python-version if they don't exist
if [ ! -f "pyproject.toml" ]; then
  echo "init: Creating pyproject.toml..."
  # uv init . --no-workspace
else
  echo "info: pyproject.toml already exists, skipping init."
fi

# 3. Add Expert-Level Dependencies
echo "📦 Adding high-performance ML dependencies..."
# Use --raw to avoid version conflicts if you've already started adding things
# uv add torch torchvision torchaudio --index https://download.pytorch.org/whl/cu121
# uv add "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
# uv add xformers trl peft accelerate bitsandbytes datasets
# uv add marker-pdf bonito pydantic pyyaml loguru

# 4. Build the Skeleton (In-Place)
echo "📂 Creating directory structure..."
mkdir -p data/{raw,processed,synthetic}
mkdir -p scripts/{extraction,generation,training,eval}
mkdir -p models/{adapters,final_gguf}
mkdir -p configs
mkdir -p logs
mkdir -p notebooks

# 5. Domain Setup
for domain in "${DOMAINS[@]}"; do
  mkdir -p "data/raw/$domain"
  mkdir -p "data/processed/$domain"
  mkdir -p "data/synthetic/$domain"
  mkdir -p "models/adapters/$domain"

  # Create config only if it doesn't exist to avoid overwriting your work
  if [ ! -f "configs/${domain}_config.yaml" ]; then
    cat << EOF > "configs/${domain}_config.yaml"
project_name: "$domain-expert"
base_model: "unsloth/gemma-2-9b-it-bnb-4bit"
learning_rate: 2e-4
epochs: 3
max_seq_length: 2048
lora_rank: 16
EOF
  fi
  echo "  ✅ Structure ready for: $domain"
done

# 6. Create a generic training script if it doesn't exist
if [ ! -f "scripts/training/train_expert.py" ]; then
  cat << EOF > scripts/training/train_expert.py
import sys
import yaml
from loguru import logger
# from unsloth import FastLanguageModel # Uncomment when running on GPU

def train(domain_config_path):
    with open(domain_config_path, 'r') as f:
        config = yaml.safe_load(f)
    logger.info(f"Initialized training for {config['project_name']} using {config['base_model']}")
    # Your fine-tuning logic goes here

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Please provide a config path.")
    else:
        train(sys.argv[1])
EOF
fi

# 7. Add a smart .gitignore
if [ ! -f ".gitignore" ]; then
  cat << EOF > .gitignore
.venv/
__pycache__/
data/raw/
models/
logs/
.env
*.ipynb_checkpoints
EOF
fi

echo "🔥 Done! Your existing folder is now a structured uv project."
echo "👉 Try running: uv run scripts/training/train_expert.py configs/agriculture_config.yaml"
