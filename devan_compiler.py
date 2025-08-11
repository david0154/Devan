import json
import os
import sys

class DevanCompiler:
    def __init__(self, filepath, output_lang="auto"):
        self.filepath = filepath
        self.output_lang = output_lang.lower()
        self.stdlib = self.load_stdlib()
        self.lines = self.read_file()
        self.translated_lines = []

    def load_stdlib(self):
        try:
            with open("devan_stdlib.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: 'devan_stdlib.json' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error decoding stdlib JSON: {e}")
            sys.exit(1)

    def read_file(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except UnicodeDecodeError:
            # 🔹 PATCH: read as raw bytes and decode with fallback instead of error
            with open(self.filepath, "rb") as f:
                raw_data = f.read()
            try:
                return raw_data.decode("utf-8", errors="replace").splitlines(True)
            except Exception as e:
                print(f"❌ Cannot read file '{self.filepath}': {e}")
                sys.exit(1)

    def detect_language(self):
        python_keywords = sum(1 for line in self.lines for word in self.stdlib if self.stdlib[word].get("python") in line)
        php_keywords = sum(1 for line in self.lines for word in self.stdlib if self.stdlib[word].get("php") in line)
        return "python" if python_keywords >= php_keywords else "php"

    def translate_line(self, line, lang):
        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def compile(self):
        lang = self.output_lang
        if lang not in {"python", "php", "auto"}:
            print(f"❌ Unknown language option: {lang}. Use 'python', 'php', or 'auto'.")
            sys.exit(1)

        if lang == "auto":
            lang = self.detect_language()

        for line in self.lines:
            translated = self.translate_line(line, lang)
            self.translated_lines.append(translated)

        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        output_ext = ".py" if lang == "python" else ".php"
        output_file = base_name + output_ext

        try:
            with open(output_file, "w", encoding="utf-8") as f:
                if lang == "php":
                    f.write("<?php\n")
                f.write("\n".join(self.translated_lines))
                if lang == "php":
                    f.write("\n?>")
            print(f"✅ Compiled to: {output_file} [{lang.upper()}]")
        except Exception as e:
            print(f"❌ Failed to write output file: {e}")

# CLI entry point
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python devan_compiler.py <file.Om> [--lang python|php|auto]")
        sys.exit(1)

    file = sys.argv[1]
    lang_flag = "auto"

    if len(sys.argv) == 4 and sys.argv[2] == "--lang":
        lang_flag = sys.argv[3]

    compiler = DevanCompiler(file, lang_flag)
    compiler.compile()
