from invoke import task
import os
import signal
import psutil
import subprocess

PID_FILE = "services.pid"  # File to store PIDs


@task
def start(ctx):
    """Start all services and save their PIDs."""
    processes = {
        "mqtt": "python -m src.local_data_process_service.app",
        "celery": "celery --app src.local_data_process_service.capp worker --loglevel=info",
        "redis": "docker start redis-db"
    }

    pids = {}

    for name, cmd in processes.items():
        process = subprocess.Popen(cmd, shell=True)
        pids[name] = process.pid  # Get PID

    # Save PIDs to file
    with open(PID_FILE, "w") as f:
        for name, pid in pids.items():
            f.write(f"{name}:{pid}\n")

    print("✅ All services started.")


@task
def stop(ctx):
    """Stop all running services."""
    if not os.path.exists(PID_FILE):
        print("❌ No running services found.")
        return

    with open(PID_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        name, pid = line.strip().split(":")
        pid = int(pid)

        if name == "redis":
            # Stop redis-db using docker
            subprocess.run("docker stop redis-db", shell=True, check=True)
            print(f"🛑 Stopped {name} (via Docker)")
        elif psutil.pid_exists(pid):
            if name == "celery":
                celery_process = psutil.Process(pid)
                celery_process.terminate()
                celery_process.wait()
                print(f"🛑 Stopped {name} (PID {pid})")
            else:
                os.kill(pid, signal.SIGTERM)
                print(f"🛑 Stopped {name} (PID {pid})")
        else:
            print(f"⚠️ Process {name} (PID {pid}) not found.")

    os.remove(PID_FILE)
    print("✅ All services stopped.")