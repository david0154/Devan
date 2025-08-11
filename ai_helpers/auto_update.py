import logging
from model_manager import check_model_update, update_model
from model_manager import check_github_file_update, update_file_from_github

# ✅ Set up logging
logging.basicConfig(
    filename='auto_update.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s'
)

def auto_update_models_and_resources():
    repo_url = "https://github.com/david0154/Devan.git"
    file_path = "devan_stdlib.json"  # Resource file path in repo

    # 🔄 Update models
    for model_key in ["tinybert", "codegen-350m"]:
        try:
            if check_model_update(model_key):
                update_model(model_key)
                logging.info(f"✅ Model updated: {model_key}")
            else:
                logging.info(f"⏸ No update needed: {model_key}")
        except Exception as e:
            logging.error(f"❌ Failed to update {model_key}: {e}")

    # 🔄 Update devan_stdlib.json (no encryption)
    try:
        if check_github_file_update(repo_url, file_path):
            update_file_from_github(repo_url, file_path)
            logging.info(f"✅ Updated resource file: {file_path}")
        else:
            logging.info(f"⏸ No update needed for {file_path}")
    except Exception as e:
        logging.error(f"❌ Failed to update {file_path}: {e}")

if __name__ == "__main__":
    auto_update_models_and_resources()
