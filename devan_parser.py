import json
import subprocess
import os
import devan_installer
import devan_php_runner

# 📦 Ensure required libraries are installed
devan_installer.check_and_install()

class DevanInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.stdlib = self.load_stdlib()
        self.lines = self.read_file()
        self.translated_lines = []
        self.php_blocks = []

    def load_stdlib(self):
        try:
            with open("devan_stdlib.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Standard library file 'devan_stdlib.json' not found.")
            return {}

    def read_file(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except UnicodeDecodeError:
            print(f"❌ Unable to read '{self.filepath}'. Is it encrypted?")
            return []
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return []

    def translate_line(self, line, lang="python"):
        line = line.strip().replace("।", "").replace("॥", "").replace(";", "")
        for sanskrit, mapping in self.stdlib.items():
            if isinstance(mapping, dict) and lang in mapping and mapping[lang]:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def detect_php_block(self, line):
        return "चालय" in line or "php" in line.lower()

    def process_lines(self):
        for line in self.lines:
            if self.detect_php_block(line):
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and "php" in parts[1].lower():
                    php_raw = parts[1].split("php", 1)[-1].strip().strip('"').strip("'")
                    self.php_blocks.append(php_raw)
                    continue
            translated = self.translate_line(line, lang="python")
            self.translated_lines.append(translated)

    def execute_python(self):
        code = "\n".join(self.translated_lines)
        print("🔍 Executing Python:\n", code)
        try:
            exec(code, globals())
        except Exception as e:
            print(f"⚠️ Python Execution Error: {e}")

    def execute_php_blocks(self):
        for php_code in self.php_blocks:
            try:
                print(f"🔧 Running PHP: {php_code}")
                devan_php_runner.run_php_code(php_code)
            except Exception as e:
                print(f"⚠️ PHP Execution Error: {e}")

    def run(self):
        self.process_lines()
        if self.translated_lines:
            self.execute_python()
        if self.php_blocks:
            self.execute_php_blocks()

# 📜 CLI Entry
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Usage: python devan_parser.py <file.Om>")
        sys.exit(1)

    file = sys.argv[1]

    if not file.endswith((".Om", ".OM", ".om")):
        print("❌ File must end with .Om")
        sys.exit(1)

    if not os.path.isfile(file):
        print(f"❌ File not found: {file}")
        sys.exit(1)

    interpreter = DevanInterpreter(file)
    interpreter.run()
