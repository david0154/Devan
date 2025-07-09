import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

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
                            device = "cuda" if torch.cuda.is_available() else "cpu"
                                model.to(device)
                                    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
                                        outputs = model.generate(**inputs, max_length=512)
                                            return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

                                            # Example usage
                                            if __name__ == "__main__":
                                                print(translate_to_sanskrit("India is a beautiful country."))