# devan_parser.py
import json
import subprocess
import os
import devan_installer
devan_installer.check_and_install()

class DevanInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.stdlib = self.load_stdlib()
        self.lines = self.read_file()
        self.translated_lines = []

    def load_stdlib(self):
        with open("devan_stdlib.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def read_file(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.readlines()

    def translate_line(self, line, lang="python"):
        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def is_php_block(self, line):
        return "php" in line.lower() or "चालय" in line

    def execute_python(self):
        code = "\n".join(self.translated_lines)
        try:
            exec(code, globals())
        except Exception as e:
            print(f"⚠️ Python Execution Error: {e}")

    def execute_php(self, code):
        try:
            result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"⚠️ PHP Execution Error: {e}")

    def run(self):
        php_blocks = []

        for line in self.lines:
            if "चालय" in line:
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and "php" in parts[1].lower():
                    code_line = parts[1].split("php", 1)[-1].strip().strip('"').strip("'")
                    php_blocks.append(code_line)
                    continue

            translated = self.translate_line(line, "python")
            self.translated_lines.append(translated)

        # Execute translated Python code
        self.execute_python()

        # Execute any PHP code blocks
        for php_code in php_blocks:
            self.execute_php(php_code)

# CLI-style usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Usage: python devan_parser.py <file.Om>")
    else:
        file = sys.argv[1]
        if not file.endswith((".Om", ".OM", ".om")):
            print("❌ File must end with .Om")
        else:
            interpreter = DevanInterpreter(file)
            interpreter.run()
