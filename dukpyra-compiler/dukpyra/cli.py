#!/usr/bin/env python3
"""
Dukpyra CLI - Main Command Line Interface
ตัวหลักของ CLI ที่ผู้ใช้เรียกผ่าน terminal
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Import จาก modules อื่นใน package
try:
    from .lexer import lexer
    from .parser import parser
except ImportError:
    # ถ้ารันโดยตรงไม่ผ่าน package
    import ply.lex as lex
    import ply.yacc as yacc


class DukpyraCompiler:
    """หัวใจของ Compiler - แปลง Python เป็น C#"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.hidden_dir = project_root / ".dukpyra"
        self.compiled_dir = self.hidden_dir / "compiled"
        self.bin_dir = self.hidden_dir / "bin"
        self.obj_dir = self.hidden_dir / "obj"

    def ensure_structure(self):
        """สร้างโครงสร้างโฟลเดอร์ที่จำเป็น"""
        self.hidden_dir.mkdir(exist_ok=True)
        self.compiled_dir.mkdir(exist_ok=True)
        self.bin_dir.mkdir(exist_ok=True)
        self.obj_dir.mkdir(exist_ok=True)

        # สร้าง .gitignore
        gitignore = self.project_root / ".gitignore"
        if not gitignore.exists():
            with open(gitignore, "w") as f:
                f.write("# Dukpyra\n")
                f.write(".dukpyra/\n")
                f.write("__pycache__/\n")
                f.write("*.pyc\n")

    def compile_file(self, python_file: Path) -> str:
        """
        แปลงไฟล์ Python หนึ่งไฟล์เป็น C#
        ใช้ Lexer + Parser ที่เราสร้างไว้
        """
        with open(python_file, "r", encoding="utf-8") as f:
            python_code = f.read()

        try:
            # ใช้ lexer และ parser จาก modules
            result = parser.parse(python_code.strip() + "\n", lexer=lexer)
            return result if result else ""
        except Exception as e:
            click.echo(f"❌ Error compiling {python_file.name}: {e}", err=True)
            return ""

    def compile_project(self) -> bool:
        """Compile ทั้งโปรเจกต์"""
        click.echo("🔨 Compiling Python to C#...")

        # หา Python files ในโฟลเดอร์หลักเท่านั้น (ไม่รวม subdirectories)
        # ยกเว้นไฟล์ที่ไม่ใช่ API เช่น tests, setup.py, conftest.py
        excluded_files = {'setup.py', 'conftest.py', '__init__.py'}
        excluded_prefixes = ('test_',)
        
        python_files = []
        for py_file in self.project_root.glob("*.py"):
            if py_file.name in excluded_files:
                continue
            if py_file.name.startswith(excluded_prefixes):
                continue
            if ".dukpyra" not in str(py_file):
                python_files.append(py_file)

        if not python_files:
            click.echo("❌ No Python files found!", err=True)
            return False

        # Compile แต่ละไฟล์
        all_routes = []
        for py_file in python_files:
            click.echo(f"   📄 {py_file.relative_to(self.project_root)}")
            csharp_code = self.compile_file(py_file)
            if csharp_code:
                all_routes.append(csharp_code)

        if not all_routes:
            click.echo("❌ No routes compiled!", err=True)
            return False

        # สร้าง Program.cs
        program_cs_content = self._merge_compiled_code(all_routes)
        program_cs_path = self.compiled_dir / "Program.cs"

        with open(program_cs_path, "w", encoding="utf-8") as f:
            f.write(program_cs_content)

        # สร้าง .csproj
        self._create_csproj()

        click.echo(f"✅ Compiled successfully!")
        click.echo(f"   Output: {program_cs_path.relative_to(self.project_root)}")
        return True

    def _merge_compiled_code(self, routes: list) -> str:
        """รวมโค้ด C# จากหลายๆ ไฟล์เป็นไฟล์เดียว"""
        
        all_route_blocks = []
        for route_output in routes:
            # ตัด header และ footer ออก เอาเฉพาะ routes
            # Parser จะสร้าง output ที่มี "// --- Dukpyra Generated Routes ---" และ "// --------------------------------"
            lines = route_output.split('\n')
            in_routes = False
            route_lines = []
            
            for line in lines:
                if "// --- Dukpyra Generated Routes ---" in line:
                    in_routes = True
                    continue
                if "// --------------------------------" in line:
                    in_routes = False
                    continue
                if in_routes:
                    route_lines.append(line)
            
            if route_lines:
                all_route_blocks.append('\n'.join(route_lines).strip())
        
        # สร้าง Program.cs ใหม่
        header = """var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// ===== Dukpyra Generated Routes =====

"""
        footer = """

// ====================================

app.Run();
"""
        return header + "\n\n".join(all_route_blocks) + footer

    def _create_csproj(self):
        """สร้างไฟล์ .csproj สำหรับ dotnet"""
        csproj_content = """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputPath>../bin/</OutputPath>
    <IntermediateOutputPath>../obj/</IntermediateOutputPath>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
"""
        csproj_path = self.compiled_dir / "dukpyra.csproj"
        with open(csproj_path, "w") as f:
            f.write(csproj_content)


class FileWatcher(FileSystemEventHandler):
    """ดูการเปลี่ยนแปลงของไฟล์ Python"""

    def __init__(self, compiler: DukpyraCompiler, restart_callback):
        self.compiler = compiler
        self.restart_callback = restart_callback
        self.last_compile = 0

    def on_modified(self, event):
        if event.src_path.endswith(".py") and ".dukpyra" not in event.src_path:
            # Debounce (ป้องกันการ compile ซ้ำเร็วเกินไป)
            current_time = time.time()
            if current_time - self.last_compile < 1:
                return

            self.last_compile = current_time

            click.echo(f"\n🔄 File changed: {Path(event.src_path).name}")
            if self.compiler.compile_project():
                click.echo("🚀 Restarting server...\n")
                self.restart_callback()


# ============================================================================
# CLI Commands
# ============================================================================


@click.group()
@click.version_option(version="0.1.0", prog_name="dukpyra")
def cli():
    """
    🚀 Dukpyra - Python to ASP.NET Core Compiler

    Convert Python web frameworks to high-performance ASP.NET Core
    """
    pass


@cli.command()
@click.argument("name", default="my-backend")
@click.option(
    "--template", default="minimal", help="Project template (minimal/api/full)"
)
def init(name, template):
    """
    Initialize a new Dukpyra project

    Example: dukpyra init my-backend
    """
    project_dir = Path.cwd() / name

    if project_dir.exists():
        click.echo(f"❌ Directory '{name}' already exists!", err=True)
        return

    click.echo(f"🎉 Creating Dukpyra project: {name}")

    # สร้างโฟลเดอร์
    project_dir.mkdir(parents=True)

    # สร้าง compiler instance
    compiler = DukpyraCompiler(project_dir)
    compiler.ensure_structure()

    # สร้างไฟล์ตัวอย่าง
    main_py = project_dir / "main.py"
    with open(main_py, "w", encoding="utf-8") as f:
        f.write("""# Dukpyra Example - Python Web API

@app.get("/")
def home():
    return {"message": "Hello from Dukpyra!", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": 1234567890}

@app.post("/api/users")
def create_user():
    return {"id": 1, "name": "John Doe", "created": "true"}
""")

    # สร้าง README
    readme = project_dir / "README.md"
    with open(readme, "w") as f:
        f.write(f"""# {name}

Created with Dukpyra 🚀

## Run

```bash
cd {name}
dukpyra run
```

## Files

- `main.py` - Your Python routes
- `.dukpyra/` - Compiled C# code (hidden)
""")

    click.echo(f"✅ Project created successfully!")
    click.echo(f"\n📝 Next steps:")
    click.echo(f"   cd {name}")
    click.echo(f"   dukpyra run")
    click.echo(f"\n📖 Edit main.py to add your routes")


@cli.command()
@click.option("--port", default=5000, help="Port to run on")
@click.option("--watch/--no-watch", default=True, help="Enable file watching")
def run(port, watch):
    """
    Run the Dukpyra project (compile + execute)

    This will:
    1. Compile Python to C#
    2. Start ASP.NET server
    3. Watch for changes (if --watch enabled)
    """
    project_dir = Path.cwd()

    # ตรวจสอบว่ามี .NET SDK หรือไม่
    try:
        subprocess.run(["dotnet", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        click.echo("❌ .NET SDK not found!", err=True)
        click.echo("   Install from: https://dotnet.microsoft.com/download")
        return

    click.echo("🚀 Starting Dukpyra...\n")

    compiler = DukpyraCompiler(project_dir)
    compiler.ensure_structure()

    # Compile ครั้งแรก
    if not compiler.compile_project():
        return

    click.echo(f"\n🌐 Starting ASP.NET server on port {port}...\n")

    csproj_path = compiler.compiled_dir / "dukpyra.csproj"
    process = None

    def start_server():
        nonlocal process
        if process:
            process.terminate()
            process.wait()

        process = subprocess.Popen(
            [
                "dotnet",
                "run",
                "--project",
                str(csproj_path),
                "--urls",
                f"http://localhost:{port}",
            ],
            cwd=str(compiler.compiled_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        # แสดง output
        try:
            for line in process.stdout:
                click.echo(line.rstrip())
        except KeyboardInterrupt:
            pass

    if watch:
        # เริ่ม watch mode
        event_handler = FileWatcher(compiler, start_server)
        observer = Observer()
        observer.schedule(event_handler, str(project_dir), recursive=True)
        observer.start()

        click.echo(f"👀 Watching for changes... (Press Ctrl+C to stop)\n")

        try:
            start_server()
        except KeyboardInterrupt:
            click.echo("\n\n👋 Stopping Dukpyra...")
            if process:
                process.terminate()
            observer.stop()

        observer.join()
    else:
        # รันแบบไม่ watch
        try:
            start_server()
        except KeyboardInterrupt:
            click.echo("\n\n👋 Stopping server...")
            if process:
                process.terminate()


@cli.command()
@click.option("--format", type=click.Choice(["text", "file"]), default="text")
def show(format):
    """
    Show the compiled C# code

    Example: dukpyra show
    """
    project_dir = Path.cwd()
    compiled_file = project_dir / ".dukpyra" / "compiled" / "Program.cs"

    if not compiled_file.exists():
        click.echo("❌ No compiled code found.", err=True)
        click.echo("   Run 'dukpyra run' first.")
        return

    with open(compiled_file, "r", encoding="utf-8") as f:
        code = f.read()

    if format == "text":
        click.echo("📄 Compiled C# Code:")
        click.echo("=" * 60)
        click.echo(code)
    else:
        output_file = project_dir / "Program.cs"
        with open(output_file, "w") as f:
            f.write(code)
        click.echo(f"✅ Saved to: {output_file}")


@cli.command()
@click.confirmation_option(prompt="Are you sure you want to delete all compiled files?")
def clean():
    """
    Clean all compiled files and build artifacts

    This will remove the .dukpyra directory
    """
    project_dir = Path.cwd()
    hidden_dir = project_dir / ".dukpyra"

    if hidden_dir.exists():
        shutil.rmtree(hidden_dir)
        click.echo("🧹 Cleaned .dukpyra directory")
    else:
        click.echo("✨ Already clean - no compiled files found")


@cli.command()
@click.option("--output", "-o", default="./dist", help="Output directory")
def build(output):
    """
    Build a production-ready binary

    This creates a standalone executable
    """
    project_dir = Path.cwd()
    compiler = DukpyraCompiler(project_dir)

    click.echo("🏗️  Building production binary...")

    # Compile
    if not compiler.compile_project():
        return

    output_dir = Path(output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build with dotnet publish
    csproj_path = compiler.compiled_dir / "dukpyra.csproj"

    result = subprocess.run(
        [
            "dotnet",
            "publish",
            str(csproj_path),
            "-c",
            "Release",
            "-o",
            str(output_dir),
            "--self-contained",
            "true",
            "-r",
            "linux-x64",
        ],  # เปลี่ยนตาม platform
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        click.echo(f"✅ Build successful!")
        click.echo(f"   Output: {output_dir}")
    else:
        click.echo(f"❌ Build failed!", err=True)
        click.echo(result.stderr)


@cli.command()
def info():
    """Show project information and status"""
    project_dir = Path.cwd()

    click.echo("📊 Dukpyra Project Info\n")
    click.echo(f"Project: {project_dir.name}")
    click.echo(f"Path: {project_dir}")

    # นับไฟล์ Python
    py_files = list(project_dir.glob("**/*.py"))
    py_files = [f for f in py_files if ".dukpyra" not in str(f)]
    click.echo(f"Python files: {len(py_files)}")

    # ตรวจสอบ compilation
    compiled = project_dir / ".dukpyra" / "compiled" / "Program.cs"
    if compiled.exists():
        size = compiled.stat().st_size
        click.echo(f"Compiled: Yes ({size} bytes)")
    else:
        click.echo("Compiled: No")

    # ตรวจสอบ .NET
    try:
        result = subprocess.run(["dotnet", "--version"], capture_output=True, text=True)
        dotnet_version = result.stdout.strip()
        click.echo(f".NET SDK: {dotnet_version}")
    except FileNotFoundError:
        click.echo(".NET SDK: Not installed")


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
