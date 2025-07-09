import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

MODEL_NAME = "ai4bharat/indictrans2-indic-en-1B"

# Load tokenizer and model with trust_remote_code=True as required by this model's repo
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

def translate_to_sanskrit(text: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    prefix = "translate English to Sanskrit: "
    input_text = prefix + text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

if __name__ == "__main__":
    print(translate_to_sanskrit("India is a beautiful country."))