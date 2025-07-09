from .model_manager import load_model
import torch

def correct_code_with_tinybert(code_snippet):
    model, tokenizer = load_model("tinybert")
    model.eval()
    # Placeholder logic: you may want to fine-tune for real code error detection
    inputs = tokenizer(code_snippet, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = logits.argmax(dim=-1).item()
        if pred == 0:
            return "No obvious errors detected (TinyBERT demo)."
        else:
            return "Potential error detected (TinyBERT demo)."

def suggest_completion_with_codegen(code_prefix, max_length=64):
    model, tokenizer = load_model("codegen-350m")
    input_ids = tokenizer.encode(code_prefix, return_tensors="pt")
    outputs = model.generate(input_ids, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
