import json
import os
import sys

# 📚 Load stdlib
def load_stdlib():
    try:
        with open("devan_stdlib.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading devan_stdlib.json: {e}")
        sys.exit(1)

# 🧼 Remove Sanskrit punctuation
def clean_line(line):
    return line.replace("।", "").replace("॥", "").replace(";", "").strip()

# 🈂️ Translate a single line
def translate_line(line, stdlib, lang):
    line = clean_line(line)
    for sanskrit, mapping in stdlib.items():
        if isinstance(mapping, dict) and lang in mapping and mapping[lang]:
            line = line.replace(sanskrit, mapping[lang])
    return line

# 🧠 Language detection: returns 'python' or 'php'
def detect_language(code_lines):
    for line in code_lines:
        if "php" in line.lower() or "चालय" in line:
            return "php"
    return "python"

# 🔁 Transpile .Om to .py or .php
def transpile(input_path, output_lang=None):
    if not input_path.lower().endswith(".om"):
        print("❌ File must end with .Om")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    stdlib = load_stdlib()

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lang = output_lang or detect_language(lines)
    out_ext = ".py" if lang == "python" else ".php"
    output_path = input_path.replace(".Om", out_ext).replace(".OM", out_ext).replace(".om", out_ext)

    translated_lines = []
    for line in lines:
        translated = translate_line(line, stdlib, lang)
        translated_lines.append(translated)

    with open(output_path, "w", encoding="utf-8") as f:
        if lang == "php":
            f.write("<?php\n")  # PHP file start
        f.write("\n".join(translated_lines))
        if lang == "php":
            f.write("\n?>")  # PHP file end

    print(f"✅ Transpiled to {output_path}")

# 📜 CLI Usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🌀 DevanLang Transpiler

Usage:
  python devan_transpiler.py file.Om [--lang python|php]

Example:
  python devan_transpiler.py hello.Om
  python devan_transpiler.py hello.Om --lang php
""")
        sys.exit(1)

    input_file = sys.argv[1]
    lang = None
    if "--lang" in sys.argv:
        try:
            lang = sys.argv[sys.argv.index("--lang") + 1].lower()
            if lang not in ["python", "php"]:
                raise ValueError()
        except:
            print("❌ Invalid or missing language after --lang")
            sys.exit(1)

    transpile(input_file, lang)
