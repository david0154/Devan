import logging
from model_manager import check_model_update, update_model
from model_manager import check_github_language_update, update_language_file

# ✅ Set up logging
logging.basicConfig(
    filename='auto_update.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(message)s'
)

# 🔁 Model & Language auto updater
def auto_update_models_and_language():
    repo_url = "https://github.com/david0154/Devan.git"
    lang_file_path = "devan_stdlib.json"  # Make sure it's correct relative path

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

    # 🔄 Update language file
    try:
        if check_github_language_update(repo_url, lang_file_path):
            update_language_file(repo_url, lang_file_path)
            logging.info("✅ Language file updated: devan_stdlib.json")
        else:
            logging.info("⏸ No change in devan_stdlib.json")
    except Exception as e:
        logging.error(f"❌ Language update failed: {e}")

# 📜 Entry point
if __name__ == "__main__":
    auto_update_models_and_language()
