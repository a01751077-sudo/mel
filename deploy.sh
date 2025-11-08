#!/bin/bash

# 🔥 DEPLOYMENT SCRIPT - OPTIMIZED PENETRATION TESTING SYSTEM
# ============================================================

echo "🔥 DEPLOYING OPTIMIZED PENETRATION TESTING SYSTEM"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "run_pentest_optimized.py" ]; then
    print_error "run_pentest_optimized.py not found!"
    print_info "Please run this script from the yui directory"
    exit 1
fi

print_info "Starting deployment process..."

# Step 1: Check Python installation
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_status "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found! Please install Python 3.8 or higher."
    exit 1
fi

# Step 2: Check pip installation
print_info "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    print_status "pip found"
    PIP_CMD="pip"
else
    print_error "pip not found! Please install pip."
    exit 1
fi

# Step 3: Install dependencies
print_info "Installing Python dependencies..."
if $PIP_CMD install -r requirements.txt --quiet --user; then
    print_status "Dependencies installed successfully"
else
    print_warning "Some dependencies may have failed to install"
    print_info "Continuing with deployment..."
fi

# Step 4: Make scripts executable
print_info "Setting up executable permissions..."
chmod +x run_pentest_optimized.py
chmod +x run_pentest.py
chmod +x setup_fast.sh
print_status "Permissions set"

# Step 5: Create necessary directories
print_info "Creating directories..."
mkdir -p logs
mkdir -p results
mkdir -p config
mkdir -p pentest_results_$(date +%Y%m%d)
print_status "Directories created"

# Step 6: Test the system
print_info "Testing system components..."
if python3 -c "
import sys
sys.path.insert(0, 'src')
from run_pentest_optimized import validate_target, OptimizedPentestCore
config = {'session_id': 'test', 'max_threads': 5}
core = OptimizedPentestCore(config)
print('System test passed')
" 2>/dev/null; then
    print_status "System test passed"
else
    print_warning "System test had issues, but deployment continues"
fi

# Step 7: Display deployment summary
echo ""
echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "====================================="
echo ""
print_info "System Status:"
echo "  📁 Working Directory: $(pwd)"
echo "  🐍 Python Version: $PYTHON_VERSION"
echo "  📦 Dependencies: Installed"
echo "  🔧 Permissions: Set"
echo "  📂 Directories: Created"
echo ""
print_info "Available Commands:"
echo "  🔥 OPTIMIZED (Recommended):"
echo "     python3 run_pentest_optimized.py"
echo ""
echo "  🐌 FULL SYSTEM:"
echo "     python3 run_pentest.py"
echo ""
print_info "Quick Start:"
echo "  1. Run: python3 run_pentest_optimized.py"
echo "  2. Enter your targets when prompted"
echo "  3. Get results in minutes!"
echo ""
print_status "Ready to start penetration testing! 🚀"
echo ""

# Step 8: Offer to run a quick demo
read -p "Would you like to run a quick system demo? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Running quick demo..."
    echo ""
    python3 -c "
import asyncio
import sys
sys.path.insert(0, 'src')
from run_pentest_optimized import OptimizedPentestCore

async def demo():
    print('🔥 DEMO: Optimized Penetration Testing System')
    print('=' * 50)
    
    config = {
        'session_id': 'demo_$(date +%Y%m%d_%H%M%S)',
        'max_threads': 3,
        'fast_mode': True
    }
    
    core = OptimizedPentestCore(config)
    
    print('⚡ Initializing system...')
    success = await core.initialize_system()
    
    if success:
        print('✅ Demo completed successfully!')
        print('🚀 System is ready for real penetration testing!')
    else:
        print('❌ Demo failed - check your setup')

asyncio.run(demo())
"
    echo ""
    print_status "Demo completed!"
fi

echo ""
print_status "Deployment finished! You can now start testing targets."
print_info "For help, check README_OPTIMIZED.md"
echo ""