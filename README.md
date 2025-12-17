# Trufflehog Powershell Scanner + Python dashboard
A powershell script to scan **a users entire github repos** with trufflehog for Windows 11+, with a Python server to display results. If secrets are found, they are labeled with a red color.

## Uses
This is mainly useful to scan **your own github repos**, in case you left any secret on there by accident. Better to find them yourself, then wait for the bad guys to find them instead.

# Requirements

- Docker on Windows.
- Python on Windows.
- Python Flask
- Github CLI for Windows

```
pip install flask
```
Or, if your Python installation uses python3:
```
python -m pip install flask
```

Move this repo to your desktop and extract it, then:

# API
Get API token in Github, or in powershell:
```
gh auth token
```

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
```
python app.py
```

Then open up the given URI, i.e. http://127.0.0.1:5000/
