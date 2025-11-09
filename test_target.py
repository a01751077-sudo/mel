#!/usr/bin/env python3
"""
Test Target Server - Simulates a vulnerable crypto platform for testing APTS
Contains REAL one-line hack vulnerabilities for demonstration
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
import urllib.parse

class VulnerableHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with vulnerable endpoints"""
        
        # Simulate vulnerable endpoints with one-line hack credentials
        vulnerable_responses = {
            "/login": """
            <html><body>
            <h1>Admin Login</h1>
            <form method="POST" action="/login">
                <input type="text" name="username" placeholder="Username">
                <input type="password" name="password" placeholder="Password">
                <input type="submit" value="Login">
            </form>
            </body></html>
            """,
            
            "/admin": """
            <html><body>
            <h1>Access Denied</h1>
            <p>You need admin privileges to access this area.</p>
            </body></html>
            """,
            
            "/search": """
            <html><body>
            <h1>Search</h1>
            <form method="GET">
                <input type="text" name="q" placeholder="Search...">
                <input type="submit" value="Search">
            </form>
            </body></html>
            """,
            
            "/file": """
            <html><body>
            <h1>File Viewer</h1>
            <form method="GET">
                <input type="text" name="file" placeholder="File path...">
                <input type="submit" value="View File">
            </form>
            </body></html>
            """,
            
            "/upload": """
            <html><body>
            <h1>File Upload</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
            </body></html>
            """,
            
            "/api/users": json.dumps({
                "users": [
                    {"id": 1, "username": "admin", "password": "admin123", "role": "administrator"},
                    {"id": 2, "username": "user", "password": "user123", "role": "user"}
                ],
                "admin_token": "ADMIN_API_TOKEN_12345",
                "database_password": "db_secret_123"
            }),
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
        
        # Handle XSS in search
        if self.path.startswith('/search?'):
            query = self.path.split('q=')[1] if 'q=' in self.path else ''
            query = urllib.parse.unquote(query)
            
            # VULNERABLE: Reflect user input without sanitization (XSS)
            response = f"""
            <html><body>
            <h1>Search Results</h1>
            <p>You searched for: {query}</p>
            <p>No results found.</p>
            </body></html>
            """
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(response.encode())
            
        # Handle directory traversal in file viewer
        elif self.path.startswith('/file?'):
            file_param = self.path.split('file=')[1] if 'file=' in self.path else ''
            file_param = urllib.parse.unquote(file_param)
            
            # VULNERABLE: Directory traversal
            if '../' in file_param or 'etc/passwd' in file_param:
                response = """root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
admin:x:1000:1000:admin:/home/admin:/bin/bash"""
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                self.send_response(404)
                self.end_headers()
                
        elif self.path in vulnerable_responses:
            content_type = 'text/html' if self.path in ['/login', '/admin', '/search', '/file', '/upload'] else 'text/plain'
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(vulnerable_responses[self.path].encode())
        else:
            # Return 404 for other paths
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests with vulnerabilities"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Handle SQL injection in login
        if self.path == '/login':
            # Parse form data
            params = urllib.parse.parse_qs(post_data)
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            # VULNERABLE: SQL injection bypass
            if "' OR '1'='1'" in username or "' OR 1=1" in username:
                # SQL injection successful - return admin dashboard
                response = """
                <html><body>
                <h1>Admin Dashboard</h1>
                <p>Welcome, Administrator!</p>
                <p>You have successfully logged in.</p>
                <a href="/admin/users">Manage Users</a> |
                <a href="/admin/settings">Settings</a> |
                <a href="/logout">Logout</a>
                </body></html>
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                # Normal login failed
                response = """
                <html><body>
                <h1>Login Failed</h1>
                <p>Invalid username or password.</p>
                <a href="/login">Try Again</a>
                </body></html>
                """
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
                
        # Handle file upload
        elif self.path == '/upload':
            # VULNERABLE: File upload allows any file type
            if 'shell.php' in post_data or '<?php' in post_data:
                response = """
                <html><body>
                <h1>Upload Successful</h1>
                <p>File uploaded successfully to /uploads/shell.php</p>
                <p>File is now accessible at <a href="/uploads/shell.php">/uploads/shell.php</a></p>
                </body></html>
                """
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
            else:
                response = """
                <html><body>
                <h1>Upload Failed</h1>
                <p>File upload failed.</p>
                </body></html>
                """
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(response.encode())
        else:
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