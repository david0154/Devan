import os
import shutil
import subprocess
from pathlib import Path
import requests
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    AutoTokenizer
)

MODEL_DIR = Path(__file__).parent / "models"

MODELS = {
    "tinybert": {
        "repo": "prajjwal1/bert-tiny",
        "type": "sequence_classification",
        "local_dir": MODEL_DIR / "tinybert"
    },
    "starcoder-mini": {
        "repo": "bigcode/starcoderbase-1b",
        "type": "causal_lm",
        "local_dir": MODEL_DIR / "starcoder-mini"
    }
}

def ensure_model_downloaded(model_key):
    info = MODELS[model_key]
    if not info["local_dir"].exists():
        print(f"Downloading model {model_key} to {info['local_dir']}")
        info["local_dir"].mkdir(parents=True, exist_ok=True)
        # Use transformers to download
        if info["type"] == "sequence_classification":
            AutoModelForSequenceClassification.from_pretrained(info["repo"], cache_dir=info["local_dir"])
            AutoTokenizer.from_pretrained(info["repo"], cache_dir=info["local_dir"])
        else:
            AutoModelForCausalLM.from_pretrained(info["repo"], cache_dir=info["local_dir"])
            AutoTokenizer.from_pretrained(info["repo"], cache_dir=info["local_dir"])
    else:
        print(f"Model {model_key} already present.")

def check_model_update(model_key):
    # For demo: always False (real: compare revision numbers, etc.)
    return False

def update_model(model_key):
    info = MODELS[model_key]
    print(f"Updating model {model_key}")
    if info["local_dir"].exists():
        shutil.rmtree(info["local_dir"])
    ensure_model_downloaded(model_key)

def load_model(model_key):
    info = MODELS[model_key]
    if info["type"] == "sequence_classification":
        model = AutoModelForSequenceClassification.from_pretrained(str(info["local_dir"]))
        tokenizer = AutoTokenizer.from_pretrained(str(info["local_dir"]))
        return model, tokenizer
    elif info["type"] == "causal_lm":
        model = AutoModelForCausalLM.from_pretrained(str(info["local_dir"]))
        tokenizer = AutoTokenizer.from_pretrained(str(info["local_dir"]))
        return model, tokenizer
    else:
        raise ValueError("Unknown model type")

def check_github_language_update(repo_url, local_version_file):
    # Simple: compare SHA of latest commit for file
    api_url = f"https://api.github.com/repos/{repo_url}/commits?path={local_version_file}&per_page=1"
    r = requests.get(api_url)
    if r.status_code == 200 and r.json():
        latest_commit = r.json()[0]["sha"]
        local_sha = ""
        local_sha_file = local_version_file + ".sha"
        if os.path.exists(local_sha_file):
            with open(local_sha_file, "r") as f:
                local_sha = f.read().strip()
        return latest_commit != local_sha
    return False

def update_language_file(repo_url, file_path, branch="main"):
    raw_url = f"https://raw.githubusercontent.com/{repo_url}/{branch}/{file_path}"
    r = requests.get(raw_url)
    if r.status_code == 200:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"Language file {file_path} updated.")
        # Update SHA
        api_url = f"https://api.github.com/repos/{repo_url}/commits?path={file_path}&per_page=1"
        sha_resp = requests.get(api_url)
        if sha_resp.status_code == 200 and sha_resp.json():
            latest_commit = sha_resp.json()[0]["sha"]
            with open(file_path + ".sha", "w") as f:
                f.write(latest_commit)
    else:
        print(f"Failed to update {file_path}.")
