import sys
import subprocess
import os
from utils.translator import translate_to_sanskrit
from utils.encryptor import encrypt

def save_translated_and_encrypted(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        original_code = f.read()

    # Encrypt and overwrite the original file
    encrypted = encrypt(original_code)
    with open(file_path, 'wb') as f:
        f.write(encrypted)

    # Translate to Sanskrit and save encrypted version
    sanskrit_code = translate_to_sanskrit(original_code)
    sanskrit_path = file_path.replace('.om', '_sa.om').replace('.OM', '_sa.OM').replace('.Om', '_sa.Om')

    with open(sanskrit_path, 'wb') as f:
        f.write(encrypt(sanskrit_code))

    print(f"🔐 Saved: {file_path} (encrypted)")
    print(f"🧠 Translated + Saved: {sanskrit_path} (Sanskrit + encrypted)")

def run_interpreter(file_path):
    try:
        subprocess.run(["python", "devan_parser.py", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Interpreter failed with error code {e.returncode}")
    except Exception as e:
        print(f"❌ Interpreter error: {e}")

def run_compiler(file_path, lang="auto"):
    try:
        subprocess.run(["python", "devan_compiler.py", file_path, "--lang", lang], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation failed with error code {e.returncode}")
    except Exception as e:
        print(f"❌ Compilation error: {e}")

def main():
    if len(sys.argv) < 3:
        print("""
🔹 DevanLang CLI Usage 🔹

Usage:
  devan run <file.Om>
  devan compile <file.Om> --lang [python|php|auto]
""")
        return

    command = sys.argv[1].lower()
    file_path = sys.argv[2]

    if not file_path.endswith((".Om", ".OM", ".om")):
        print("❌ File must end with .Om")
        return

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    # Translate and encrypt before executing any command
    save_translated_and_encrypted(file_path)

    if command == "run":
        run_interpreter(file_path)
    elif command == "compile":
        lang = "auto"
        if len(sys.argv) == 5 and sys.argv[3] == "--lang":
            lang = sys.argv[4].lower()
        run_compiler(file_path, lang)
    else:
        print("❌ Unknown command. Use 'run' or 'compile'.")

if __name__ == "__main__":
    main()
