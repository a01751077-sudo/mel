"""
Target System - Level 2 Target Acquisition and Reconnaissance
Advanced target discovery and intelligence gathering
"""

import asyncio
import aiohttp
import re
import json
import socket
import ssl
import subprocess
from urllib.parse import urlparse, urljoin
from pathlib import Path
from typing import List, Dict, Set, Any, Optional
from dataclasses import dataclass, field
from loguru import logger
import dns.resolver
import whois
from bs4 import BeautifulSoup
import requests

@dataclass
class Target:
    """Target information structure"""
    url: str
    domain: str
    ip_addresses: List[str] = field(default_factory=list)
    subdomains: List[str] = field(default_factory=list)
    ports: Dict[int, str] = field(default_factory=dict)
    technologies: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    api_endpoints: List[str] = field(default_factory=list)
    mobile_apps: List[str] = field(default_factory=list)
    certificates: List[Dict] = field(default_factory=list)
    whois_info: Dict = field(default_factory=dict)
    cloud_services: List[str] = field(default_factory=list)
    third_party_services: List[str] = field(default_factory=list)

class SubdomainEnumerator:
    """Advanced subdomain enumeration"""
    
    def __init__(self):
        self.wordlists = self._load_wordlists()
        self.dns_servers = [
            "8.8.8.8", "8.8.4.4",  # Google
            "1.1.1.1", "1.0.0.1",  # Cloudflare
            "208.67.222.222", "208.67.220.220"  # OpenDNS
        ]
        
    def _load_wordlists(self) -> List[str]:
        """Load subdomain wordlists"""
        common_subdomains = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk",
            "ns2", "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test",
            "ns", "blog", "pop3", "dev", "www2", "admin", "forum", "news", "vpn", "ns3",
            "mail2", "new", "mysql", "old", "www1", "email", "img", "www3", "help", "shop",
            "api", "secure", "support", "www4", "app", "stage", "staging", "beta", "demo",
            "mobile", "cdn", "static", "media", "assets", "images", "js", "css", "files",
            "upload", "uploads", "download", "downloads", "docs", "documentation", "wiki",
            "portal", "dashboard", "panel", "control", "manage", "management", "admin2",
            "administrator", "root", "system", "internal", "private", "secret", "hidden",
            "backup", "backups", "archive", "old-site", "legacy", "v1", "v2", "v3", "api-v1",
            "api-v2", "rest", "graphql", "websocket", "ws", "wss", "socket", "realtime",
            "live", "stream", "video", "audio", "voice", "chat", "message", "notification",
            "push", "webhook", "callback", "oauth", "auth", "login", "signin", "signup",
            "register", "account", "profile", "user", "users", "customer", "customers",
            "client", "clients", "partner", "partners", "vendor", "vendors", "supplier",
            "payment", "pay", "billing", "invoice", "order", "orders", "cart", "checkout",
            "store", "shop", "ecommerce", "marketplace", "catalog", "product", "products",
            "service", "services", "solution", "solutions", "tool", "tools", "utility",
            "monitor", "monitoring", "metrics", "analytics", "stats", "statistics", "log",
            "logs", "audit", "report", "reports", "dashboard", "console", "terminal"
        ]
        
        return common_subdomains
        
    async def enumerate_subdomains(self, domain: str) -> List[str]:
        """Comprehensive subdomain enumeration"""
        logger.info(f"🔍 Enumerating subdomains for {domain}")
        
        subdomains = set()
        
        # Method 1: Dictionary-based enumeration
        dict_subdomains = await self._dictionary_enumeration(domain)
        subdomains.update(dict_subdomains)
        
        # Method 2: Certificate transparency logs
        ct_subdomains = await self._certificate_transparency_search(domain)
        subdomains.update(ct_subdomains)
        
        # Method 3: DNS zone transfer attempt
        zone_subdomains = await self._dns_zone_transfer(domain)
        subdomains.update(zone_subdomains)
        
        # Method 4: Search engine enumeration
        search_subdomains = await self._search_engine_enumeration(domain)
        subdomains.update(search_subdomains)
        
        # Method 5: Reverse DNS lookup
        reverse_subdomains = await self._reverse_dns_lookup(domain)
        subdomains.update(reverse_subdomains)
        
        # Validate discovered subdomains
        valid_subdomains = await self._validate_subdomains(list(subdomains))
        
        logger.info(f"✅ Found {len(valid_subdomains)} valid subdomains for {domain}")
        return valid_subdomains
        
    async def _dictionary_enumeration(self, domain: str) -> List[str]:
        """Dictionary-based subdomain enumeration"""
        subdomains = []
        semaphore = asyncio.Semaphore(50)  # Limit concurrent requests
        
        async def check_subdomain(subdomain: str):
            async with semaphore:
                full_domain = f"{subdomain}.{domain}"
                try:
                    # Try to resolve the subdomain
                    resolver = dns.resolver.Resolver()
                    resolver.timeout = 2
                    resolver.lifetime = 2
                    
                    answers = resolver.resolve(full_domain, 'A')
                    if answers:
                        subdomains.append(full_domain)
                        logger.debug(f"Found subdomain: {full_domain}")
                        
                except Exception:
                    pass  # Subdomain doesn't exist
                    
        # Create tasks for all subdomains
        tasks = [check_subdomain(sub) for sub in self.wordlists]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return subdomains
        
    async def _certificate_transparency_search(self, domain: str) -> List[str]:
        """Search certificate transparency logs"""
        subdomains = []
        
        try:
            # Use crt.sh API
            url = f"https://crt.sh/?q=%.{domain}&output=json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        for cert in data:
                            name_value = cert.get('name_value', '')
                            # Parse certificate names
                            names = name_value.split('\n')
                            for name in names:
                                name = name.strip()
                                if name.endswith(f'.{domain}') and name not in subdomains:
                                    subdomains.append(name)
                                    
        except Exception as e:
            logger.debug(f"Certificate transparency search failed: {e}")
            
        return subdomains
        
    async def _dns_zone_transfer(self, domain: str) -> List[str]:
        """Attempt DNS zone transfer"""
        subdomains = []
        
        try:
            # Get name servers for the domain
            resolver = dns.resolver.Resolver()
            ns_records = resolver.resolve(domain, 'NS')
            
            for ns in ns_records:
                try:
                    # Attempt zone transfer
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ns), domain))
                    for name in zone.nodes.keys():
                        subdomain = f"{name}.{domain}"
                        if subdomain not in subdomains:
                            subdomains.append(subdomain)
                            
                except Exception:
                    continue  # Zone transfer not allowed
                    
        except Exception as e:
            logger.debug(f"DNS zone transfer failed: {e}")
            
        return subdomains
        
    async def _search_engine_enumeration(self, domain: str) -> List[str]:
        """Search engine-based subdomain discovery"""
        subdomains = []
        
        # This would implement search engine queries
        # For now, return empty list to avoid rate limiting
        return subdomains
        
    async def _reverse_dns_lookup(self, domain: str) -> List[str]:
        """Reverse DNS lookup for IP ranges"""
        subdomains = []
        
        try:
            # Get IP addresses for the domain
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, 'A')
            
            for answer in answers:
                ip = str(answer)
                # Perform reverse DNS lookup
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                    if hostname.endswith(f'.{domain}') and hostname not in subdomains:
                        subdomains.append(hostname)
                except Exception:
                    continue
                    
        except Exception as e:
            logger.debug(f"Reverse DNS lookup failed: {e}")
            
        return subdomains
        
    async def _validate_subdomains(self, subdomains: List[str]) -> List[str]:
        """Validate discovered subdomains"""
        valid_subdomains = []
        semaphore = asyncio.Semaphore(20)
        
        async def validate_subdomain(subdomain: str):
            async with semaphore:
                try:
                    resolver = dns.resolver.Resolver()
                    resolver.timeout = 3
                    resolver.lifetime = 3
                    
                    answers = resolver.resolve(subdomain, 'A')
                    if answers:
                        valid_subdomains.append(subdomain)
                        
                except Exception:
                    pass
                    
        tasks = [validate_subdomain(sub) for sub in subdomains]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return valid_subdomains

class PortScanner:
    """Advanced port scanning capabilities"""
    
    def __init__(self):
        self.common_ports = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
            995: "POP3S", 1433: "MSSQL", 3306: "MySQL", 5432: "PostgreSQL",
            6379: "Redis", 27017: "MongoDB", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            9200: "Elasticsearch", 5984: "CouchDB", 8086: "InfluxDB",
            3000: "Node.js", 4000: "Development", 5000: "Flask", 8000: "Django",
            9000: "Admin Panel", 9090: "Prometheus", 3001: "React Dev",
            4200: "Angular Dev", 8888: "Jupyter", 9999: "Admin"
        }
        
    async def scan_ports(self, target: str, ports: List[int] = None) -> Dict[int, str]:
        """Scan ports on target"""
        if ports is None:
            ports = list(self.common_ports.keys())
            
        logger.info(f"🔍 Scanning {len(ports)} ports on {target}")
        
        open_ports = {}
        semaphore = asyncio.Semaphore(100)  # Limit concurrent connections
        
        async def scan_port(port: int):
            async with semaphore:
                try:
                    # Create connection with timeout
                    future = asyncio.open_connection(target, port)
                    reader, writer = await asyncio.wait_for(future, timeout=3)
                    
                    # Port is open
                    service = self.common_ports.get(port, "Unknown")
                    open_ports[port] = service
                    
                    writer.close()
                    await writer.wait_closed()
                    
                    logger.debug(f"Port {port} open on {target} ({service})")
                    
                except Exception:
                    pass  # Port is closed or filtered
                    
        # Scan all ports concurrently
        tasks = [scan_port(port) for port in ports]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info(f"✅ Found {len(open_ports)} open ports on {target}")
        return open_ports

class WebApplicationMapper:
    """Web application mapping and endpoint discovery"""
    
    def __init__(self):
        self.common_paths = [
            "/", "/admin", "/api", "/api/v1", "/api/v2", "/graphql", "/swagger",
            "/docs", "/documentation", "/openapi.json", "/swagger.json",
            "/robots.txt", "/sitemap.xml", "/.well-known/", "/health", "/status",
            "/login", "/signin", "/signup", "/register", "/logout", "/dashboard",
            "/panel", "/control", "/manage", "/config", "/settings", "/profile",
            "/user", "/users", "/account", "/accounts", "/customer", "/customers",
            "/upload", "/uploads", "/download", "/downloads", "/files", "/media",
            "/images", "/img", "/assets", "/static", "/public", "/private",
            "/backup", "/backups", "/archive", "/old", "/legacy", "/v1", "/v2",
            "/test", "/testing", "/dev", "/development", "/staging", "/beta",
            "/debug", "/trace", "/log", "/logs", "/audit", "/monitor", "/metrics"
        ]
        
    async def map_application(self, target: Target, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Comprehensive web application mapping"""
        logger.info(f"🗺️ Mapping web application: {target.url}")
        
        mapping_results = {
            "endpoints": [],
            "api_endpoints": [],
            "technologies": [],
            "forms": [],
            "javascript_files": [],
            "css_files": [],
            "images": [],
            "documents": []
        }
        
        # Discover endpoints
        endpoints = await self._discover_endpoints(target.url, session)
        mapping_results["endpoints"] = endpoints
        
        # Analyze main page
        main_page_info = await self._analyze_main_page(target.url, session)
        mapping_results.update(main_page_info)
        
        # Discover API endpoints
        api_endpoints = await self._discover_api_endpoints(target.url, session)
        mapping_results["api_endpoints"] = api_endpoints
        
        # Technology detection
        technologies = await self._detect_technologies(target.url, session)
        mapping_results["technologies"] = technologies
        
        return mapping_results
        
    async def _discover_endpoints(self, base_url: str, session: aiohttp.ClientSession) -> List[str]:
        """Discover web application endpoints"""
        discovered_endpoints = []
        semaphore = asyncio.Semaphore(20)
        
        async def check_endpoint(path: str):
            async with semaphore:
                try:
                    url = urljoin(base_url, path)
                    async with session.get(url, allow_redirects=False) as response:
                        if response.status in [200, 301, 302, 403, 401]:
                            discovered_endpoints.append(url)
                            logger.debug(f"Found endpoint: {url} ({response.status})")
                            
                except Exception:
                    pass
                    
        # Check common paths
        tasks = [check_endpoint(path) for path in self.common_paths]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        return discovered_endpoints
        
    async def _analyze_main_page(self, url: str, session: aiohttp.ClientSession) -> Dict[str, Any]:
        """Analyze main page for information"""
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract links, forms, scripts, etc.
                    links = [a.get('href') for a in soup.find_all('a', href=True)]
                    forms = [form.get('action') for form in soup.find_all('form', action=True)]
                    scripts = [script.get('src') for script in soup.find_all('script', src=True)]
                    stylesheets = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
                    
                    return {
                        "links": links,
                        "forms": forms,
                        "javascript_files": scripts,
                        "css_files": stylesheets
                    }
                    
        except Exception as e:
            logger.debug(f"Main page analysis failed: {e}")
            
        return {}
        
    async def _discover_api_endpoints(self, base_url: str, session: aiohttp.ClientSession) -> List[str]:
        """Discover API endpoints"""
        api_endpoints = []
        
        # Common API documentation endpoints
        api_docs = [
            "/swagger", "/swagger.json", "/swagger.yaml", "/swagger-ui",
            "/api-docs", "/api/docs", "/openapi.json", "/openapi.yaml",
            "/graphql", "/graphiql", "/api/graphql", "/v1/graphql",
            "/redoc", "/docs", "/documentation", "/api-documentation"
        ]
        
        for endpoint in api_docs:
            try:
                url = urljoin(base_url, endpoint)
                async with session.get(url) as response:
                    if response.status == 200:
                        api_endpoints.append(url)
                        
                        # Try to parse API documentation
                        content = await response.text()
                        if 'swagger' in content.lower() or 'openapi' in content.lower():
                            # Parse Swagger/OpenAPI spec
                            additional_endpoints = await self._parse_api_spec(content, base_url)
                            api_endpoints.extend(additional_endpoints)
                            
            except Exception:
                continue
                
        return api_endpoints
        
    async def _parse_api_spec(self, spec_content: str, base_url: str) -> List[str]:
        """Parse API specification for endpoints"""
        endpoints = []
        
        try:
            # Try to parse as JSON
            spec = json.loads(spec_content)
            
            # Extract paths from OpenAPI/Swagger spec
            if 'paths' in spec:
                for path in spec['paths'].keys():
                    full_url = urljoin(base_url, path)
                    endpoints.append(full_url)
                    
        except json.JSONDecodeError:
            # Try to extract endpoints using regex
            path_pattern = r'["\'](/[^"\']*)["\']'
            matches = re.findall(path_pattern, spec_content)
            
            for match in matches:
                if match.startswith('/api') or match.startswith('/v'):
                    full_url = urljoin(base_url, match)
                    endpoints.append(full_url)
                    
        return endpoints
        
    async def _detect_technologies(self, url: str, session: aiohttp.ClientSession) -> List[str]:
        """Detect web technologies"""
        technologies = []
        
        try:
            async with session.get(url) as response:
                headers = response.headers
                content = await response.text()
                
                # Server header
                server = headers.get('Server', '')
                if server:
                    technologies.append(f"Server: {server}")
                    
                # X-Powered-By header
                powered_by = headers.get('X-Powered-By', '')
                if powered_by:
                    technologies.append(f"Powered-By: {powered_by}")
                    
                # Content analysis
                if 'react' in content.lower():
                    technologies.append("React")
                if 'angular' in content.lower():
                    technologies.append("Angular")
                if 'vue' in content.lower():
                    technologies.append("Vue.js")
                if 'jquery' in content.lower():
                    technologies.append("jQuery")
                if 'bootstrap' in content.lower():
                    technologies.append("Bootstrap")
                    
        except Exception as e:
            logger.debug(f"Technology detection failed: {e}")
            
        return technologies

class MobileAppAnalyzer:
    """Mobile application analysis"""
    
    async def discover_mobile_apps(self, domain: str) -> List[str]:
        """Discover mobile applications"""
        mobile_apps = []
        
        # Common mobile app download patterns
        app_patterns = [
            f"https://play.google.com/store/apps/details?id=com.{domain}",
            f"https://apps.apple.com/app/{domain}",
            f"https://{domain}/app",
            f"https://{domain}/mobile",
            f"https://{domain}/download",
            f"https://{domain}/android",
            f"https://{domain}/ios"
        ]
        
        # This would implement actual mobile app discovery
        # For now, return the patterns to check
        return app_patterns

class TargetSystem:
    """Main target acquisition and reconnaissance system"""
    
    def __init__(self):
        self.subdomain_enumerator = SubdomainEnumerator()
        self.port_scanner = PortScanner()
        self.web_mapper = WebApplicationMapper()
        self.mobile_analyzer = MobileAppAnalyzer()
        
    async def initialize(self):
        """Initialize target system"""
        logger.info("🎯 Target system initialized")
        
    async def acquire_targets(self, target_urls: List[str]) -> List[Target]:
        """Comprehensive target acquisition and reconnaissance"""
        logger.info(f"🎯 Acquiring and analyzing {len(target_urls)} target(s)")
        
        targets = []
        
        for url in target_urls:
            try:
                target = await self._analyze_single_target(url)
                targets.append(target)
            except Exception as e:
                logger.error(f"Failed to analyze target {url}: {e}")
                
        logger.info(f"✅ Successfully analyzed {len(targets)} target(s)")
        return targets
        
    async def _analyze_single_target(self, url: str) -> Target:
        """Comprehensive analysis of a single target"""
        logger.info(f"🔍 Analyzing target: {url}")
        
        # Parse URL
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path
        
        # Remove www prefix if present
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Create target object
        target = Target(url=url, domain=domain)
        
        # Get IP addresses
        target.ip_addresses = await self._resolve_ip_addresses(domain)
        
        # Enumerate subdomains
        target.subdomains = await self.subdomain_enumerator.enumerate_subdomains(domain)
        
        # Port scanning
        if target.ip_addresses:
            target.ports = await self.port_scanner.scan_ports(target.ip_addresses[0])
            
        # Web application mapping
        if 80 in target.ports or 443 in target.ports:
            from .ghost_mode import GhostMode
            ghost = GhostMode()
            session = await ghost.get_anonymous_session()
            
            try:
                web_info = await self.web_mapper.map_application(target, session)
                target.endpoints = web_info.get("endpoints", [])
                target.api_endpoints = web_info.get("api_endpoints", [])
                target.technologies = web_info.get("technologies", [])
            finally:
                await session.close()
                
        # Mobile app discovery
        target.mobile_apps = await self.mobile_analyzer.discover_mobile_apps(domain)
        
        # WHOIS information
        target.whois_info = await self._get_whois_info(domain)
        
        logger.info(f"✅ Target analysis complete: {domain}")
        logger.info(f"   - IPs: {len(target.ip_addresses)}")
        logger.info(f"   - Subdomains: {len(target.subdomains)}")
        logger.info(f"   - Open ports: {len(target.ports)}")
        logger.info(f"   - Endpoints: {len(target.endpoints)}")
        logger.info(f"   - API endpoints: {len(target.api_endpoints)}")
        
        return target
        
    async def _resolve_ip_addresses(self, domain: str) -> List[str]:
        """Resolve IP addresses for domain"""
        ip_addresses = []
        
        try:
            resolver = dns.resolver.Resolver()
            answers = resolver.resolve(domain, 'A')
            
            for answer in answers:
                ip_addresses.append(str(answer))
                
        except Exception as e:
            logger.debug(f"IP resolution failed for {domain}: {e}")
            
        return ip_addresses
        
    async def _get_whois_info(self, domain: str) -> Dict:
        """Get WHOIS information for domain"""
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date) if w.creation_date else None,
                "expiration_date": str(w.expiration_date) if w.expiration_date else None,
                "name_servers": w.name_servers
            }
        except Exception as e:
            logger.debug(f"WHOIS lookup failed for {domain}: {e}")
            return {}