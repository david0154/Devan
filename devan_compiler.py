# devan_compiler.py
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
        with open("devan_stdlib.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def read_file(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.readlines()

    def detect_language(self):
        python_keywords = sum(1 for line in self.lines for word in self.stdlib if self.stdlib[word]["python"] in line)
        php_keywords = sum(1 for line in self.lines for word in self.stdlib if self.stdlib[word]["php"] in line)
        return "python" if python_keywords >= php_keywords else "php"

    def translate_line(self, line, lang):
        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def compile(self):
        lang = self.output_lang
        if lang == "auto":
            lang = self.detect_language()

        for line in self.lines:
            translated = self.translate_line(line, lang)
            self.translated_lines.append(translated)

        base_name = os.path.splitext(os.path.basename(self.filepath))[0]
        output_ext = ".py" if lang == "python" else ".php"
        output_file = base_name + output_ext

        with open(output_file, "w", encoding="utf-8") as f:
            if lang == "php":
                f.write("<?php\n")
            f.write("\n".join(self.translated_lines))
            if lang == "php":
                f.write("\n?>")

        print(f"✅ Compiled: {output_file}")

# CLI usage
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
