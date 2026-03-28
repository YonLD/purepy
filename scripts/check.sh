#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

echo "========================================"
echo "Running Python Code Quality Checks"
echo "========================================"

echo ""
echo "1. Checking Python syntax..."
python3 -m py_compile pure/*.py pure/core/*.py
if [ $? -eq 0 ]; then
    echo "   ✓ Syntax check passed"
else
    echo "   ✗ Syntax check failed"
    exit 1
fi

echo ""
echo "2. Running flake8..."
if command -v flake8 &> /dev/null; then
    flake8 pure/ --max-line-length=88 --exclude=pure/__init__.py
    if [ $? -eq 0 ]; then
        echo "   ✓ flake8 check passed"
    else
        echo "   ✗ flake8 check failed"
        exit 1
    fi
else
    echo "   ! flake8 not installed. Run: pip install flake8"
fi

echo ""
echo "3. Running mypy..."
if command -v mypy &> /dev/null; then
    mypy pure/ --ignore-missing-imports
    if [ $? -eq 0 ]; then
        echo "   ✓ mypy check passed"
    else
        echo "   ✗ mypy check failed"
    fi
else
    echo "   ! mypy not installed. Run: pip install mypy"
fi

echo ""
echo "4. Checking black formatting..."
if command -v black &> /dev/null; then
    black --check pure/
    if [ $? -eq 0 ]; then
        echo "   ✓ black check passed"
    else
        echo "   ✗ black check failed (run 'black pure/' to fix)"
    fi
else
    echo "   ! black not installed. Run: pip install black"
fi

echo ""
echo "5. Running pytest..."
if command -v pytest &> /dev/null; then
    # Ensure package is installed
    pip install -e . --quiet 2>/dev/null
    pytest tests/ -v
    if [ $? -eq 0 ]; then
        echo "   ✓ Tests passed"
    else
        echo "   ✗ Tests failed"
        exit 1
    fi
else
    echo "   ! pytest not installed. Run: pip install pytest pytest-cov"
fi

echo ""
echo "========================================"
echo "All checks completed!"
echo "========================================"