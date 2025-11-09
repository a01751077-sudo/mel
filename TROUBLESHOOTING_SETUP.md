# APTS Setup Troubleshooting Guide
## Fixing Common Installation Issues

🔧 **Having trouble getting APTS running? Here's how to fix it!**

## 🚨 Issue: "destination path 'yui' already exists"

This means you already have a `yui` directory. Here's how to fix it:

### Solution 1: Remove existing directory and clone fresh
```bash
# Remove the existing yui directory
rm -rf yui

# Clone the repository fresh
git clone https://github.com/husyia52-png/yui.git
cd yui

# Switch to the APTS branch
git checkout feature/apts-military-grade-penetration-testing-system

# Verify you have the APTS files
ls -la
```

### Solution 2: Clone to a different directory name
```bash
# Clone to a different directory name
git clone https://github.com/husyia52-png/yui.git apts-system
cd apts-system

# Switch to the APTS branch
git checkout feature/apts-military-grade-penetration-testing-system

# Verify you have the APTS files
ls -la
```

### Solution 3: Update existing repository
```bash
# Go into existing yui directory
cd yui

# Check current remote
git remote -v

# If it's the correct repository, fetch latest changes
git fetch origin

# Switch to the APTS branch
git checkout feature/apts-military-grade-penetration-testing-system

# If branch doesn't exist, create it from remote
git checkout -b feature/apts-military-grade-penetration-testing-system origin/feature/apts-military-grade-penetration-testing-system
```

## 🚨 Issue: "pathspec 'feature/apts-military-grade-penetration-testing-system' did not match"

This means the branch doesn't exist locally. Here's how to fix it:

```bash
# First, make sure you're in the right repository
cd yui
git remote -v

# Should show: origin  https://github.com/husyia52-png/yui.git

# Fetch all branches from remote
git fetch --all

# List all available branches
git branch -a

# Create and switch to the APTS branch
git checkout -b feature/apts-military-grade-penetration-testing-system origin/feature/apts-military-grade-penetration-testing-system
```

## 🚨 Issue: "can't open file 'install.py' or 'apts.py'"

This means you're not in the right directory or the files aren't there. Here's how to fix it:

```bash
# Check what files are in your current directory
ls -la

# You should see these APTS files:
# - apts.py (main system)
# - install.py (installer)
# - requirements.txt (dependencies)
# - core/ (core modules)
# - config/ (configuration)
# - README.md (documentation)

# If you don't see these files, you're either:
# 1. In the wrong directory
# 2. On the wrong branch
# 3. The repository wasn't cloned correctly
```

## 🔧 Complete Fresh Installation

If you're having multiple issues, here's a complete fresh start:

```bash
# Step 1: Clean slate
cd ~
rm -rf yui apts-system

# Step 2: Clone fresh
git clone https://github.com/husyia52-png/yui.git
cd yui

# Step 3: Verify repository
git remote -v
# Should show: origin  https://github.com/husyia52-png/yui.git

# Step 4: Fetch all branches
git fetch --all

# Step 5: List available branches
git branch -a
# Should show: remotes/origin/feature/apts-military-grade-penetration-testing-system

# Step 6: Switch to APTS branch
git checkout -b feature/apts-military-grade-penetration-testing-system origin/feature/apts-military-grade-penetration-testing-system

# Step 7: Verify APTS files are present
ls -la
# Should show: apts.py, install.py, requirements.txt, core/, config/, etc.

# Step 8: Install dependencies
python3 install.py

# Step 9: Start APTS
python3 apts.py
```

## 🔍 Verification Commands

Use these commands to verify everything is working:

```bash
# Check you're in the right directory
pwd
# Should show: /home/Rachael/yui (or similar)

# Check you're on the right branch
git branch
# Should show: * feature/apts-military-grade-penetration-testing-system

# Check APTS files exist
ls -la apts.py install.py requirements.txt
# Should show all three files

# Check Python version
python3 --version
# Should show: Python 3.8+ 

# Test basic import
python3 -c "import sys; print('Python path:', sys.executable)"
```

## 🚀 Alternative Installation Methods

### Method 1: Direct Download
If git is causing issues, download directly:

```bash
# Download the repository as ZIP
wget https://github.com/husyia52-png/yui/archive/refs/heads/feature/apts-military-grade-penetration-testing-system.zip

# Extract
unzip feature/apts-military-grade-penetration-testing-system.zip

# Navigate to extracted directory
cd yui-feature-apts-military-grade-penetration-testing-system

# Install and run
python3 install.py
python3 apts.py
```

### Method 2: Manual Dependency Installation
If the installer fails:

```bash
# Install core dependencies manually
pip3 install rich loguru aiohttp cryptography requests beautifulsoup4

# Install additional dependencies
pip3 install asyncio aiofiles uvloop stem socks PySocks scapy

# Install security libraries
pip3 install pycryptodome bcrypt jwt pyotp

# Install system tools
sudo apt-get update
sudo apt-get install -y nmap tor proxychains dnsutils whois

# Then start APTS
python3 apts.py
```

## 🆘 Still Having Issues?

### Check System Requirements
```bash
# Check Python version (need 3.8+)
python3 --version

# Check available memory (need 4GB+)
free -h

# Check disk space (need 10GB+)
df -h

# Check internet connection
ping -c 3 google.com
```

### Common Error Solutions

#### Error: "ModuleNotFoundError: No module named 'rich'"
```bash
pip3 install rich loguru
```

#### Error: "Permission denied"
```bash
chmod +x apts.py install.py
```

#### Error: "Can't connect to proxy sources"
```bash
# Check internet connection
curl -I https://google.com

# Try with different DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

## 📞 Getting Help

If you're still having issues:

1. **Check the error message carefully** - it usually tells you exactly what's wrong
2. **Verify you're in the right directory** - `pwd` should show the yui folder
3. **Check you're on the right branch** - `git branch` should show the APTS branch
4. **Ensure all files are present** - `ls -la` should show apts.py and other files
5. **Check Python version** - needs to be 3.8 or higher

## 🎯 Quick Success Path

Here's the fastest way to get APTS running:

```bash
# One-liner to get everything working
cd ~ && rm -rf yui && git clone https://github.com/husyia52-png/yui.git && cd yui && git checkout -b feature/apts-military-grade-penetration-testing-system origin/feature/apts-military-grade-penetration-testing-system && python3 install.py && python3 apts.py
```

This command will:
1. Remove any existing yui directory
2. Clone the repository fresh
3. Switch to the APTS branch
4. Install dependencies
5. Start the system

**You should see the APTS banner and be ready to go!** 🚀

---

*If you're still having issues after trying these solutions, the problem might be with your system environment or network connectivity.*