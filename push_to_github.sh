#!/bin/bash
set -e

echo "================================================================="
echo "         AI TECH CONSULTANT — GITHUB PUSH AUTOMATOR              "
echo "================================================================="

# Ensure on main branch
git branch -M main

REPO_URL="$1"
if [ -z "$REPO_URL" ]; then
    echo ""
    echo "Please enter your GitHub Repository Remote URL"
    echo "Example: https://github.com/YOUR_USERNAME/ai-tech-consultant.git"
    read -p "GitHub Remote URL: " REPO_URL
fi

if [ -z "$REPO_URL" ]; then
    echo "[ERROR] No GitHub URL provided. Aborting push."
    exit 1
fi

echo ""
echo "[1/3] Configuring Git remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
echo "Remote set to: $REPO_URL"

echo ""
echo "[2/3] Staging and committing files..."
git add .
if ! git diff-index --quiet HEAD --; then
    git commit -m "feat(github): Prepare enterprise repository with CI workflows, LICENSE, and documentation"
fi

echo ""
echo "[3/3] Pushing to GitHub (main branch)..."
git push -u origin main

echo ""
echo "================================================================="
echo "   SUCCESSFULLY PUSHED AI TECH CONSULTANT TO GITHUB!            "
echo "================================================================="
