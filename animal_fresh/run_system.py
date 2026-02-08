import subprocess
import sys
import time
import os
import argparse

def run_system(backend_only=False, frontend_only=False):
    print("🚀 Starting Veterinary AI System (Local Mode)...")
    
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

    try:
        # 1. Start Backend (FastAPI)
        if not frontend_only:
            print(f"🔹 Launching Backend API ({backend_script})...")
            # Using sys.executable ensures we use the same python interpreter (the venv)
            backend_process = subprocess.Popen(
                [sys.executable, backend_script],
                cwd=base_dir,  # Run inside animal_fresh
                env=os.environ.copy()
            )
            processes.append(backend_process)
            
            # Wait a moment for backend to initialize if running both
            if not backend_only:
                time.sleep(3)
        
        # 2. Start Frontend (Streamlit)
        if not backend_only:
            target_dashboard = dashboard_files["main"] # Default
            
            # Check if specific dashboard requested via args (future enhancement)
            # For now, default to main app.
            
            print(f"🔹 Launching Frontend Dashboard ({target_dashboard})...")
            # Note: Streamlit options like --server.port must come BEFORE the script name
            frontend_cmd = [
                sys.executable, "-m", "streamlit", "run", 
                "--server.port=8501", 
                target_dashboard
            ]
            
            frontend_process = subprocess.Popen(
                frontend_cmd,
                cwd=base_dir, # Run inside animal_fresh
                env=os.environ.copy()
            )
            processes.append(frontend_process)
        
        print("\n✅ System is Running!")
        if not frontend_only:
            print("   - API: http://localhost:8000")
        if not backend_only:
            print("   - Dashboard Portal: http://localhost:8501 (Use Sidebar to navigate)")
        print("\nPress Ctrl+C to stop the system.")
        
        # Keep the script running to monitor processes
        for p in processes:
            p.wait()
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        print("✅ System stopped successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Veterinary AI System locally.")
    parser.add_argument("--backend", action="store_true", help="Run only the Backend API")
    parser.add_argument("--frontend", action="store_true", help="Run only the Frontend Dashboard")
    args = parser.parse_args()
    
    run_system(backend_only=args.backend, frontend_only=args.frontend)
