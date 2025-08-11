import torch
from .model_manager import load_model

# Automatically use GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def correct_code_with_tinybert(code_snippet):
    """
    Uses a TinyBERT model to check for potential errors in a code snippet.
    This is a placeholder example. For real results, fine-tune TinyBERT on code error datasets.
    """
    model, tokenizer = load_model("tinybert")
    model.to(device)
    model.eval()

    # Tokenize input code
    inputs = tokenizer(
        code_snippet,
        return_tensors="pt",
        truncation=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred = logits.argmax(dim=-1).item()

    if pred == 0:
        return "✅ No obvious errors detected (TinyBERT demo)."
    else:
        return "⚠️ Potential error detected (TinyBERT demo)."

def suggest_completion_with_codegen(code_prefix, max_length=64):
    """
    Uses CodeGen model to generate code completion based on the provided prefix.
    """
    model, tokenizer = load_model("codegen-350m")
    model.to(device)
    model.eval()

    input_ids = tokenizer.encode(
        code_prefix,
        return_tensors="pt"
    ).to(device)

    # Generate completion
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
