import os
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "ai4bharat/indictrans2-indic-en-1B"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True)

def translate_to_sanskrit(text: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # ✅ Set source and target language tags this way
    tokenizer.src_lang = "en"
    tokenizer.tgt_lang = "sa"

    # Now call tokenizer without explicit lang arguments
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model.generate(**inputs, max_length=512)

    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

if __name__ == "__main__":
    print(translate_to_sanskrit("India is a beautiful country."))
