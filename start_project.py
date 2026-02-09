import os
import subprocess
import sys
import argparse

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the virtual environment's python executable on Windows
    # Adjust if on Linux/Mac (bin/python)
    if os.name == 'nt':
        venv_python = os.path.join(base_dir, "animal_env", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(base_dir, "animal_env", "bin", "python")
        
    script_to_run = os.path.join(base_dir, "run_system.py")

    print(f"🚀 Bootstrapping Animal Fresh System...")
    
    if not os.path.exists(venv_python):
        print(f"❌ Error: Virtual environment python not found at {venv_python}")
        print("   Checking available pythons...")
        # Fallback to current python if venv python doesn't work, but warn user
        print(f"   Falling back to current system python: {sys.executable}")
        venv_python = sys.executable

    if not os.path.exists(script_to_run):
        print(f"❌ Error: System runner script not found at {script_to_run}")
        return

    print(f"🔹 Using Python Interpreter: {venv_python}")
    print(f"🔹 Running System Script: {script_to_run}")
    print("-" * 50)
    
    # Construct command to include any arguments passed to this script
    cmd = [venv_python, script_to_run] + sys.argv[1:]
    
    try:
        # Using call instead of check_call so we can handle return codes gracefully
        ret = subprocess.call(cmd)
        if ret != 0:
            print(f"\n⚠️ System process exited with code {ret}")
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
