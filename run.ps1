if (Test-Path ".\requirements.txt") {
    py -m pip install -r requirements.txt
}

Start-Process py app.py
Start-Sleep 1

Start-Process "http://127.0.0.1:5500/index.html"

Read-Host "Server running. Press Enter to exit."