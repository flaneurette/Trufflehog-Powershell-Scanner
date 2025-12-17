# Trufflehog Powershell Scanner
A powershell script to scan all github repos with trufflehog for Windows 11+

# Requirements
Docker on Windows.

# API
Get API token in Github, or in powershell:
```
gh auth token
```

# Powershell

```cd C:\your\path\to\truffle-scan.ps1```

```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

```./truffle-scan.ps1```

Then:

- Enter your username when asked
- Enter your github API key when asked
