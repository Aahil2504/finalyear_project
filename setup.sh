#!/bin/bash

# Setup script for Face Recognition Attendance System

echo "🚀 Setting up Face Recognition Attendance System..."

# Create directories
mkdir -p dataset
mkdir -p attendance

# Create .gitkeep files to preserve directories
touch dataset/.gitkeep
touch attendance/.gitkeep

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd api
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Backend: cd api && python app.py"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker:"
echo "docker-compose up --build"
