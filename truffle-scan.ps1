# ===============================
# TruffleHog GitHub Scan (per-repo)
# ===============================

# Ask for username and token
$username = Read-Host "Enter your GitHub username"
$token = Read-Host "Enter your GitHub Personal Access Token (input hidden)" -AsSecureString
$tokenPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($token))

# Set environment variable for Docker
$env:GITHUB_TOKEN = $tokenPlain

# Output folder
$outputFolder = "TruffleHogResults"
if (-not (Test-Path $outputFolder)) { New-Item -ItemType Directory -Path $outputFolder }

# Test token by listing repos
try {
    $repos = gh repo list $username --limit 100 --json nameWithOwner | ConvertFrom-Json
    if (-not $repos) { throw "No repos found or token invalid." }
} catch {
    Write-Error "Failed to list repos: $_"
    exit 1
}

# Loop through each repo
foreach ($repo in $repos) {
    $repoName = $repo.nameWithOwner
    $outputFile = Join-Path $outputFolder (($repoName -replace '/','_') + ".json")

    Write-Host "Scanning repo: $repoName"
    docker run --rm -it -e GITHUB_TOKEN=$env:GITHUB_TOKEN trufflesecurity/trufflehog github --repo "https://github.com/$repoName" --json > $outputFile

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Done: $repoName -> $outputFile"
    } else {
        Write-Warning "Failed: $repoName"
    }
}

Write-Host "`nAll done. Results are in $outputFolder"
