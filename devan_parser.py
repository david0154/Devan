import json
import os
import sys
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
        """Load standard library mappings from JSON."""
        try:
            with open("devan_stdlib.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: 'devan_stdlib.json' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in 'devan_stdlib.json' → {e}")
            sys.exit(1)

    def read_file(self):
        """Read source file into a list of lines."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except UnicodeDecodeError:
            print(f"❌ Error: Unable to read '{self.filepath}' as UTF-8. Is it encrypted?")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error reading '{self.filepath}': {e}")
            sys.exit(1)

    def translate_line(self, line, lang="python"):
        """Replace Devanagari keywords with target language equivalents."""
        line = line.strip().replace("।", "").replace("॥", "").replace(";", "")
        for sanskrit, mapping in self.stdlib.items():
            if isinstance(mapping, dict) and lang in mapping and mapping[lang]:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def detect_php_block(self, line):
        """Detect if a line contains PHP code."""
        return "चालय" in line or "php" in line.lower()

    def process_lines(self):
        """Process each line: translate to Python or store PHP for execution."""
        for line in self.lines:
            if self.detect_php_block(line):
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and "php" in parts[1].lower():
                    php_raw = parts[1].split("php", 1)[-1].strip().strip('"').strip("'")
                    self.php_blocks.append(php_raw)
                    continue
            self.translated_lines.append(self.translate_line(line, lang="python"))

    def execute_python(self):
        """Execute translated Python code."""
        code = "\n".join(self.translated_lines)
        print("🐍 Executing Python Code:\n" + "-" * 40)
        try:
            exec(code, {})
        except Exception as e:
            print(f"⚠️ Python Execution Error: {e}")

    def execute_php_blocks(self):
        """Execute stored PHP code blocks."""
        for php_code in self.php_blocks:
            try:
                print(f"🐘 Executing PHP Code: {php_code}")
                devan_php_runner.run_php_code(php_code)
            except Exception as e:
                print(f"⚠️ PHP Execution Error: {e}")

    def run(self):
        """Main interpreter flow."""
        self.process_lines()
        if self.translated_lines:
            self.execute_python()
        if self.php_blocks:
            self.execute_php_blocks()

# 📜 CLI Entry
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python devan_parser.py <file.Om>")
        sys.exit(1)

    file = sys.argv[1]

    if not file.endswith((".Om", ".OM", ".om")):
        print("❌ Error: File must have a .Om extension.")
        sys.exit(1)

    if not os.path.isfile(file):
        print(f"❌ Error: File not found: {file}")
        sys.exit(1)

    interpreter = DevanInterpreter(file)
    interpreter.run()
