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
    ║         Python → C# JIT Compiler         ║
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
    help="🔮 Dukpyra - Python to C# JIT Compiler",
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
    """Initialize a new Dukpyra project structure"""
    print_banner()
    log_info("Initializing Dukpyra project...")
    
    ensure_services_dir()
    if not ensure_dotnet_project():
        raise typer.Exit(code=1)
    
    input_file = Path("input.py")
    if not input_file.exists():
        input_file.write_text('''# input.py - Your API definitions go here
from typing import List, Optional


@app.get("/")
def index():
    return {"message": "Hello from Dukpyra! 🔮"}


@app.get("/health")
def health():
    return {"status": "ok"}
''')
        log_success("Created input.py template")
    
    print()
    log_success(f"{Style.BOLD}Project initialized!{Style.RESET}")
    print(f"\n  {Style.GRAY}Next steps:{Style.RESET}")
    print(f"  {Style.CYAN}1.{Style.RESET} Edit {Style.BOLD}input.py{Style.RESET} to define your API")
    print(f"  {Style.CYAN}2.{Style.RESET} Run {Style.BOLD}dukpyra dev{Style.RESET} to start development server")
    print()


@app.command()
def build():
    """Build the project: compile Python → C#"""
    log_info("Building project...")
    
    try:
        if not Path(compiler.INPUT_FILE).exists():
            log_error(f"{compiler.INPUT_FILE} not found!")
            log_info("Run 'dukpyra init' first")
            raise typer.Exit(code=1)
        
        ensure_services_dir()
        if not ensure_dotnet_project():
            raise typer.Exit(code=1)
        
        # Compile (suppress output)
        log_info("Compiling Python → C#...")
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            compiler.dukpyra_compile()
        
        log_success(f"{Style.BOLD}Build completed!{Style.RESET}")
        print(f"\n  {Style.GRAY}Output:{Style.RESET} {Style.CYAN}{compiler.OUTPUT_FILE}{Style.RESET}\n")
        
    except Exception as e:
        log_error(f"Build failed: {e}")
        raise typer.Exit(code=1)


def monitor_dotnet_output(process, port: int, https: bool):
    """Monitor .NET process output and show our styled messages"""
    global server_ready
    
    while process.poll() is None:
        line = process.stdout.readline()
        if line:
            line = line.strip()
            
            # Detect server ready (from .NET runtime)
            if "Now listening on:" in line:
                server_ready = True
                print_server_ready(port, https)
            
            # Detect dotnet watch build
            elif "dotnet watch" in line.lower():
                if "Build succeeded" in line:
                    log_success("Build succeeded")
                elif "Building" in line and ".csproj" in line:
                    log_info("Building .NET project...")
                elif "Hot reload" in line:
                    log_info("Hot reload enabled")
                elif "File changed:" in line:
                    log_info("File changed, reloading...")
            
            # Detect build errors
            elif "error CS" in line or "error:" in line.lower():
                # แสดง error แบบย่อ
                if "error CS" in line:
                    log_error(line.split(": error")[1] if ": error" in line else line)
                else:
                    log_error(line)
            
            # Detect build failure
            elif "build failed" in line.lower():
                log_error("Build failed!")
            
            # Debug: uncomment to see all output
            # else:
            #     print(f"{Style.DIM}{line}{Style.RESET}")


@app.command()
def run(
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="Port to run the server on"),
    https: bool = typer.Option(False, "--https", help="Enable HTTPS"),
):
    """Run the compiled .NET server"""
    csproj_path = SERVICES_DIR / f"{PROJECT_NAME}.csproj"
    
    if not csproj_path.exists():
        log_error("No .NET project found! Run 'dukpyra build' first.")
        raise typer.Exit(code=1)
    
    program_cs = SERVICES_DIR / "Program.cs"
    if not program_cs.exists():
        log_error("No Program.cs found! Run 'dukpyra build' first.")
        raise typer.Exit(code=1)
    
    protocol = "https" if https else "http"
    urls = f"{protocol}://localhost:{port}"
    
    log_info("Starting server...")
    
    env = os.environ.copy()
    env["ASPNETCORE_URLS"] = urls
    env["DOTNET_NOLOGO"] = "1"
    
    try:
        process = subprocess.Popen(
            ["dotnet", "run", "--no-launch-profile"],
            cwd=str(SERVICES_DIR),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        
        # Monitor output in background
        monitor_thread = threading.Thread(
            target=monitor_dotnet_output,
            args=(process, port, https),
            daemon=True,
        )
        monitor_thread.start()
        
        # Wait for process
        process.wait()
        
    except KeyboardInterrupt:
        print(f"\n{Style.GRAY}Shutting down...{Style.RESET}")
        if process:
            process.terminate()
        log_success("Server stopped")
    except Exception as e:
        log_error(f"Server error: {e}")
        raise typer.Exit(code=1)


def run_dotnet_background(port: int = DEFAULT_PORT, https: bool = False):
    """รัน .NET server แบบ background (สำหรับ dev mode)"""
    global dotnet_process, server_ready
    server_ready = False

    # Kill old process ถ้ามี
    if dotnet_process:
        log_info("Restarting server...")
        dotnet_process.terminate()
        try:
            dotnet_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            dotnet_process.kill()

    protocol = "https" if https else "http"
    urls = f"{protocol}://localhost:{port}"
    
    env = os.environ.copy()
    env["ASPNETCORE_URLS"] = urls
    env["DOTNET_NOLOGO"] = "1"
    
    dotnet_process = subprocess.Popen(
        ["dotnet", "run", "--no-launch-profile"],
        cwd=str(SERVICES_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    
    # Monitor output in background
    monitor_thread = threading.Thread(
        target=monitor_dotnet_output,
        args=(dotnet_process, port, https),
        daemon=True,
    )
    monitor_thread.start()


def compile_only():
    """Compile input.py -> Program.cs (without restarting server)"""
    import io
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        compiler.dukpyra_compile()


def run_dotnet_watch(port: int = DEFAULT_PORT, https: bool = False):
    """รัน dotnet watch run (hot reload built-in)"""
    global dotnet_process, server_ready
    server_ready = False

    protocol = "https" if https else "http"
    urls = f"{protocol}://localhost:{port}"
    
    env = os.environ.copy()
    env["ASPNETCORE_URLS"] = urls
    env["DOTNET_NOLOGO"] = "1"
    env["DOTNET_WATCH_SUPPRESS_EMOJIS"] = "1"
    
    # ส่ง --urls ไปที่ app โดยตรง
    dotnet_process = subprocess.Popen(
        ["dotnet", "watch", "run", "--no-launch-profile", "--", "--urls", urls],
        cwd=str(SERVICES_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    
    # Monitor output in background
    monitor_thread = threading.Thread(
        target=monitor_dotnet_output,
        args=(dotnet_process, port, https),
        daemon=True,
    )
    monitor_thread.start()


class CodeChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = 0
        self.debounce_seconds = 0.5

    def on_modified(self, event):
        if event.src_path.endswith("input.py"):
            current_time = time.time()
            if current_time - self.last_modified > self.debounce_seconds:
                self.last_modified = current_time
                try:
                    log_info("Change detected, recompiling...")
                    compile_only()
                    log_success("Compiled → dotnet watch will reload")
                except Exception as e:
                    log_error(f"Compile failed: {e}")


@app.command()
def dev(
    port: int = typer.Option(DEFAULT_PORT, "--port", "-p", help="Port to run the server on"),
    https: bool = typer.Option(False, "--https", help="Enable HTTPS"),
    build_first: bool = typer.Option(True, "--build/--no-build", "-b", help="Build before starting"),
):
    """Start development mode with hot reload 🔥"""
    print_banner()
    
    print(f"  {Style.PURPLE}▸{Style.RESET} {Style.BOLD}Dev Mode{Style.RESET}")
    print(f"  {Style.GRAY}─────────────────────────{Style.RESET}")
    print(f"  {Style.GRAY}Port:{Style.RESET}       {Style.CYAN}{port}{Style.RESET}")
    print(f"  {Style.GRAY}HTTPS:{Style.RESET}      {Style.CYAN}{'Yes' if https else 'No'}{Style.RESET}")
    print(f"  {Style.GRAY}Hot Reload:{Style.RESET} {Style.GREEN}Enabled (.NET Watch){Style.RESET}")
    print()

    ensure_services_dir()
    if not ensure_dotnet_project():
        raise typer.Exit(code=1)

    if build_first:
        log_info("Initial build...")
        try:
            compile_only()
            log_success("Compiled successfully")
        except Exception as e:
            log_error(f"Initial build failed: {e}")
            raise typer.Exit(code=1)

    # Start dotnet watch (it will auto-reload when Program.cs changes)
    run_dotnet_watch(port, https)

    # Watch input.py for changes
    log_info(f"Watching {Style.BOLD}input.py{Style.RESET} for changes...")
    
    event_handler = CodeChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Style.GRAY}Shutting down...{Style.RESET}")
        observer.stop()
        if dotnet_process:
            dotnet_process.terminate()
        log_success("Server stopped. Goodbye! 👋")
    observer.join()


@app.command()
def clean():
    """Remove the services/ directory and all generated files"""
    if SERVICES_DIR.exists():
        confirm = typer.confirm(f"Delete {SERVICES_DIR}/ directory?")
        if confirm:
            shutil.rmtree(SERVICES_DIR)
            log_success(f"Removed {SERVICES_DIR}/")
        else:
            log_info("Cancelled")
    else:
        log_info(f"{SERVICES_DIR}/ does not exist")


@app.command()
def version():
    """Show Dukpyra version"""
    print(f"\n  {Style.PURPLE}{Style.BOLD}🔮 Dukpyra{Style.RESET} {Style.GRAY}v0.1.0{Style.RESET}")
    print(f"  {Style.GRAY}Python → C# JIT Compiler{Style.RESET}\n")


if __name__ == "__main__":
    app()
