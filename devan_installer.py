# devan_installer.py
import subprocess
import sys
import importlib

# List of essential packages required by Devan
REQUIRED_PACKAGES = ["numpy", "pandas", "requests"]

def is_installed(package_name):
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name):
    print(f"📦 Installing: {package_name}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])

def check_and_install():
    print("🔍 Checking required packages...")
    for package in REQUIRED_PACKAGES:
        if not is_installed(package):
            try:
                install_package(package)
            except Exception as e:
                print(f"❌ Failed to install {package}: {e}")
        else:
            print(f"✅ {package} already installed.")

if __name__ == "__main__":
    check_and_install()
