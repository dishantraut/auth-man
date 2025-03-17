#!/bin/bash
# filepath: start.sh

# * Author          :- Dishant
# * Created Date    :- 17/Mar/2025
# * Updated Date    :- 17/Mar/2025
# * Description     :- run IAM service
# * Usage           :- bash scripts/start.sh

set -euo pipefail

# * Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# * Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    # Install dependencies if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    fi
fi

# * Check if app.py exists
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found"
    exit 1
fi

clear && python3 app.py
