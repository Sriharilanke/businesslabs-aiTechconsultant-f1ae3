param (
    [string]$RepoUrl = ""
)

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "         AI TECH CONSULTANT — GITHUB PUSH AUTOMATOR              " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Cyan

# Ensure on main branch
git branch -M main

# Check if URL provided or prompt
if (-not $RepoUrl) {
    Write-Host "`nPlease enter your GitHub Repository Remote URL" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/YOUR_USERNAME/ai-tech-consultant.git" -ForegroundColor DarkGray
    $RepoUrl = Read-Host "GitHub Remote URL"
}

if (-not $RepoUrl) {
    Write-Host "`n[ERROR] No GitHub URL provided. Aborting push." -ForegroundColor Red
    exit 1
}

# Set remote origin
Write-Host "`n[1/3] Configuring Git remote origin..." -ForegroundColor Cyan
git remote remove origin 2>$null
git remote add origin $RepoUrl
Write-Host "Remote set to: $RepoUrl" -ForegroundColor Green

# Stage all files
Write-Host "`n[2/3] Staging all files..." -ForegroundColor Cyan
git add .
git status -s

# Commit any remaining changes
$status = git status --porcelain
if ($status) {
    git commit -m "feat(github): Prepare enterprise repository with CI workflows, LICENSE, and documentation"
}

# Push to GitHub
Write-Host "`n[3/3] Pushing to GitHub (main branch)..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=================================================================" -ForegroundColor Green
    Write-Host "   SUCCESSFULLY PUSHED AI TECH CONSULTANT TO GITHUB!            " -ForegroundColor Green
    Write-Host "=================================================================" -ForegroundColor Green
} else {
    Write-Host "`n[NOTICE] If push failed due to authentication, run:" -ForegroundColor Yellow
    Write-Host "  gh auth login" -ForegroundColor Cyan
    Write-Host "  or verify your GitHub Personal Access Token." -ForegroundColor Cyan
}
