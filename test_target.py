#!/usr/bin/env python3
"""
Test Target Server - Simulates a vulnerable crypto platform for testing APTS
Contains REAL one-line hack vulnerabilities for demonstration
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with vulnerable endpoints"""
        
        # Simulate vulnerable endpoints with one-line hack credentials
        vulnerable_responses = {
            "/.env": """
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=admin123
mysql_root_password=supersecret123

# Hot Wallet Configuration  
hot_wallet_private_key=a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456
ethereum_private_key=0xa1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456

# Admin Tokens
admin_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJzdXBlcl9hZG1pbiJ9
super_admin_token=SUPER_ADMIN_GOD_MODE_TOKEN_12345
transaction_auth_token=TRANSACTION_BYPASS_TOKEN_67890

# Cloud Credentials
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

# HSM Configuration
hsm_token=HSM_MASTER_TOKEN_ABCDEF123456
cold_wallet_key=cold_wallet_master_key_xyz789
""",
            
            "/config.json": json.dumps({
                "database": {
                    "host": "localhost",
                    "user": "root", 
                    "password": "admin123"
                },
                "wallet": {
                    "hot_wallet_private_key": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
                    "cold_wallet_key": "cold_wallet_master_key_xyz789"
                },
                "admin": {
                    "super_admin_token": "SUPER_ADMIN_GOD_MODE_TOKEN_12345",
                    "transaction_auth_token": "TRANSACTION_BYPASS_TOKEN_67890"
                }
            }),
            
            "/wallet.json": json.dumps({
                "private_key": "a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456",
                "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
                "seed": "master_seed_phrase_for_all_wallets_123456789"
            }),
            
            "/admin/config": json.dumps({
                "admin_session": "ADMIN_SESSION_TOKEN_ABCDEF",
                "god_mode_token": "GOD_MODE_UNLIMITED_ACCESS_TOKEN",
                "bypass_token": "BYPASS_ALL_SECURITY_TOKEN_123"
            }),
            
            "/api/admin/token": json.dumps({
                "token": "ADMIN_API_TOKEN_FULL_ACCESS_123456",
                "permissions": ["transfer", "withdraw", "admin", "god_mode"]
            }),
            
            "/hsm/config": json.dumps({
                "hsm_token": "HSM_MASTER_TOKEN_ABCDEF123456",
                "hardware_security_module": "MASTER_HSM_KEY_XYZ789"
            }),
            
            "/trading/config": json.dumps({
                "trading_engine_key": "TRADING_ENGINE_MASTER_KEY_123",
                "market_maker_token": "MARKET_MANIPULATION_TOKEN_456"
            }),
            
            "/k8s/config": """
apiVersion: v1
kind: Config
users:
- name: admin
  user:
    token: KUBERNETES_ADMIN_TOKEN_CLUSTER_MASTER_123456
""",
            
            "/.aws/credentials": """
[default]
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
"""
        }
        
        if self.path in vulnerable_responses:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(vulnerable_responses[self.path].encode())
        else:
            # Return 404 for other paths
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass

def start_test_server(port=8888):
    """Start the vulnerable test server"""
    server = HTTPServer(('localhost', port), VulnerableHandler)
    print(f"🎯 Vulnerable test server started on http://localhost:{port}")
    print("📋 Available vulnerable endpoints:")
    print("   - /.env (contains hot wallet keys, admin tokens, DB creds)")
    print("   - /config.json (JSON config with credentials)")
    print("   - /wallet.json (wallet private keys)")
    print("   - /admin/config (admin tokens)")
    print("   - /api/admin/token (API admin token)")
    print("   - /hsm/config (HSM tokens)")
    print("   - /trading/config (trading engine keys)")
    print("   - /k8s/config (Kubernetes admin token)")
    print("   - /.aws/credentials (AWS keys)")
    print("\n🚨 This server contains REAL one-line hack vulnerabilities for testing!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Test server stopped")
        server.shutdown()

if __name__ == "__main__":
    start_test_server()