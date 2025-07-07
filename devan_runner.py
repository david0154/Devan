# devan_runner.py
import sys
import subprocess

def run_interpreter(file_path):
    try:
        subprocess.run(["python", "devan_parser.py", file_path])
    except Exception as e:
        print(f"❌ Interpreter failed: {e}")

def run_compiler(file_path, lang="auto"):
    try:
        subprocess.run(["python", "devan_compiler.py", file_path, "--lang", lang])
    except Exception as e:
        print(f"❌ Compilation failed: {e}")

def main():
    if len(sys.argv) < 3:
        print("❌ Usage:\n  devan run <file.Om>\n  devan compile <file.Om> --lang [python|php|auto]")
        return

    command = sys.argv[1]
    file_path = sys.argv[2]

    if not file_path.endswith((".Om", ".OM", ".om")):
        print("❌ File must end with .Om")
        return

    if command == "run":
        run_interpreter(file_path)

    elif command == "compile":
        lang = "auto"
        if len(sys.argv) == 5 and sys.argv[3] == "--lang":
            lang = sys.argv[4].lower()
        run_compiler(file_path, lang)

    else:
        print("❌ Unknown command. Use 'run' or 'compile'.")

if __name__ == "__main__":
    main()
