import subprocess
import sys
import time
import os
import argparse

import signal

def run_system(backend_only=False, frontend_only=False, is_docker=False):
    print("🚀 Starting Veterinary AI System...")
    if is_docker:
        print("🐳 Running in Docker Mode (All interfaces 0.0.0.0)")
    
    # Determined base directory to ensure CWD is correct regardless of where script is run from
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define paths
    backend_script = os.path.join(base_dir, "simple_api.py")
    frontend_script = os.path.join(base_dir, "app_dashboard.py")
    
    # Dashboard scripts
    dashboard_files = {
        "admin": os.path.join(base_dir, "dashboard_admin.py"),
        "analytics": os.path.join(base_dir, "dashboard_analytics.py"),
        "species": os.path.join(base_dir, "dashboard_species.py"),
        "executive": os.path.join(base_dir, "dashboard_executive.py"),
        "main": frontend_script
    }

    processes = []

    def shutdown_handler(signum, frame):
        print("\n🛑 Signal received, stopping system...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        print("✅ System stopped successfully.")
        sys.exit(0)

    # Register signals for Docker/Process management
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        # 1. Start Backend (FastAPI)
        if not frontend_only:
            print(f"🔹 Launching Backend API ({backend_script})...")
            # Using sys.executable ensures we use the same python interpreter
            backend_cmd = [sys.executable, backend_script]
            if is_docker:
                backend_cmd.extend(["--host", "0.0.0.0"]) # Pass host to uvicorn in simple_api.py if supported
            
            # Simple API handles uvicorn.run internally. Let's ensure it handles args or defaults.
            # Actually simple_api.py lines 93-97 uses uvicorn.run(app, host="0.0.0.0", port=8000)
            # So it's already Docker-ready for host.
            
            backend_process = subprocess.Popen(
                backend_cmd,
                cwd=base_dir,
                env=os.environ.copy()
            )
            processes.append(backend_process)
            
            # Wait a moment for backend to initialize
            if not backend_only:
                time.sleep(3)
        
        # 2. Start Frontend (Streamlit)
        if not backend_only:
            target_dashboard = dashboard_files["main"]
            
            print(f"🔹 Launching Frontend Dashboard ({target_dashboard})...")
            # Streamlit options
            frontend_cmd = [
                sys.executable, "-m", "streamlit", "run", 
                "--server.port=8501", 
                f"--server.address={'0.0.0.0' if is_docker else 'localhost'}",
                "--browser.gatherUsageStats=false",
                target_dashboard
            ]
            
            frontend_process = subprocess.Popen(
                frontend_cmd,
                cwd=base_dir,
                env=os.environ.copy()
            )
            processes.append(frontend_process)
        
        print("\n✅ System is Running!")
        if not frontend_only:
            print(f"   - API: http://{'0.0.0.0' if is_docker else 'localhost'}:8000")
        if not backend_only:
            print(f"   - Dashboard Portal: http://{'0.0.0.0' if is_docker else 'localhost'}:8501")
        
        if not is_docker:
            print("\nPress Ctrl+C to stop the system.")
        
        # Keep the script running to monitor processes
        while True:
            for p in processes:
                if p.poll() is not None:
                    print(f"❌ Process {p.pid} exited with code {p.returncode}")
                    shutdown_handler(None, None)
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        shutdown_handler(None, None)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Veterinary AI System.")
    parser.add_argument("--backend", action="store_true", help="Run only the Backend API")
    parser.add_argument("--frontend", action="store_true", help="Run only the Frontend Dashboard")
    parser.add_argument("--docker", action="store_true", help="Run in Docker mode (0.0.0.0)")
    args = parser.parse_args()
    
    run_system(backend_only=args.backend, frontend_only=args.frontend, is_docker=args.docker)
