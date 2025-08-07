#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "Please edit .env file and add your OpenAI API key"
    echo ""
    read -p "Press enter to continue..."
fi

echo ""
echo "Starting the server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
