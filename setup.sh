#!/bin/bash
set -e

echo "🚀 Setting up AI Knowledge Assistant..."

# Activate venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -q --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "✓ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Configure .env: cp .env.example .env"
echo "3. Add your OPENAI_API_KEY to .env"
echo ""
echo "Try it out:"
echo "  python -m uvicorn src.api.main:app --reload"
echo "  # or"
echo "  python -m src.api.cli query --query 'Your question?'"
