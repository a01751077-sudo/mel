# APTS Quick Start Guide
## Clone, Install, and Test the System

🚀 **Ready to test your military-grade penetration testing system?**

## 📥 Step 1: Clone the Repository

```bash
# Clone the APTS repository
git clone https://github.com/husyia52-png/yui.git

# Navigate to the project directory
cd yui

# Switch to the APTS feature branch
git checkout feature/apts-military-grade-penetration-testing-system

# Verify you're on the correct branch
git branch
```

## 🔧 Step 2: System Requirements Check

```bash
# Check Python version (3.8+ required)
python3 --version

# Check available memory (4GB+ recommended)
free -h

# Check disk space (10GB+ recommended)
df -h

# Check internet connectivity
ping -c 3 google.com
```

## 📦 Step 3: Install Dependencies

### Option A: Automated Installation (Recommended)
```bash
# Run the automated installer
python3 install.py
```

### Option B: Manual Installation
```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y nmap tor proxychains dnsutils whois build-essential libssl-dev libffi-dev python3-dev git curl wget

# Install Python dependencies
pip3 install -r requirements.txt

# Or install core dependencies manually
pip3 install rich loguru aiohttp cryptography requests beautifulsoup4 asyncio aiofiles
```

## 🚀 Step 4: Launch APTS

```bash
# Start the Advanced Penetration Testing System
python3 apts.py
```

You should see the APTS banner and legal disclaimer:

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     █████╗ ██████╗ ████████╗███████╗                         ║
║    ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝                         ║
║    ███████║██████╔╝   ██║   ███████╗                         ║
║    ██╔══██║██╔═══╝    ██║   ╚════██║                         ║
║    ██║  ██║██║        ██║   ███████║                         ║
║    ╚═╝  ╚═╝╚═╝        ╚═╝   ╚══════╝                         ║
║                                                               ║
║         Advanced Penetration Testing System                   ║
║              Military-Grade Security Assessment               ║
║                                                               ║
║    Version: 1.0.0 - GHOST PROTOCOL                          ║
║    Classification: AUTHORIZED USE ONLY                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

⚠️  WARNING: AUTHORIZED PENETRATION TESTING ONLY ⚠️
```

## ⚖️ Step 5: Legal Authorization

When prompted:
```
Do you have written authorization to test your targets? (yes/no):
```

**IMPORTANT**: Only answer "yes" if you have:
- ✅ Written authorization from target system owners
- ✅ Legal permission to test the systems
- ✅ Proper scope and boundaries defined
- ✅ Emergency contact procedures in place

## 🎯 Step 6: System Testing Workflow

### 6.1 Initialize System
```
🚀 Initializing APTS Ghost Protocol...
⚡ Activating hardware optimization...
👻 Initializing Ghost Mode anonymization...
🎯 Initializing target acquisition system...
🔍 Loading 30 critical vulnerability modules...
📊 Initializing encrypted reporting system...
✅ APTS Ghost Protocol initialized successfully!
```

### 6.2 Main Menu Options
```
APTS - Main Menu

[1] Activate Ghost Mode (Level 1)
[2] Configure Targets (Level 2)
[3] Run Penetration Test
[4] View System Status
[5] Generate Test Report
[6] Exit System
```

### 6.3 Testing Sequence

#### Option 1: Activate Ghost Mode
```
Select option (1-6): 1

👻 Activating Ghost Mode...
🔄 Starting proxy scraping and verification...
🧅 Connecting to Tor network...
🎭 Activating traffic obfuscation...
🔍 Verifying anonymization level...
✅ Ghost Mode activated! Anonymity level: 97%
```

#### Option 2: Configure Targets
```
Select option (1-6): 2

🎯 Target Configuration
Enter target URLs (comma-separated): https://example.com, https://test-site.com
✅ Configured 2 target(s)
```

#### Option 3: Run Penetration Test
```
Select option (1-6): 3

🎯 Starting penetration test on 2 target(s)...
🔍 Phase 1: Target acquisition and reconnaissance...
⚔️  Phase 2: Aggressive vulnerability assessment...
💥 Phase 3: Exploitation and evidence collection...
📊 Phase 4: Generating encrypted report...
✅ Penetration test completed! Report: reports/APTS_Security_Assessment_20241109_143022_ENCRYPTED.apts
```

## 🧪 Step 7: Test Your Own Platform First

**CRITICAL**: Before testing client systems, test on your own secure platform:

```bash
# Set up a local test environment
docker run -d -p 8080:80 --name test-target nginx

# Configure APTS to test localhost
# Target: http://localhost:8080
```

## 📊 Step 8: Review Results

### Expected Output
```
🎯 APTS Assessment Results
Target: example.com

🔴 CRITICAL Vulnerabilities Found: 3
├── Hot Wallet Private Key Exposed
│   Impact: Complete hot wallet drainage
│   One-Line Hack: transfer_all_funds('attacker_wallet', private_key='...')
├── Admin Transaction Token Leaked
│   Impact: Unlimited fund transfers
│   One-Line Hack: curl -H 'Authorization: Bearer ...' -X POST /api/admin/transfer
└── Database Admin Credentials Exposed
    Impact: Complete database access
    One-Line Hack: mysql -u admin -p'password' -e 'UPDATE balances...'

💰 Total Funds at Risk: $50,000,000+
⏱️ Time to Complete Compromise: < 5 minutes
🚨 Immediate Action Required: Move all funds to cold storage
```

### Decrypt Reports
```bash
# The system will generate encrypted reports
# To decrypt (for authorized personnel only):
python3 -c "
from core.reporting import ReportingEngine
engine = ReportingEngine()
engine.decrypt_report('reports/APTS_Security_Assessment_ENCRYPTED.apts', 'decrypted_output')
"

# Passphrase: WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Install missing dependencies
pip3 install <missing_module>

# Or reinstall all requirements
pip3 install -r requirements.txt --force-reinstall
```

#### 2. Permission Errors
```bash
# Make scripts executable
chmod +x apts.py install.py

# Run with proper permissions
sudo python3 apts.py  # Only if needed
```

#### 3. Network Issues
```bash
# Check internet connectivity
ping -c 3 8.8.8.8

# Test proxy connectivity
curl --proxy socks5://127.0.0.1:9050 http://httpbin.org/ip
```

#### 4. Low Anonymity Levels
```bash
# Restart Tor service
sudo systemctl restart tor

# Clear proxy cache and restart Ghost Mode
```

## 🎯 Testing Scenarios

### Scenario 1: Basic Functionality Test
```bash
# Target: Your own test server
python3 apts.py
# 1. Activate Ghost Mode
# 2. Configure target: http://localhost:8080
# 3. Run basic scan
```

### Scenario 2: Crypto Exchange Simulation
```bash
# Set up a mock crypto exchange
# Test all 30 vulnerability modules
# Verify one-line hack detection
```

### Scenario 3: Full Assessment Workflow
```bash
# Complete end-to-end testing
# Ghost Mode → Target Config → Full Scan → Report Generation
```

## 📋 Pre-Production Checklist

Before using APTS on client systems:

- [ ] **Legal Authorization** - Written permission obtained
- [ ] **Test Environment** - Successfully tested on own systems
- [ ] **Ghost Mode** - Achieving 95%+ anonymity consistently
- [ ] **All Modules** - 30 vulnerability modules loading correctly
- [ ] **Reporting** - Encrypted reports generating successfully
- [ ] **Emergency Procedures** - Incident response plan in place
- [ ] **Insurance** - Professional liability coverage active

## 🚨 Emergency Commands

### Immediate Stop
```bash
# Kill all APTS processes
pkill -f apts.py

# Clear all temporary files
rm -rf temp/* logs/* evidence/*
```

### System Cleanup
```bash
# Secure deletion of sensitive data
shred -vfz -n 3 logs/* evidence/* reports/*

# Clear system caches
sync && echo 3 > /proc/sys/vm/drop_caches
```

## 🎉 You're Ready!

Your APTS system is now ready for authorized penetration testing. Remember:

- ✅ **Always get written authorization**
- ✅ **Test on your own systems first**
- ✅ **Use Ghost Mode for anonymity**
- ✅ **Follow responsible disclosure**
- ✅ **Keep evidence secure**

**Happy (Ethical) Hacking!** 🔒

---

*APTS v1.0.0 - GHOST PROTOCOL*
*For Authorized Security Assessments Only*