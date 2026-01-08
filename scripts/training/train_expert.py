from unsloth import FastLanguageModel
import torch

def train(config_path):
    # ... (load config logic) ...

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = config['base_model'],
        max_seq_length = config['max_seq_length'],
        load_in_4bit = True, # CRITICAL for T4
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r = config['lora_rank'],
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                          "gate_proj", "up_proj", "down_proj",],
        lora_alpha = 16,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth", # CRITICAL for T4
        random_state = 3407,
    )

    # ... (Rest of training logic) ...