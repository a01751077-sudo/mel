"""
APTS Configuration Settings
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
EVIDENCE_DIR = BASE_DIR / "evidence"
TEMP_DIR = BASE_DIR / "temp"

# Create directories
for directory in [LOGS_DIR, REPORTS_DIR, EVIDENCE_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Ghost Mode Settings
GHOST_MODE = {
    "PROXY_SOURCES_COUNT": 300,
    "PROXY_VERIFICATION_CONCURRENT": 100,
    "PROXY_ROTATION_INTERVAL": 30,  # seconds
    "TOR_CIRCUIT_ROTATION": 60,  # seconds
    "ANONYMITY_THRESHOLD": 95,  # minimum anonymity level required
    "USER_AGENT_ROTATION": True,
    "HEADER_RANDOMIZATION": True,
    "REQUEST_DELAY_MIN": 0.1,
    "REQUEST_DELAY_MAX": 2.0
}

# Target System Settings
TARGET_SYSTEM = {
    "MAX_CONCURRENT_SCANS": 50,
    "SUBDOMAIN_WORDLIST_SIZE": 10000,
    "PORT_SCAN_TIMEOUT": 3,
    "HTTP_REQUEST_TIMEOUT": 30,
    "DNS_TIMEOUT": 5,
    "MAX_SUBDOMAINS_PER_TARGET": 1000
}

# Vulnerability Engine Settings
VULNERABILITY_ENGINE = {
    "MAX_CONCURRENT_MODULES": 10,
    "MODULE_TIMEOUT": 300,  # 5 minutes per module
    "EXPLOITATION_ENABLED": True,
    "EVIDENCE_COLLECTION": True,
    "SCREENSHOT_ENABLED": True,
    "NETWORK_CAPTURE": True
}

# Reporting Settings
REPORTING = {
    "ENCRYPTION_ENABLED": True,
    "DIGITAL_SIGNATURES": True,
    "EVIDENCE_COMPRESSION": True,
    "REPORT_FORMATS": ["markdown", "json", "pdf"],
    "MASTER_PASSPHRASE": "WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER"
}

# Security Settings
SECURITY = {
    "AUTHORIZED_ONLY": True,
    "CONSENT_REQUIRED": True,
    "AUDIT_LOGGING": True,
    "SECURE_DELETION": True,
    "MEMORY_ONLY_MODE": False  # Set to True for maximum security
}

# Performance Settings
PERFORMANCE = {
    "HARDWARE_OPTIMIZATION": True,
    "MEMORY_COMPRESSION": True,
    "CPU_OPTIMIZATION": True,
    "NETWORK_OPTIMIZATION": True,
    "STORAGE_OPTIMIZATION": True
}