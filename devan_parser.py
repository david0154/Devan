import json
import subprocess
import os
from devan_lexer import DevanLexer
import devan_installer
import devan_php_runner

# 📦 Ensure dependencies are ready
devan_installer.check_and_install()

class DevanInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.stdlib = self.load_stdlib()
        self.patch_runtime_translations()  # 🛠 Inject runtime fixes
        self.code = self.read_code()
        self.translated_lines = []

    def load_stdlib(self):
        try:
            with open("devan_stdlib.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Error: 'devan_stdlib.json' not found.")
            exit(1)
        except json.JSONDecodeError as e:
<<<<<<< HEAD
            print(f"❌ Error loading stdlib JSON: {e}")
            exit(1)

    def patch_runtime_translations(self):
        patch = {
            "write": {"python": "print", "php": "echo"},
            "inputं": {"python": "input", "php": "readline"},
            "mergeतु": {"python": "append", "php": ""},
            "मुख्यं": {"python": "def", "php": "function"},
            "आरभत": {"python": ":", "php": ":"},
            "taskं": {"python": "task", "php": "task"},
            "विरम": {"python": "break", "php": "break"},
            "else if": {"python": "elif", "php": "elseif"},
            "intं": {"python": "int", "php": "intval"},
            "list.लम्बं()": {"python": "len(list)", "php": "count($list)"},
            "लम्बं": {"python": "len", "php": "count"},
            "निष्कासय": {"python": "pop", "php": "unset"},
            "प्रत्येकं": {"python": "for", "php": "foreach"},
            "चक्रं": {"python": "while", "php": "while"},
            "समाप्तं": {"python": "", "php": ""},
        }
        self.stdlib.update(patch)

    def read_code(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            print(f"❌ Cannot read '{self.filepath}' as UTF-8. Is it encrypted?")
            exit(1)
        except Exception as e:
            print(f"❌ Error reading file: {e}")
=======
            print(f"❌ Error decoding JSON: {e}")
            exit(1)

    def read_file(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return f.readlines()
        except UnicodeDecodeError:
            print(f"❌ Cannot read '{self.filepath}': Not a valid UTF-8 file. Is it encrypted?")
>>>>>>> 10b93076c1cb298208de5f8bcefd42bd2eb6971c
            exit(1)

    def translate_line(self, line, lang="python"):
        # 🧼 Clean punctuation
        line = line.replace("।", "").replace("॥", "").replace(";", "")

        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping and mapping[lang]:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def is_php_block(self, line):
        return "php" in line.lower() or "चालय" in line

<<<<<<< HEAD
    def run_php_block(self, code_line):
        try:
            code = code_line.split("php", 1)[-1].strip().strip('"').strip("'")
            result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(f"⚠️ PHP stderr: {result.stderr.strip()}")
        except Exception as e:
            print(f"⚠️ PHP Error: {e}")
=======
    def process_lines(self):
        for line in self.lines:
            if self.detect_php_block(line):
                parts = line.strip().split("=", 1)
                if len(parts) == 2 and "php" in parts[1].lower():
                    php_raw = parts[1].split("php", 1)[-1].strip().strip('"').strip("'")
                    self.php_blocks.append(php_raw)
                    continue
            self.translated_lines.append(self.translate_line(line, lang="python"))
>>>>>>> 10b93076c1cb298208de5f8bcefd42bd2eb6971c

    def execute_python_code(self):
        code = "\n".join(self.translated_lines)
        try:
            exec(code, globals())
        except Exception as e:
            print("⚠️ Python Execution Error:")
            print("--- Translated code ---")
            print(code)
            print(f"➡️ {e}")

    def run(self):
        lexer = DevanLexer(self.code)
        _ = lexer.tokenize()  # not used directly yet

<<<<<<< HEAD
        for line in self.code.splitlines():
            if self.is_php_block(line):
                self.run_php_block(line)
            else:
                translated = self.translate_line(line, lang="python")
                self.translated_lines.append(translated)

        if self.translated_lines:
            self.execute_python_code()

# 📜 CLI Entry
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("""
❌ Usage:
   python devan_interpreter.py <file.Om>
=======
# CLI Entry Point
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("""
❌ Usage:
  python devan_parser.py <file.Om>

📝 Note:
  Make sure you provide a clean, unencrypted source file. Encrypted or binary .Om files cannot be parsed directly.
>>>>>>> 10b93076c1cb298208de5f8bcefd42bd2eb6971c
""")
        exit(1)

    file = sys.argv[1]

    if not file.endswith((".Om", ".OM", ".om")):
        print("❌ File must end with .Om")
        exit(1)

    if not os.path.isfile(file):
        print(f"❌ File not found: {file}")
        exit(1)

    interpreter = DevanInterpreter(file)
    interpreter.run()
<<<<<<< HEAD

=======
>>>>>>> 10b93076c1cb298208de5f8bcefd42bd2eb6971c
