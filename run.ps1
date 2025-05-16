# Cài dependencies nếu có requirements.txt
if (Test-Path ".\requirements.txt") {
    py -m pip install -r requirements.txt
}

Start-Process -NoNewWindow -FilePath py -ArgumentList "app.py"

Start-Sleep 0
function Test-LiveServer {
    try {
        $version = live-server --version
        return $true
    }
    catch {
        return $false
    }
}

if (Test-LiveServer) {
    Start-Process -NoNewWindow -FilePath live-server -ArgumentList "--port=5500 --open=./index.html"
}
else {
    Start-Process -NoNewWindow -FilePath py -ArgumentList "-m http.server 5500"
    Start-Sleep 1
    Start-Process "http://127.0.0.1:5500/index.html"
}

Read-Host "Servers are running. Press Enter to exit."
