#!/bin/bash

# 🔥 FAST SETUP SCRIPT FOR OPTIMIZED PENETRATION TESTING SYSTEM
# ==============================================================

echo "🔥 FAST SETUP - OPTIMIZED PENETRATION TESTING SYSTEM"
echo "====================================================="

# Check if we're in the right directory
if [ ! -f "run_pentest_optimized.py" ]; then
    echo "❌ Error: run_pentest_optimized.py not found!"
    echo "Please run this script from the yui directory"
    exit 1
fi

echo "📦 Installing required dependencies..."

# Install Python dependencies
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt --quiet
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt --quiet
else
    echo "❌ Error: pip not found! Please install Python pip first."
    exit 1
fi

echo "✅ Dependencies installed successfully!"

# Make scripts executable
chmod +x run_pentest_optimized.py
chmod +x run_pentest.py

echo "🔧 Setting up directories..."
mkdir -p logs
mkdir -p results
mkdir -p config

echo "✅ Setup completed successfully!"
echo ""
echo "🚀 READY TO RUN!"
echo "================"
echo ""
echo "Choose your launcher:"
echo "1. 🔥 OPTIMIZED (Recommended): python3 run_pentest_optimized.py"
echo "   - Fast parallel processing"
echo "   - 5-15 minutes total time"
echo "   - No OTIS overhead"
echo "   - Maximum efficiency"
echo ""
echo "2. 🐌 FULL SYSTEM: python3 run_pentest.py"
echo "   - Complete OTIS integration"
echo "   - 15-45 minutes per target"
echo "   - Full feature set"
echo "   - Higher resource usage"
echo ""
echo "💡 For best performance, use the OPTIMIZED version!"
echo ""