import torch
import os
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
import numpy as np 
from transformers import LlamaTokenizer
from transformers import pipeline
from peft import PeftModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

model_name = 'NousResearch/Llama-2-7b-chat-hf'
peft_model = 'finetuned_models/dow30-llama2-custom_202312271412'
merged_peft_model_name = 'Hacks234/unbound'

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code = True)
tokenizer.pad_token = tokenizer.eos_token
max_seq_length = tokenizer.model_max_length

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.float16
)

hf_token = os.getenv("HF_TOKEN")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    token = hf_token,
    load_in_8bit = False,
    torch_dtype = torch.float16,
    device_map = "cpu",
    offload_folder = "offload"
)

model = PeftModel.from_pretrained(
    model,
    peft_model,
    torch_dtype = torch.float16,
    device_map = "cpu",
    offload_folder = "offload"
)

model = model.merge_and_unload()
model.save_pretrained(merged_peft_model_name)
tokenizer.save_pretrained(merged_peft_model_name)
model.push_to_hub(merged_peft_model_name)