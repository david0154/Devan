from .model_manager import check_model_update, update_model, check_github_language_update, update_language_file

def auto_update_models_and_language(repo_url, lang_file_path):
    for model_key in ["tinybert", "codegen-350m"]:
        if check_model_update(model_key):
            update_model(model_key)
    if check_github_language_update(repo_url, lang_file_path):
        update_language_file(repo_url, lang_file_path)
