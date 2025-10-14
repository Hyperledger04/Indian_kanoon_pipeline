#!/bin/bash

# Indian Kanoon Pipeline - Quick Start Script
# This script helps you set up and deploy the entire pipeline

set -e

echo "=========================================="
echo "  Indian Kanoon Pipeline - Quick Start"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Step 1: GitHub Repository Setup
echo -e "${BLUE}Step 1: GitHub Repository Setup${NC}"
echo "--------------------------------"
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: indian-kanoon-pipeline): " REPO_NAME
REPO_NAME=${REPO_NAME:-indian-kanoon-pipeline}

echo ""
echo -e "${YELLOW}Creating repository structure...${NC}"

# Initialize git if not already
if [ ! -d .git ]; then
    git init
    echo -e "${GREEN}✓ Git initialized${NC}"
else
    echo -e "${GREEN}✓ Git already initialized${NC}"
fi

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
venv/
.env
chromedriver
*.log
.DS_Store
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
fi

# Step 2: Railway Backend Setup
echo ""
echo -e "${BLUE}Step 2: Railway Backend Deployment${NC}"
echo "-----------------------------------"
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Go to https://railway.app and sign up/login"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Connect this repository: $GITHUB_USERNAME/$REPO_NAME"
echo "4. Railway will automatically deploy!"
echo ""
read -p "Press Enter when you've deployed to Railway..."

read -p "Enter your Railway app URL (e.g., https://your-app.up.railway.app): " RAILWAY_URL

# Update index.html with Railway URL
if [ -f index.html ]; then
    sed -i.bak "s|const API_URL = 'https://your-app-name.up.railway.app/scrape';|const API_URL = '$RAILWAY_URL/scrape';|g" index.html
    rm index.html.bak 2>/dev/null || true
    echo -e "${GREEN}✓ Updated index.html with your Railway URL${NC}"
fi

# Step 3: GitHub Pages Setup
echo ""
echo -e "${BLUE}Step 3: GitHub Pages Deployment${NC}"
echo "--------------------------------"
echo "Committing and pushing to GitHub..."

git add .
git commit -m "Initial deployment setup" 2>/dev/null || echo "No changes to commit"

if git remote | grep -q origin; then
    echo -e "${YELLOW}Remote 'origin' already exists${NC}"
else
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo -e "${GREEN}✓ Added remote origin${NC}"
fi

git branch -M main
echo ""
echo -e "${YELLOW}Pushing to GitHub...${NC}"
echo "You may need to authenticate with GitHub"
git push -u origin main

echo ""
echo -e "${GREEN}✓ Code pushed to GitHub!${NC}"
echo ""
echo -e "${YELLOW}Now enable GitHub Pages:${NC}"
echo "1. Go to https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
echo "2. Source: Deploy from branch 'main', folder '/ (root)'"
echo "3. Click 'Save'"
echo ""
read -p "Press Enter when GitHub Pages is enabled..."

# Step 4: n8n Setup
echo ""
echo -e "${BLUE}Step 4: n8n Workflow Setup${NC}"
echo "---------------------------"
read -p "Enter your n8n webhook URL (default: https://n8n.n8nit.xyz/webhook/indian-kanoon): " N8N_URL
N8N_URL=${N8N_URL:-https://n8n.n8nit.xyz/webhook/indian-kanoon}

echo ""
echo -e "${YELLOW}Make sure your n8n workflow:${NC}"
echo "✓ Is ACTIVE (not just saved)"
echo "✓ Has OpenAI API credentials configured"
echo "✓ Has Google Sheets OAuth connected"
echo "✓ Webhook URL is set to Production mode"
echo ""
read -p "Press Enter when n8n is configured..."

# Final Summary
echo ""
echo "=========================================="
echo -e "${GREEN}  🎉 Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Your Application URLs:${NC}"
echo "• Frontend: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo "• Backend:  $RAILWAY_URL"
echo "• n8n:      $N8N_URL"
echo ""
echo -e "${YELLOW}Testing Your Deployment:${NC}"
echo "1. Visit: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo "2. Test backend health: $RAILWAY_URL/health"
echo "3. Enter a test Indian Kanoon URL"
echo "4. Set max documents to 2-3 for testing"
echo "5. Check results in your Google Sheet"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo "• Monitor Railway logs for backend issues"
echo "• Check n8n execution history"
echo "• Review README.md for advanced configuration"
echo ""
echo "Happy scraping! 🚀"