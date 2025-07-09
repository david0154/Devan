## AI-Powered Code Correction and Updates

### Features

- Integrates TinyBERT for language/bug detection and CodeGen-350M for code completion (CPU-friendly).
- Automatically checks for model and language updates.
- Easy to extend for additional AI models or language resources.

### Usage

#### Install dependencies:
```bash
pip install transformers torch requests
```

#### Download models (first time):
```python
from ai_helpers.model_manager import ensure_model_downloaded
ensure_model_downloaded("tinybert")
ensure_model_downloaded("codegen-350m")
```

#### Correct code or suggest completions:
```python
from ai_helpers.ai_fix import correct_code_with_tinybert, suggest_completion_with_codegen

result = correct_code_with_tinybert("your code snippet here")
print(result)

suggestion = suggest_completion_with_codegen("start of your code")
print(suggestion)
```

#### Auto-update models and language files:
```python
from ai_helpers.auto_update import auto_update_models_and_language
# Replace 'david0154/Devan' and 'path/to/your/lang_file.py' appropriately
auto_update_models_and_language("david0154/Devan", "path/to/your/lang_file.py")
```

---

**Note:**  
- Replace the language file path with your actual Devan language file for updates.
- The TinyBERT correction logic is a placeholder; improve it with a fine-tuned model for real code error detection.
