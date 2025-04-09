from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

# Load Model & Tokenizer
model_name = "google/flan-t5-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, device_map="auto")

# Move to MPS (Apple GPU) for efficiency
device = "mps" if torch.backends.mps.is_available() else "cpu"
model.to(device)
