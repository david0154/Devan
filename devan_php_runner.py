# devan_php_runner.py
import subprocess
import os

def run_php_code(code: str):
    try:
        result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ PHP Error:\n{result.stderr}")
        else:
            print(f"🧾 PHP Output:\n{result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ PHP CLI not found. Please install PHP and ensure 'php' is in your system PATH.")
    except Exception as e:
        print(f"❌ PHP Execution Failed: {e}")

def run_php_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"❌ PHP file not found: {file_path}")
        return

    try:
        result = subprocess.run(["php", file_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ PHP Error:\n{result.stderr}")
        else:
            print(f"🧾 PHP Output:\n{result.stdout.strip()}")
    except Exception as e:
        print(f"❌ Error running PHP file: {e}")

# Example CLI usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("📌 Usage:")
        print("  python devan_php_runner.py '<php_code>'")
        print("  python devan_php_runner.py file:<path_to_php_file>")
    else:
        arg = sys.argv[1]
        if arg.startswith("file:"):
            run_php_file(arg[5:])
        else:
            run_php_code(arg)
