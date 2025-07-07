# devan_php_runner.py
import subprocess

def run_php_code(code: str):
    try:
        result = subprocess.run(["php", "-r", code], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ PHP Error:\n{result.stderr}")
        else:
            print(result.stdout)
    except FileNotFoundError:
        print("❌ PHP CLI not found. Please install PHP and ensure 'php' command is available.")
    except Exception as e:
        print(f"❌ PHP Execution Failed: {e}")

def run_php_file(file_path: str):
    try:
        result = subprocess.run(["php", file_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ PHP Error:\n{result.stderr}")
        else:
            print(result.stdout)
    except Exception as e:
        print(f"❌ Error running PHP file: {e}")

# Example direct usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python devan_php_runner.py '<php_code>'")
    else:
        run_php_code(sys.argv[1])
