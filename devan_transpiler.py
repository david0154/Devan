import json
import os
import sys

def load_stdlib():
    try:
        with open("devan_stdlib.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading devan_stdlib.json: {e}")
        sys.exit(1)

def build_reverse_stdlib(stdlib, lang="python"):
    reverse = {}
    for sanskrit, mapping in stdlib.items():
        if isinstance(mapping, dict) and lang in mapping:
            val = mapping[lang]
            if val:
                reverse[val] = sanskrit
    return reverse

def clean_line(line):
    return line.replace("।", "").replace("॥", "").replace(";", "").strip()

def translate_line_to_target(line, stdlib, lang="python"):
    line = clean_line(line)
    for sanskrit, mapping in stdlib.items():
        if isinstance(mapping, dict) and lang in mapping and mapping[lang]:
            line = line.replace(sanskrit, mapping[lang])
    return line

def translate_line_to_sanskrit(line, reverse_stdlib):
    line = clean_line(line)
    for eng, sanskrit in reverse_stdlib.items():
        line = line.replace(eng, sanskrit)
    return line

def detect_language(lines):
    for line in lines:
        if "php" in line.lower() or "चालय" in line:
            return "php"
    return "python"

def transpile(input_path, lang=None, reverse=False):
    if not os.path.isfile(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    stdlib = load_stdlib()

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if reverse:
        if not input_path.endswith((".py", ".php")):
            print("❌ Reverse mode only supports .py or .php files")
            sys.exit(1)

        lang = lang or ("php" if input_path.endswith(".php") else "python")
        reverse_stdlib = build_reverse_stdlib(stdlib, lang=lang)
        output_path = input_path.replace(".py", ".Om").replace(".php", ".Om")

        # Remove PHP tags for reverse translation
        if lang == "php":
            lines = [
                l for l in lines
                if not l.strip().startswith("<?") and not l.strip().startswith("?>")
            ]

        translated_lines = [
            translate_line_to_sanskrit(line, reverse_stdlib)
            for line in lines
        ]

    else:
        lang = lang or detect_language(lines)
        out_ext = ".py" if lang == "python" else ".php"
        output_path = (
            input_path.replace(".Om", out_ext)
                      .replace(".OM", out_ext)
                      .replace(".om", out_ext)
        )
        translated_lines = [
            translate_line_to_target(line, stdlib, lang=lang)
            for line in lines
        ]

    with open(output_path, "w", encoding="utf-8") as f:
        if not reverse and lang == "php":
            f.write("<?php\n")
        f.write("\n".join(translated_lines))
        if not reverse and lang == "php":
            f.write("\n?>")

    print(f"✅ Transpiled to {output_path}")

# CLI Entry
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""
🌀 DevanLang Bidirectional Transpiler

Usage:
  python devan_transpiler.py file.Om [--lang python|php]
  python devan_transpiler.py file.py --reverse
  python devan_transpiler.py file.php --reverse --lang php
""")
        sys.exit(1)

    input_file = sys.argv[1]
    lang = None
    reverse = "--reverse" in sys.argv

    if "--lang" in sys.argv:
        try:
            lang = sys.argv[sys.argv.index("--lang") + 1].lower()
            if lang not in ["python", "php"]:
                raise ValueError()
        except:
            print("❌ Invalid or missing value after --lang")
            sys.exit(1)

    transpile(input_file, lang=lang, reverse=reverse)
