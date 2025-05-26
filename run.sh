#!/bin/bash

read -p "Enter Profile Name : " profile

export AWS_PROFILE=$profile

echo "application starting with profile $AWS_PROFILE"

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
	source .venv/bin/activate
fi

# Ensure script runs from the project root
cd "$(dirname "$0")"

exec uvicorn aws.main:app --reload --host 0.0.0.0 --port 8000