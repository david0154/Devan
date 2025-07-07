import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_DIR = "models/indictrans/"
MODEL_NAME = "ai4bharat/indictrans2-en-sa"

def setup_model():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, cache_dir=MODEL_DIR)
    return tokenizer, model

tokenizer, model = setup_model()

def translate_to_sanskrit(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    outputs = model.generate(**inputs, max_length=512)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
