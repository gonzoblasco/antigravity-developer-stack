#!/bin/bash

# Scaffold a new MCP Server
# Usage: ./scaffold.sh [project_name]

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
  echo "Usage: ./scaffold.sh [project_name]"
  exit 1
fi

echo "🚀 Scaffolding MCP Server: $PROJECT_NAME"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi

# Use the official creator
# We use -y to accept defaults, but we can customize if needed
npx @modelcontextprotocol/create-server "$PROJECT_NAME"

echo ""
echo "✅ Project created in $PROJECT_NAME"
echo "👉 Next steps:"
echo "   cd $PROJECT_NAME"
echo "   npm install"
echo "   npm run build"
