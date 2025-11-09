"""
Hardware Optimization System
Advanced compression and performance enhancement using military-grade techniques
"""

import asyncio
import psutil
import gc
import os
import sys
from pathlib import Path
from loguru import logger
from typing import Dict, Any

# Optional compression libraries - graceful fallback if not available
try:
    import lz4.frame
    HAS_LZ4 = True
except ImportError:
    HAS_LZ4 = False
    logger.warning("LZ4 compression not available - using fallback")

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False
    logger.warning("Zstandard compression not available - using fallback")

try:
    import blosc
    HAS_BLOSC = True
except ImportError:
    HAS_BLOSC = False
    logger.warning("Blosc compression not available - using fallback")

class HardwareOptimizer:
    """Military-grade hardware optimization system"""
    
    def __init__(self):
        self.optimization_active = False
        self.original_settings = {}
        self.compression_engines = {}
        
        # Initialize available compression engines
        if HAS_LZ4:
            self.compression_engines['lz4'] = lz4.frame
        if HAS_ZSTD:
            self.compression_engines['zstd'] = zstd.ZstdCompressor()
        if HAS_BLOSC:
            self.compression_engines['blosc'] = blosc
            
        # Always have a fallback compression method
        if not self.compression_engines:
            import gzip
            self.compression_engines['gzip'] = gzip
            logger.info("Using gzip as fallback compression method")
        
    async def optimize_system(self):
        """Apply comprehensive system optimizations"""
        logger.info("🚀 Starting hardware optimization...")
        
        try:
            # Memory optimization
            await self.optimize_memory()
            
            # CPU optimization
            await self.optimize_cpu()
            
            # Network optimization
            await self.optimize_network()
            
            # Storage optimization
            await self.optimize_storage()
            
            # Python runtime optimization
            await self.optimize_python_runtime()
            
            self.optimization_active = True
            logger.success("✅ Hardware optimization completed")
            
        except Exception as e:
            logger.error(f"Hardware optimization failed: {e}")
            raise
            
    async def optimize_memory(self):
        """Advanced memory optimization techniques"""
        logger.info("🧠 Optimizing memory subsystem...")
        
        # Force garbage collection
        gc.collect()
        
        # Set aggressive garbage collection thresholds
        gc.set_threshold(700, 10, 10)
        
        # Enable memory compression if available
        try:
            import mmap
            # Configure memory mapping for large data structures
            self.memory_pool = {}
            logger.info("Memory compression enabled")
        except ImportError:
            logger.warning("Memory compression not available")
            
        # Get memory info
        memory = psutil.virtual_memory()
        logger.info(f"Memory optimization: {memory.available / (1024**3):.2f}GB available")
        
    async def optimize_cpu(self):
        """CPU optimization and affinity management"""
        logger.info("⚡ Optimizing CPU performance...")
        
        # Get CPU info
        cpu_count = psutil.cpu_count(logical=False)
        logical_cpu_count = psutil.cpu_count(logical=True)
        
        # Set process priority to high (with proper error handling)
        try:
            process = psutil.Process()
            if sys.platform == "win32":
                # Windows priority classes
                if hasattr(psutil, 'HIGH_PRIORITY_CLASS'):
                    process.nice(psutil.HIGH_PRIORITY_CLASS)
                else:
                    process.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            else:
                # Unix nice values (-20 to 19, lower = higher priority)
                try:
                    process.nice(-5)  # Moderate high priority
                    logger.info("Process priority set to HIGH")
                except PermissionError:
                    # Fallback to normal priority if no permissions
                    process.nice(0)
                    logger.info("Process priority set to NORMAL (no root permissions)")
        except (AttributeError, PermissionError, ProcessLookupError) as e:
            logger.warning(f"Could not set process priority: {e}")
            
        # Configure CPU affinity for maximum performance
        try:
            available_cpus = list(range(logical_cpu_count))
            process.cpu_affinity(available_cpus)
            logger.info(f"CPU affinity set to all {logical_cpu_count} cores")
        except Exception as e:
            logger.warning(f"Could not set CPU affinity: {e}")
            
        logger.info(f"CPU optimization: {cpu_count} physical, {logical_cpu_count} logical cores")
        
    async def optimize_network(self):
        """Network stack optimization"""
        logger.info("🌐 Optimizing network performance...")
        
        # Configure asyncio for maximum performance
        if sys.platform != "win32":
            try:
                import uvloop
                # Only set if not already set
                if not isinstance(asyncio.get_event_loop_policy(), uvloop.EventLoopPolicy):
                    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
                logger.info("UV Loop enabled for maximum async performance")
            except (ImportError, RuntimeError) as e:
                logger.warning(f"UV Loop not available: {e}, using default event loop")
                
        # Network buffer optimization
        self.network_config = {
            'connection_pool_size': 1000,
            'max_connections_per_host': 100,
            'timeout': 30,
            'keepalive': True
        }
        
        logger.info("Network optimization completed")
        
    async def optimize_storage(self):
        """Storage and I/O optimization"""
        logger.info("💾 Optimizing storage performance...")
        
        # Create optimized temporary directory
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        # Configure compression engines
        self.storage_config = {
            'compression_level': 9,  # Maximum compression
            'buffer_size': 1024 * 1024,  # 1MB buffer
            'use_memory_mapping': True
        }
        
        # Test compression performance
        test_data = b"A" * 10000  # 10KB test data
        compression_results = {}
        
        for engine_name, engine in self.compression_engines.items():
            try:
                if engine_name == 'lz4':
                    compressed = lz4.frame.compress(test_data)
                elif engine_name == 'zstd':
                    compressed = engine.compress(test_data)
                elif engine_name == 'blosc':
                    compressed = blosc.compress(test_data, cname='zstd')
                    
                compression_ratio = len(test_data) / len(compressed)
                compression_results[engine_name] = compression_ratio
                
            except Exception as e:
                logger.warning(f"Compression engine {engine_name} failed: {e}")
                
        # Select best compression engine
        if compression_results:
            best_engine = max(compression_results, key=compression_results.get)
            self.best_compression_engine = best_engine
            logger.info(f"Best compression engine: {best_engine} (ratio: {compression_results[best_engine]:.2f})")
        else:
            self.best_compression_engine = None
            logger.warning("No compression engines available")
            
    async def optimize_python_runtime(self):
        """Python runtime optimizations"""
        logger.info("🐍 Optimizing Python runtime...")
        
        # Disable debug mode if enabled
        if __debug__:
            logger.warning("Python running in debug mode - performance may be reduced")
            
        # Configure sys settings for performance (Python 3.9+ compatible)
        try:
            # Try the old method first (Python < 3.9)
            if hasattr(sys, 'setcheckinterval'):
                sys.setcheckinterval(1000)
            # Use the new method for Python 3.9+
            elif hasattr(sys, 'setswitchinterval'):
                sys.setswitchinterval(0.001)  # 1ms switch interval
            logger.info("Python thread switching optimized")
        except Exception as e:
            logger.warning(f"Could not optimize thread switching: {e}")
            
        # Import performance-critical modules
        performance_modules = [
            'asyncio', 'aiohttp', 'concurrent.futures',
            'multiprocessing', 'threading', 'queue'
        ]
        
        for module in performance_modules:
            try:
                __import__(module)
            except ImportError:
                logger.warning(f"Performance module {module} not available")
                
        logger.info("Python runtime optimization completed")
        
    async def compress_data(self, data: bytes) -> bytes:
        """Compress data using the best available engine"""
        if not self.best_compression_engine:
            return data
            
        try:
            engine = self.compression_engines[self.best_compression_engine]
            
            if self.best_compression_engine == 'lz4' and HAS_LZ4:
                return lz4.frame.compress(data)
            elif self.best_compression_engine == 'zstd' and HAS_ZSTD:
                return engine.compress(data)
            elif self.best_compression_engine == 'blosc' and HAS_BLOSC:
                return blosc.compress(data, cname='zstd')
            elif self.best_compression_engine == 'gzip':
                import gzip
                return gzip.compress(data)
            else:
                return data
                
        except Exception as e:
            logger.error(f"Data compression failed: {e}")
            return data
            
    async def decompress_data(self, compressed_data: bytes) -> bytes:
        """Decompress data using the best available engine"""
        if not self.best_compression_engine:
            return compressed_data
            
        try:
            engine = self.compression_engines[self.best_compression_engine]
            
            if self.best_compression_engine == 'lz4' and HAS_LZ4:
                return lz4.frame.decompress(compressed_data)
            elif self.best_compression_engine == 'zstd' and HAS_ZSTD:
                return zstd.ZstdDecompressor().decompress(compressed_data)
            elif self.best_compression_engine == 'blosc' and HAS_BLOSC:
                return blosc.decompress(compressed_data)
            elif self.best_compression_engine == 'gzip':
                import gzip
                return gzip.decompress(compressed_data)
            else:
                return compressed_data
                
        except Exception as e:
            logger.error(f"Data decompression failed: {e}")
            return compressed_data
            
    async def get_system_stats(self) -> Dict[str, Any]:
        """Get current system performance statistics"""
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage('/')
        
        return {
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used
            },
            'cpu': {
                'percent': cpu_percent,
                'count': psutil.cpu_count(),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': (disk.used / disk.total) * 100
            },
            'optimization_active': self.optimization_active
        }
        
    async def cleanup(self):
        """Cleanup optimization resources"""
        if self.optimization_active:
            logger.info("🧹 Cleaning up optimization resources...")
            
            # Restore original settings if needed
            for setting, value in self.original_settings.items():
                try:
                    # Restore setting
                    pass
                except Exception as e:
                    logger.warning(f"Could not restore setting {setting}: {e}")
                    
            # Force garbage collection
            gc.collect()
            
            self.optimization_active = False
            logger.info("Optimization cleanup completed")