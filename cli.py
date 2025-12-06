import os
import shutil
import subprocess
import sys
import time
import threading
from pathlib import Path
from typing import Optional
from datetime import datetime

# ดึง logic การแปลงร่างจาก Level ที่แล้วมาใช้
import compiler
import typer
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ==============================================
# 🎨 Console Styling
# ==============================================
class Style:
    """ANSI color codes for terminal styling"""
    # Colors
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Reset
    RESET = "\033[0m"


def log_info(msg: str):
    """Log info message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.GRAY}{timestamp}{Style.RESET}  {Style.CYAN}ℹ{Style.RESET}  {msg}")


def log_success(msg: str):
    """Log success message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.GRAY}{timestamp}{Style.RESET}  {Style.GREEN}✓{Style.RESET}  {msg}")


def log_warning(msg: str):
    """Log warning message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.GRAY}{timestamp}{Style.RESET}  {Style.YELLOW}⚠{Style.RESET}  {msg}")


def log_error(msg: str):
    """Log error message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.GRAY}{timestamp}{Style.RESET}  {Style.RED}✗{Style.RESET}  {msg}")


def log_server(msg: str):
    """Log server message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Style.GRAY}{timestamp}{Style.RESET}  {Style.PURPLE}▸{Style.RESET}  {msg}")


def print_banner():
    """Print Dukpyra banner"""
    banner = f"""
{Style.PURPLE}{Style.BOLD}
    ╔══════════════════════════════════════════╗
    ║                                          ║
    ║      🔮  D U K P Y R A                   ║
    ║              Framework                   ║
    ║                                          ║
    ╚══════════════════════════════════════════╝
{Style.RESET}"""
    print(banner)


def print_server_ready(port: int, https: bool = False):
    """Print server ready message"""
    protocol = "https" if https else "http"
    url = f"{protocol}://localhost:{port}"
    
    print()
    print(f"  {Style.GREEN}{Style.BOLD}➜{Style.RESET}  {Style.BOLD}Server running at:{Style.RESET}  {Style.CYAN}{Style.UNDERLINE}{url}{Style.RESET}")
    print(f"  {Style.GRAY}➜  Press {Style.BOLD}Ctrl+C{Style.RESET}{Style.GRAY} to stop{Style.RESET}")
    print()


# ==============================================
# CLI Config
# ==============================================
app = typer.Typer(
    name="dukpyra",
    help="🔮 Dukpyra - Framework",
    add_completion=False,
)

SERVICES_DIR = Path("services")
PROJECT_NAME = "DukpyraApp"
DEFAULT_PORT = 5000

# Global state
dotnet_process = None
current_port = DEFAULT_PORT
server_ready = False


def ensure_services_dir():
    """สร้าง services/ directory ถ้ายังไม่มี"""
    if not SERVICES_DIR.exists():
        log_info(f"Creating {Style.BOLD}services/{Style.RESET} directory...")
        SERVICES_DIR.mkdir(parents=True, exist_ok=True)
    return SERVICES_DIR


def ensure_dotnet_project():
    """สร้าง .NET project ใน services/ ถ้ายังไม่มี"""
    csproj_path = SERVICES_DIR / f"{PROJECT_NAME}.csproj"
    
    if not csproj_path.exists():
        log_info(f"Initializing .NET project: {Style.BOLD}{PROJECT_NAME}{Style.RESET}")
        
        result = subprocess.run(
            ["dotnet", "new", "web", "-n", PROJECT_NAME, "-o", str(SERVICES_DIR), "--force"],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            log_error(f"Failed to create .NET project")
            return False
        
        # ลบ Program.cs ที่ dotnet สร้างมา
        default_program = SERVICES_DIR / "Program.cs"
        if default_program.exists():
            default_program.unlink()
        
        log_success(f".NET project created")
    
    return True


@app.command()
def init():
    """Initialize a new Dukpyra project"""
    print_banner()
    ensure_services_dir()
    ensure_dotnet_project()
    log_success("Project initialized successfully! 🚀")
    print(f"\nExample usage:\n  {Style.CYAN}dukpyra dev{Style.RESET}\n")


@app.command()
def build():
    """Compile Python to C#"""
    log_info("Compiling...")
    try:
        compiler.dukpyra_compile()
        log_success("Compilation successful!")
    except Exception as e:
        log_error(f"Compilation failed: {e}")
        raise typer.Exit(code=1)


@app.command()
def run(
    port: int = typer.Option(DEFAULT_PORT, help="Port to run the server on"),
    https: bool = typer.Option(False, help="Enable HTTPS"),
):
    """Run the production server"""
    if not (SERVICES_DIR / f"{PROJECT_NAME}.csproj").exists():
        log_error("Project not initialized. Run 'dukpyra init' first.")
        raise typer.Exit(code=1)
        
    log_server(f"Starting production server on port {port}...")
    
    protocol = "https" if https else "http"
    try:
        subprocess.run(
            ["dotnet", "run", "--project", f"services/{PROJECT_NAME}.csproj", "--urls", f"{protocol}://localhost:{port}"],
            check=True
        )
    except KeyboardInterrupt:
        print()
        log_info("Server stopped.")
    except subprocess.CalledProcessError:
        log_error("Failed to run server.")
        raise typer.Exit(code=1)


class ReloadHandler(FileSystemEventHandler):
    """Watch files and trigger recompile + restart"""
    
    def __init__(self, restart_callback):
        super().__init__()
        self.restart_callback = restart_callback
        self._debounce_timer = None
    
    def on_modified(self, event):
        # Watch both input.py and generated C# files
        if event.src_path.endswith("input.py"):
            log_info("Detected change in input.py")
            try:
                compiler.dukpyra_compile()
                log_success("Re-compiled successfully!")
                self._trigger_restart()
            except Exception as e:
                log_error(f"Re-compilation failed: {e}")
        elif event.src_path.endswith(".cs"):
            log_info("Detected change in C# files")
            self._trigger_restart()
    
    def _trigger_restart(self):
        """Debounced restart to avoid multiple restarts"""
        if self._debounce_timer:
            self._debounce_timer.cancel()
        self._debounce_timer = threading.Timer(0.5, self.restart_callback)
        self._debounce_timer.start()


class DotnetRunner:
    """Manages dotnet run process with restart capability"""
    
    def __init__(self, port: int, https: bool = False):
        self.port = port
        self.https = https
        self.process = None
        self._lock = threading.Lock()
    
    def start(self):
        """Start the dotnet server"""
        with self._lock:
            if self.process:
                self.stop()
            
            protocol = "https" if self.https else "http"
            cmd = [
                "dotnet", "run",
                "--project", f"services/{PROJECT_NAME}.csproj",
                "--urls", f"{protocol}://localhost:{self.port}"
            ]
            
            self.process = subprocess.Popen(cmd)
            log_info("Starting .NET server...")
    
    def stop(self):
        """Stop the dotnet server"""
        with self._lock:
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                self.process = None
    
    def restart(self):
        """Restart the dotnet server"""
        log_info("Restarting .NET server...")
        self.stop()
        time.sleep(0.5)  # Brief pause before restart
        self.start()
    
    def wait(self):
        """Wait for process to complete"""
        if self.process:
            self.process.wait()


@app.command()
def dev(
    port: int = typer.Option(DEFAULT_PORT, help="Port to run the server on"),
    https: bool = typer.Option(False, help="Enable HTTPS"),
):
    """Run development server with hot reload"""
    print_banner()
    
    # 1. Build first
    build()
    
    # 2. Create dotnet runner
    runner = DotnetRunner(port, https)
    
    # 3. Setup Watchdog for input.py -> compile -> restart
    event_handler = ReloadHandler(restart_callback=runner.restart)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.schedule(event_handler, path="services", recursive=True)
    observer.start()
    
    log_info("Watching 'input.py' and 'services/' for changes...")
    
    print_server_ready(port, https)
    
    # 4. Start dotnet run (not watch!)
    runner.start()
    
    try:
        # Keep running until Ctrl+C
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        runner.stop()
        observer.stop()
        observer.join()
        print()
        log_info("Development server stopped.")


@app.command()
def clean():
    """Clean generated files"""
    if SERVICES_DIR.exists():
        shutil.rmtree(SERVICES_DIR)
        log_success("Cleaned services/ directory")
    else:
        log_info("Nothing to clean")


@app.command()
def restart():
    """Rebuild and restart (use during dev server)"""
    log_info("Rebuilding...")
    try:
        compiler.dukpyra_compile()
        log_success("Rebuild complete! Server will restart automatically if running in dev mode.")
    except Exception as e:
        log_error(f"Rebuild failed: {e}")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Show version"""
    # Should probably read from pyproject.toml but hardcoding for now as per README
    print(f"Dukpyra v0.00001")


if __name__ == "__main__":
    app()
