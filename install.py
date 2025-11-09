#!/usr/bin/env python3
"""
APTS Installation and Setup Script
Automated installation of all dependencies and system configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class APTSInstaller:
    """APTS Installation Manager"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.base_dir = Path(__file__).parent
        
    def check_requirements(self):
        """Check system requirements"""
        console.print("\n[bold blue]🔍 Checking system requirements...[/bold blue]")
        
        # Check Python version
        if self.python_version < (3, 8):
            console.print("[bold red]❌ Python 3.8+ required![/bold red]")
            sys.exit(1)
        else:
            console.print(f"[green]✅ Python {self.python_version.major}.{self.python_version.minor} detected[/green]")
            
        # Check pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            console.print("[green]✅ pip available[/green]")
        except subprocess.CalledProcessError:
            console.print("[bold red]❌ pip not available![/bold red]")
            sys.exit(1)
            
    def install_system_dependencies(self):
        """Install system-level dependencies"""
        console.print("\n[bold blue]📦 Installing system dependencies...[/bold blue]")
        
        if self.system == "linux":
            self._install_linux_deps()
        elif self.system == "darwin":  # macOS
            self._install_macos_deps()
        elif self.system == "windows":
            self._install_windows_deps()
        else:
            console.print(f"[yellow]⚠️ Unsupported system: {self.system}[/yellow]")
            
    def _install_linux_deps(self):
        """Install Linux dependencies"""
        deps = [
            "nmap", "tor", "proxychains", "dnsutils", "whois",
            "build-essential", "libssl-dev", "libffi-dev",
            "python3-dev", "git", "curl", "wget"
        ]
        
        try:
            # Try apt-get (Debian/Ubuntu)
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=True)
            console.print("[green]✅ Linux dependencies installed[/green]")
        except subprocess.CalledProcessError:
            try:
                # Try yum (RHEL/CentOS)
                subprocess.run(["sudo", "yum", "install", "-y"] + deps, check=True)
                console.print("[green]✅ Linux dependencies installed[/green]")
            except subprocess.CalledProcessError:
                console.print("[yellow]⚠️ Could not install system dependencies automatically[/yellow]")
                
    def _install_macos_deps(self):
        """Install macOS dependencies"""
        try:
            # Check if Homebrew is installed
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
            
            deps = ["nmap", "tor", "proxychains-ng", "whois"]
            subprocess.run(["brew", "install"] + deps, check=True)
            console.print("[green]✅ macOS dependencies installed[/green]")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠️ Homebrew not found. Please install Homebrew first[/yellow]")
            
    def _install_windows_deps(self):
        """Install Windows dependencies"""
        console.print("[yellow]⚠️ Windows detected. Some features may require manual setup[/yellow]")
        console.print("Please ensure you have:")
        console.print("- Nmap installed")
        console.print("- Tor Browser or standalone Tor")
        console.print("- Git for Windows")
        
    def install_python_dependencies(self):
        """Install Python dependencies"""
        console.print("\n[bold blue]🐍 Installing Python dependencies...[/bold blue]")
        
        requirements_file = self.base_dir / "requirements.txt"
        
        if not requirements_file.exists():
            console.print("[bold red]❌ requirements.txt not found![/bold red]")
            return
            
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Installing packages...", total=None)
                
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    console.print("[green]✅ Python dependencies installed successfully[/green]")
                else:
                    console.print("[bold red]❌ Failed to install Python dependencies[/bold red]")
                    console.print(result.stderr)
                    
        except Exception as e:
            console.print(f"[bold red]❌ Installation error: {e}[/bold red]")
            
    def setup_tor(self):
        """Setup Tor configuration"""
        console.print("\n[bold blue]🧅 Setting up Tor configuration...[/bold blue]")
        
        tor_config = """
# APTS Tor Configuration
SocksPort 9050
ControlPort 9051
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
CookieAuthentication 1
        """
        
        if self.system == "linux":
            tor_config_path = Path("/etc/tor/torrc")
            try:
                with open(tor_config_path, "a") as f:
                    f.write(tor_config)
                console.print("[green]✅ Tor configuration updated[/green]")
            except PermissionError:
                console.print("[yellow]⚠️ Could not update Tor config. Run with sudo or update manually[/yellow]")
        else:
            console.print("[yellow]⚠️ Please configure Tor manually for your system[/yellow]")
            
    def create_directories(self):
        """Create necessary directories"""
        console.print("\n[bold blue]📁 Creating directories...[/bold blue]")
        
        directories = [
            "logs", "reports", "evidence", "temp", "config", "modules", "exploits"
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(exist_ok=True)
            console.print(f"[green]✅ Created: {directory}/[/green]")
            
    def setup_permissions(self):
        """Setup file permissions"""
        if self.system != "windows":
            console.print("\n[bold blue]🔒 Setting up permissions...[/bold blue]")
            
            # Make main script executable
            main_script = self.base_dir / "apts.py"
            if main_script.exists():
                os.chmod(main_script, 0o755)
                console.print("[green]✅ Made apts.py executable[/green]")
                
    def run_tests(self):
        """Run basic system tests"""
        console.print("\n[bold blue]🧪 Running system tests...[/bold blue]")
        
        try:
            # Test Python imports
            test_imports = [
                "asyncio", "aiohttp", "cryptography", "loguru", 
                "rich", "requests", "beautifulsoup4"
            ]
            
            for module in test_imports:
                try:
                    __import__(module)
                    console.print(f"[green]✅ {module} import successful[/green]")
                except ImportError:
                    console.print(f"[red]❌ {module} import failed[/red]")
                    
        except Exception as e:
            console.print(f"[red]❌ Test error: {e}[/red]")
            
    def display_completion_message(self):
        """Display installation completion message"""
        completion_message = """
🎉 APTS Installation Complete! 🎉

Your Advanced Penetration Testing System is now ready for use.

Quick Start:
1. Run: python3 apts.py
2. Follow the setup wizard
3. Ensure you have written authorization before testing

Important Notes:
• This system is for AUTHORIZED testing only
• Always obtain proper legal authorization
• Use responsibly and ethically
• Keep your system updated

For support and updates:
• Check the documentation
• Review the code for customization
• Follow security best practices

Happy (Ethical) Hacking! 🔒
        """
        
        console.print(Panel(
            completion_message,
            title="[bold green]Installation Complete[/bold green]",
            border_style="green"
        ))
        
    def install(self):
        """Run complete installation process"""
        console.print(Panel(
            "APTS - Advanced Penetration Testing System\nInstallation Wizard",
            title="[bold red]APTS Installer[/bold red]",
            border_style="red"
        ))
        
        try:
            self.check_requirements()
            self.install_system_dependencies()
            self.install_python_dependencies()
            self.setup_tor()
            self.create_directories()
            self.setup_permissions()
            self.run_tests()
            self.display_completion_message()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Installation cancelled by user[/yellow]")
            sys.exit(1)
        except Exception as e:
            console.print(f"\n[bold red]Installation failed: {e}[/bold red]")
            sys.exit(1)

def main():
    """Main installation function"""
    installer = APTSInstaller()
    installer.install()

if __name__ == "__main__":
    main()