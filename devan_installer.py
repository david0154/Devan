# devan_installer.py
import subprocess
import sys
import importlib

# List of supported auto-install packages
REQUIRED_PACKAGES = ["numpy", "pandas", "requests"]

def is_installed(pkg):
    try:
        importlib.import_module(pkg)
        return True
    except ImportError:
        return False

def install_package(pkg):
    print(f"📦 Installing: {pkg}")
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

def check_and_install():
    for pkg in REQUIRED_PACKAGES:
        if not is_installed(pkg):
            try:
                install_package(pkg)
            except Exception as e:
                print(f"❌ Failed to install {pkg}: {e}")

if __name__ == "__main__":
    check_and_install()
