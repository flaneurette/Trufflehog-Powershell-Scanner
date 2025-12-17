# Trufflehog Powershell Scanner
A powershell script to scan all github repos with trufflehog for Windows 11+, with a Python server to display results. If secrets are found, they are labeled with a red color.

# Requirements

- Docker on Windows.
- Python on Windows.

# API
Get API token in Github, or in powershell:
```
gh auth token
```

Move this repo to your desktop and extract it, then:

# Powershell

```cd %USERPROFILE%\Desktop\Trufflehog-Powershell-Scanner\```

```Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass```

```./truffle-scan.ps1```

Then:

- Enter your username when asked
- Enter your github API key when asked

# Processing

When finished, process results:

```
cd TruffleHogResults
```
python app.py
```

Then open up the given URI, i.e. http://127.0.0.1:5000/
