# devan_interpreter.py

import json
import subprocess
from devan_lexer import DevanLexer
import devan_installer
import devan_php_runner

devan_installer.check_and_install()

class DevanInterpreter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.stdlib = self.load_stdlib()
        self.code = self.read_code()
        self.translated_lines = []

    def load_stdlib(self):
        with open("devan_stdlib.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def read_code(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return f.read()

    def translate_line(self, line, lang="python"):
        for sanskrit, mapping in self.stdlib.items():
            if lang in mapping and mapping[lang]:
                line = line.replace(sanskrit, mapping[lang])
        return line

    def is_php_block(self, line):
        return "php" in line.lower() or "चालय" in line

    def run_php_block(self, code_line):
        try:
            code = code_line.split("php", 1)[-1].strip().strip('"').strip("'")
            result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"⚠️ PHP Error: {e}")

    def execute_python_code(self):
        code = "\n".join(self.translated_lines)
        try:
            exec(code, globals())
        except Exception as e:
            print(f"⚠️ Python Execution Error: {e}")

    def run(self):
        lexer = DevanLexer(self.code)
        tokens = lexer.tokenize()

        lines = self.code.splitlines()
        for line in lines:
            if self.is_php_block(line):
                self.run_php_block(line)
            else:
                translated = self.translate_line(line, lang="python")
                self.translated_lines.append(translated)

        self.execute_python_code()

# CLI style runner
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("❌ Usage: python devan_interpreter.py <file.Om>")
    else:
        file = sys.argv[1]
        if not file.endswith((".Om", ".OM", ".om")):
            print("❌ File must end with .Om")
        else:
            interpreter = DevanInterpreter(file)
            interpreter.run()
