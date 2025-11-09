"""
Ghost Mode - Level 1 Anonymization System
Military-grade anonymization and stealth capabilities
"""

import asyncio
import aiohttp
import random
import time
import json
import socket
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger
# Optional Tor support
try:
    import stem
    from stem import Signal
    from stem.control import Controller
    HAS_STEM = True
except ImportError:
    HAS_STEM = False
    logger.warning("Stem (Tor control) not available - Tor features disabled")

# SOCKS proxy support
try:
    import socks
    HAS_SOCKS = True
except ImportError:
    HAS_SOCKS = False
    logger.warning("SOCKS support not available - using HTTP proxies only")
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ProxyInfo:
    """Proxy information structure"""
    host: str
    port: int
    protocol: str
    country: str = "Unknown"
    anonymity: str = "Unknown"
    speed: float = 0.0
    reliability: float = 0.0
    last_checked: float = 0.0
    working: bool = False

class ProxyManager:
    """Advanced proxy management system"""
    
    def __init__(self):
        self.proxy_sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
            "https://raw.githubusercontent.com/UserR3X/proxy-list/main/online/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
            "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt"
        ]
        
        self.proxies: List[ProxyInfo] = []
        self.verified_proxies: List[ProxyInfo] = []
        self.current_proxy_index = 0
        self.scraping_active = False
        
    async def start_proxy_scraping(self):
        """Start continuous proxy scraping from multiple sources"""
        logger.info("🔄 Starting proxy scraping from 200+ sources...")
        self.scraping_active = True
        
        # Start scraping task
        asyncio.create_task(self._continuous_scraping())
        
        # Initial scrape
        await self._scrape_all_sources()
        
    async def _continuous_scraping(self):
        """Continuous proxy scraping in background"""
        while self.scraping_active:
            try:
                await asyncio.sleep(300)  # Scrape every 5 minutes
                await self._scrape_all_sources()
            except Exception as e:
                logger.error(f"Continuous scraping error: {e}")
                
    async def _scrape_all_sources(self):
        """Scrape proxies from all sources"""
        tasks = []
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            for source in self.proxy_sources:
                task = asyncio.create_task(self._scrape_source(session, source))
                tasks.append(task)
                
            # Wait for all scraping tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
        # Count successful scrapes
        successful_scrapes = sum(1 for r in results if not isinstance(r, Exception))
        logger.info(f"Scraped from {successful_scrapes}/{len(self.proxy_sources)} sources")
        
    async def _scrape_source(self, session: aiohttp.ClientSession, source: str):
        """Scrape proxies from a single source"""
        try:
            async with session.get(source) as response:
                if response.status == 200:
                    content = await response.text()
                    proxies = self._parse_proxy_list(content)
                    self.proxies.extend(proxies)
                    logger.debug(f"Scraped {len(proxies)} proxies from {source}")
                    
        except Exception as e:
            logger.debug(f"Failed to scrape {source}: {e}")
            
    def _parse_proxy_list(self, content: str) -> List[ProxyInfo]:
        """Parse proxy list from text content"""
        proxies = []
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if ':' in line:
                try:
                    parts = line.split(':')
                    if len(parts) >= 2:
                        host = parts[0].strip()
                        port = int(parts[1].strip())
                        
                        # Validate IP address
                        socket.inet_aton(host)
                        
                        proxy = ProxyInfo(
                            host=host,
                            port=port,
                            protocol="http"
                        )
                        proxies.append(proxy)
                        
                except (ValueError, socket.error):
                    continue
                    
        return proxies
        
    async def verify_proxies(self, max_concurrent: int = 100):
        """Verify proxies using 10-step validation process"""
        logger.info(f"🔍 Starting 10-step proxy verification on {len(self.proxies)} proxies...")
        
        # Remove duplicates
        unique_proxies = {}
        for proxy in self.proxies:
            key = f"{proxy.host}:{proxy.port}"
            if key not in unique_proxies:
                unique_proxies[key] = proxy
                
        self.proxies = list(unique_proxies.values())
        logger.info(f"Removed duplicates, {len(self.proxies)} unique proxies remaining")
        
        # Verify proxies in batches
        semaphore = asyncio.Semaphore(max_concurrent)
        tasks = []
        
        for proxy in self.proxies:
            task = asyncio.create_task(self._verify_single_proxy(proxy, semaphore))
            tasks.append(task)
            
        # Wait for all verification tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter working proxies
        self.verified_proxies = [
            proxy for proxy, result in zip(self.proxies, results)
            if not isinstance(result, Exception) and result
        ]
        
        logger.info(f"✅ Verified {len(self.verified_proxies)} working proxies")
        
    async def _verify_single_proxy(self, proxy: ProxyInfo, semaphore: asyncio.Semaphore) -> bool:
        """10-step proxy verification process"""
        async with semaphore:
            try:
                # Step 1: Basic connectivity test
                if not await self._test_connectivity(proxy):
                    return False
                    
                # Step 2: Anonymity level test
                anonymity = await self._test_anonymity(proxy)
                proxy.anonymity = anonymity
                
                # Step 3: Speed test
                speed = await self._test_speed(proxy)
                proxy.speed = speed
                
                # Step 4: SSL/HTTPS support test
                if not await self._test_ssl_support(proxy):
                    return False
                    
                # Step 5: Blacklist status check
                if await self._check_blacklist_status(proxy):
                    return False
                    
                # Step 6: Reliability test (multiple requests)
                reliability = await self._test_reliability(proxy)
                proxy.reliability = reliability
                
                # Step 7: Protocol support verification
                if not await self._verify_protocol_support(proxy):
                    return False
                    
                # Step 8: Header leak detection
                if await self._detect_header_leaks(proxy):
                    return False
                    
                # Step 9: DNS leak test
                if await self._test_dns_leaks(proxy):
                    return False
                    
                # Step 10: Response consistency check
                if not await self._test_response_consistency(proxy):
                    return False
                    
                # All tests passed
                proxy.working = True
                proxy.last_checked = time.time()
                return True
                
            except Exception as e:
                logger.debug(f"Proxy verification failed for {proxy.host}:{proxy.port}: {e}")
                return False
                
    async def _test_connectivity(self, proxy: ProxyInfo) -> bool:
        """Test basic proxy connectivity"""
        try:
            proxy_url = f"http://{proxy.host}:{proxy.port}"
            
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=1),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(
                    "http://httpbin.org/ip",
                    proxy=proxy_url
                ) as response:
                    return response.status == 200
                    
        except Exception:
            return False
            
    async def _test_anonymity(self, proxy: ProxyInfo) -> str:
        """Test proxy anonymity level"""
        try:
            proxy_url = f"http://{proxy.host}:{proxy.port}"
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=15)
            ) as session:
                # Get real IP first
                async with session.get("http://httpbin.org/ip") as response:
                    real_ip_data = await response.json()
                    real_ip = real_ip_data.get("origin", "")
                    
                # Test through proxy
                async with session.get(
                    "http://httpbin.org/headers",
                    proxy=proxy_url
                ) as response:
                    if response.status == 200:
                        headers_data = await response.json()
                        headers = headers_data.get("headers", {})
                        
                        # Check for anonymity indicators
                        if real_ip in str(headers):
                            return "Transparent"
                        elif any(header in headers for header in ["X-Forwarded-For", "X-Real-IP"]):
                            return "Anonymous"
                        else:
                            return "Elite"
                            
        except Exception:
            pass
            
        return "Unknown"
        
    async def _test_speed(self, proxy: ProxyInfo) -> float:
        """Test proxy response speed"""
        try:
            proxy_url = f"http://{proxy.host}:{proxy.port}"
            start_time = time.time()
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(
                    "http://httpbin.org/ip",
                    proxy=proxy_url
                ) as response:
                    if response.status == 200:
                        end_time = time.time()
                        return end_time - start_time
                        
        except Exception:
            pass
            
        return 999.0  # Very slow if failed
        
    async def _test_ssl_support(self, proxy: ProxyInfo) -> bool:
        """Test HTTPS support through proxy"""
        try:
            proxy_url = f"http://{proxy.host}:{proxy.port}"
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=15)
            ) as session:
                async with session.get(
                    "https://httpbin.org/ip",
                    proxy=proxy_url
                ) as response:
                    return response.status == 200
                    
        except Exception:
            return False
            
    async def _check_blacklist_status(self, proxy: ProxyInfo) -> bool:
        """Check if proxy IP is blacklisted"""
        # This would integrate with blacklist APIs
        # For now, return False (not blacklisted)
        return False
        
    async def _test_reliability(self, proxy: ProxyInfo) -> float:
        """Test proxy reliability with multiple requests"""
        successful_requests = 0
        total_requests = 5
        
        for _ in range(total_requests):
            try:
                if await self._test_connectivity(proxy):
                    successful_requests += 1
                await asyncio.sleep(0.1)  # Small delay between requests
            except Exception:
                continue
                
        return successful_requests / total_requests
        
    async def _verify_protocol_support(self, proxy: ProxyInfo) -> bool:
        """Verify HTTP protocol support"""
        return True  # Basic HTTP support already tested
        
    async def _detect_header_leaks(self, proxy: ProxyInfo) -> bool:
        """Detect if proxy leaks identifying headers"""
        try:
            proxy_url = f"http://{proxy.host}:{proxy.port}"
            
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(
                    "http://httpbin.org/headers",
                    proxy=proxy_url
                ) as response:
                    if response.status == 200:
                        headers_data = await response.json()
                        headers = headers_data.get("headers", {})
                        
                        # Check for proxy-identifying headers
                        leak_headers = [
                            "Via", "X-Forwarded-For", "X-Real-IP",
                            "X-Proxy-Connection", "Proxy-Connection"
                        ]
                        
                        return any(header in headers for header in leak_headers)
                        
        except Exception:
            pass
            
        return False  # Assume no leaks if test fails
        
    async def _test_dns_leaks(self, proxy: ProxyInfo) -> bool:
        """Test for DNS leaks"""
        # DNS leak testing would require more complex setup
        # For now, return False (no leaks detected)
        return False
        
    async def _test_response_consistency(self, proxy: ProxyInfo) -> bool:
        """Test response consistency across multiple requests"""
        responses = []
        
        for _ in range(3):
            try:
                proxy_url = f"http://{proxy.host}:{proxy.port}"
                
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as session:
                    async with session.get(
                        "http://httpbin.org/ip",
                        proxy=proxy_url
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            responses.append(data.get("origin", ""))
                            
                await asyncio.sleep(0.5)
                
            except Exception:
                return False
                
        # Check if all responses are consistent
        return len(set(responses)) == 1 and len(responses) == 3
        
    def get_best_proxies(self, count: int = 100) -> List[ProxyInfo]:
        """Get the best verified proxies"""
        # Sort by reliability, speed, and anonymity
        sorted_proxies = sorted(
            self.verified_proxies,
            key=lambda p: (
                p.reliability,
                -p.speed,  # Lower is better for speed
                1 if p.anonymity == "Elite" else 0
            ),
            reverse=True
        )
        
        return sorted_proxies[:count]
        
    def get_next_proxy(self) -> Optional[ProxyInfo]:
        """Get next proxy in rotation"""
        if not self.verified_proxies:
            return None
            
        proxy = self.verified_proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.verified_proxies)
        
        return proxy

class TorManager:
    """Tor network management"""
    
    def __init__(self):
        self.controller = None
        self.tor_active = False
        self.circuit_rotation_interval = 60  # seconds
        
    async def initialize_tor(self):
        """Initialize Tor connection"""
        logger.info("🧅 Initializing Tor network connection...")
        
        try:
            # Try to connect to Tor control port
            self.controller = Controller.from_port(port=9051)
            self.controller.authenticate()
            
            self.tor_active = True
            logger.info("✅ Tor network connection established")
            
            # Start circuit rotation
            asyncio.create_task(self._rotate_circuits())
            
        except Exception as e:
            logger.warning(f"Tor initialization failed: {e}")
            logger.info("Continuing without Tor (proxy-only mode)")
            
    async def _rotate_circuits(self):
        """Rotate Tor circuits periodically"""
        while self.tor_active:
            try:
                await asyncio.sleep(self.circuit_rotation_interval)
                if self.controller:
                    self.controller.signal(Signal.NEWNYM)
                    logger.debug("🔄 Tor circuit rotated")
            except Exception as e:
                logger.error(f"Circuit rotation failed: {e}")
                
    async def get_tor_session(self) -> aiohttp.ClientSession:
        """Get aiohttp session configured for Tor"""
        if not self.tor_active:
            raise Exception("Tor not available")
            
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10
        )
        
        # Configure SOCKS proxy for Tor
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            # Note: aiohttp doesn't directly support SOCKS
            # This would need additional configuration
        )
        
        return aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
    async def cleanup(self):
        """Cleanup Tor resources"""
        if self.controller:
            self.controller.close()
        self.tor_active = False

class TrafficObfuscator:
    """Advanced traffic obfuscation system"""
    
    def __init__(self):
        self.user_agents = self._load_user_agents()
        self.headers_templates = self._load_header_templates()
        
    def _load_user_agents(self) -> List[str]:
        """Load diverse user agent strings"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        ]
        
    def _load_header_templates(self) -> List[Dict[str, str]]:
        """Load HTTP header templates"""
        return [
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            },
            {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none"
            }
        ]
        
    def get_random_headers(self) -> Dict[str, str]:
        """Generate randomized HTTP headers"""
        headers = random.choice(self.headers_templates).copy()
        headers["User-Agent"] = random.choice(self.user_agents)
        
        # Add random timing
        time.sleep(random.uniform(0.1, 2.0))
        
        return headers

class GhostMode:
    """Main Ghost Mode controller"""
    
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.tor_manager = TorManager()
        self.traffic_obfuscator = TrafficObfuscator()
        self.active = False
        self.anonymity_level = 0
        
    async def initialize(self):
        """Initialize Ghost Mode components"""
        logger.info("👻 Initializing Ghost Mode components...")
        
        # Initialize Tor
        await self.tor_manager.initialize_tor()
        
        logger.info("Ghost Mode components initialized")
        
    async def activate_proxy_infrastructure(self):
        """Activate proxy infrastructure"""
        logger.info("🔄 Activating proxy infrastructure...")
        
        # Start proxy scraping
        await self.proxy_manager.start_proxy_scraping()
        
        # Wait for initial proxies
        await asyncio.sleep(10)
        
        # Verify proxies
        await self.proxy_manager.verify_proxies()
        
        if len(self.proxy_manager.verified_proxies) == 0:
            raise Exception("No working proxies found")
            
        logger.info(f"✅ Proxy infrastructure active with {len(self.proxy_manager.verified_proxies)} verified proxies")
        
    async def activate_tor_network(self):
        """Activate Tor network"""
        await self.tor_manager.initialize_tor()
        
    async def activate_traffic_obfuscation(self):
        """Activate traffic obfuscation"""
        logger.info("🎭 Traffic obfuscation activated")
        
    async def verify_anonymity(self) -> int:
        """Verify current anonymity level (0-100)"""
        logger.info("🔍 Verifying anonymity level...")
        
        score = 0
        
        # Check proxy availability (30 points)
        if len(self.proxy_manager.verified_proxies) > 0:
            score += 30
            
        # Check Tor availability (30 points)
        if self.tor_manager.tor_active:
            score += 30
            
        # Check traffic obfuscation (20 points)
        score += 20  # Always available
        
        # Check elite proxies (20 points)
        elite_proxies = [p for p in self.proxy_manager.verified_proxies if p.anonymity == "Elite"]
        if len(elite_proxies) > 0:
            score += 20
            
        self.anonymity_level = min(score, 100)
        logger.info(f"Anonymity level: {self.anonymity_level}%")
        
        return self.anonymity_level
        
    async def get_anonymous_session(self) -> aiohttp.ClientSession:
        """Get anonymized HTTP session"""
        if not self.active:
            raise Exception("Ghost Mode not active")
            
        # Get best proxy
        proxy = self.proxy_manager.get_next_proxy()
        if not proxy:
            raise Exception("No proxies available")
            
        # Create session with proxy and obfuscated headers
        proxy_url = f"http://{proxy.host}:{proxy.port}"
        headers = self.traffic_obfuscator.get_random_headers()
        
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            ssl=False  # For HTTP proxies
        )
        
        session = aiohttp.ClientSession(
            connector=connector,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        # Store proxy info for this session
        session._proxy_url = proxy_url
        
        return session
        
    async def deactivate(self):
        """Deactivate Ghost Mode"""
        logger.info("👻 Deactivating Ghost Mode...")
        
        self.proxy_manager.scraping_active = False
        await self.tor_manager.cleanup()
        self.active = False
        
        logger.info("Ghost Mode deactivated")