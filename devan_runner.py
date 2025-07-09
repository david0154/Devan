import sys
import subprocess
import os
import chardet
import time
from utils.translator import translate_to_sanskrit
from utils.encryptor import encrypt

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw = f.read(2048)
    return chardet.detect(raw)['encoding'] or 'utf-8'

def is_safe_for_text(file_path):
    try:
        encoding = detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False

def save_translated_and_encrypted(file_path, skip_translate=False, skip_encrypt=False):
    encoding = detect_encoding(file_path)

    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        original_code = f.read()

    # 🔐 Encrypt original .om file
    if not skip_encrypt:
        encrypted_path = file_path + '.enc'
        with open(encrypted_path, 'wb') as f:
            f.write(encrypt(original_code))
        print(f"🔐 Encrypted copy saved to: {encrypted_path}")

    # 🧠 Translate to Sanskrit and encrypt
    if not skip_translate:
        try:
            if any(kw in original_code for kw in ["from", "def", "print", "import"]):
                sanskrit_code = translate_to_sanskrit(original_code)
                sanskrit_path = file_path.replace('.om', '_sa.om').replace('.OM', '_sa.OM').replace('.Om', '_sa.Om')
                with open(sanskrit_path, 'wb') as f:
                    f.write(encrypt(sanskrit_code))
                print(f"🧠 Sanskrit translation encrypted to: {sanskrit_path}")
            else:
                print("🌿 Detected Sanskrit-style syntax. Skipping retranslation.")
        except Exception as e:
            print(f"⚠️ Sanskrit translation failed: {e}")

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
    start = time.time()

    if len(sys.argv) < 3:
        print("""
🔹 DevanLang CLI Usage 🔹

Usage:
  devan run <file.Om> [--no-translate] [--no-encrypt]
  devan compile <file.Om> --lang [python|php|auto] [--no-translate] [--no-encrypt]
""")
        sys.exit(1)

    command = sys.argv[1].lower()
    file_path = sys.argv[2]

    skip_translate = "--no-translate" in sys.argv
    skip_encrypt = "--no-encrypt" in sys.argv

    # Normalize extension comparison
    file_path_lower = file_path.lower()

    if not file_path_lower.endswith(".om"):
        print("❌ File must end with .Om")
        sys.exit(1)

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    if file_path_lower.endswith(".enc") or file_path_lower.endswith("_sa.om"):
        print("❌ Cannot run or compile an encrypted or Sanskrit-translated file. Use the original .Om file.")
        sys.exit(1)

    if not is_safe_for_text(file_path):
        print(f"❌ Cannot read '{file_path}' as text. It may be encrypted or corrupted.")
        sys.exit(1)

    save_translated_and_encrypted(file_path, skip_translate, skip_encrypt)

    if command == "run":
        run_interpreter(file_path)
    elif command == "compile":
        lang = "auto"
        if "--lang" in sys.argv:
            try:
                lang = sys.argv[sys.argv.index("--lang") + 1].lower()
            except IndexError:
                print("❌ Missing value after '--lang' flag.")
                sys.exit(1)
        run_compiler(file_path, lang)
    else:
        print("❌ Unknown command. Use 'run' or 'compile'.")
        sys.exit(1)

    print(f"⏱️ Done in {time.time() - start:.2f}s")

if __name__ == "__main__":
    main()
