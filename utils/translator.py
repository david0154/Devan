import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "ai4bharat/indictrans2-indic-en-1B"

# 🔧 Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

def translate_to_sanskrit(text: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 🏷️ Provide language tags explicitly
    src_lang = "en"
    tgt_lang = "sa"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
        src_lang=src_lang,
        tgt_lang=tgt_lang
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model.generate(**inputs, max_length=512)

    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

if __name__ == "__main__":
    print(translate_to_sanskrit("India is a beautiful country."))
