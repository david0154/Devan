# devan_parser.py
import json
import subprocess
import os
import devan_installer
import devan_php_runner

# Ensure required libraries are installed
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
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.readlines()

    def translate_line(self, line, lang="python"):
        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping and mapping[lang]:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def detect_php_block(self, line):
        return "चालय" in line or "php" in line.lower()

    def process_lines(self):
        for line in self.lines:
            if self.detect_php_block(line):
                # Extract inline PHP code from चालय = "php echo ...";
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and "php" in parts[1].lower():
                    php_raw = parts[1].split("php", 1)[-1].strip().strip('"').strip("'")
                    self.php_blocks.append(php_raw)
                    continue
            # Otherwise treat as Python code
            translated = self.translate_line(line, lang="python")
            self.translated_lines.append(translated)

    def execute_python(self):
        code = "\n".join(self.translated_lines)
        try:
            exec(code, globals())
        except Exception as e:
            print(f"⚠️ Python Execution Error: {e}")

    def execute_php_blocks(self):
        for php_code in self.php_blocks:
            try:
                devan_php_runner.run_php_code(php_code)
            except Exception as e:
                print(f"⚠️ PHP Execution Error: {e}")

    def run(self):
        self.process_lines()
        if self.translated_lines:
            self.execute_python()
        if self.php_blocks:
            self.execute_php_blocks()

# CLI Entry
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("❌ Usage: python devan_parser.py <file.Om>")
    else:
        file = sys.argv[1]
        if not file.endswith((".Om", ".OM", ".om")):
            print("❌ File must end with .Om")
        elif not os.path.isfile(file):
            print(f"❌ File not found: {file}")
        else:
            interpreter = DevanInterpreter(file)
            interpreter.run()
