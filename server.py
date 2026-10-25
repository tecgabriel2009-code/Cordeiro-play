import http.server
import socketserver
import os
import urllib.parse

PORT = 3000
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_CONTENT = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cordeiro Play - Download APK</title>
    <style>
        :root {
            --bg: #0D0A1A;
            --surface: #18122B;
            --primary: #FF007F;
            --secondary: #00E5FF;
            --text: #FFFFFF;
            --text-muted: #A09DB5;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            background-color: var(--bg);
            color: var(--text);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 24px;
            text-align: center;
        }
        .card {
            background: var(--surface);
            border-radius: 24px;
            padding: 32px 24px;
            max-width: 440px;
            width: 100%;
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6), 0 0 24px rgba(255, 0, 127, 0.15);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .logo {
            width: 130px;
            height: 130px;
            border-radius: 50%;
            margin-bottom: 20px;
            box-shadow: 0 0 25px rgba(255, 0, 127, 0.4);
            animation: pulse 3s infinite ease-in-out;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 25px rgba(255, 0, 127, 0.4); }
            50% { transform: scale(1.03); box-shadow: 0 0 35px rgba(0, 229, 255, 0.5); }
        }
        h1 {
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #FFF, var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .badge {
            display: inline-block;
            background: rgba(0, 229, 255, 0.15);
            color: var(--secondary);
            font-size: 12px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 229, 255, 0.3);
        }
        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 14px;
            margin: 24px 0;
        }
        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 16px 20px;
            border-radius: 16px;
            text-decoration: none;
            font-weight: 700;
            font-size: 16px;
            transition: all 0.2s ease;
        }
        .btn-primary {
            background: linear-gradient(135deg, var(--primary), #D6006B);
            color: white;
            box-shadow: 0 8px 24px rgba(255, 0, 127, 0.4);
        }
        .btn-primary:active {
            transform: scale(0.98);
        }
        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: var(--secondary);
            border: 1px solid rgba(0, 229, 255, 0.3);
        }
        .btn-secondary:active {
            transform: scale(0.98);
        }
        .features {
            text-align: left;
            background: rgba(0, 0, 0, 0.25);
            padding: 16px;
            border-radius: 14px;
            font-size: 13px;
            color: var(--text-muted);
            margin-top: 10px;
        }
        .features li {
            margin-bottom: 8px;
            list-style: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .features li:last-child {
            margin-bottom: 0;
        }
        .check {
            color: #00E676;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="card">
        <img src="/logo_cordeiro_play.png" alt="Cordeiro Play Logo" class="logo">
        <h1>Cordeiro Play</h1>
        <div class="badge">APK ATUALIZADO & COMPILADO</div>
        
        <div class="btn-group">
            <a href="/app-debug.apk" download="app-debug.apk" class="btn btn-primary">
                ⬇️ Baixar APK Direto (app-debug.apk)
            </a>
            <a href="/cordeiro-play-export.zip" download="cordeiro-play-export.zip" class="btn btn-secondary">
                📦 Baixar Pacote ZIP de Exportação
            </a>
        </div>

        <div class="features">
            <ul>
                <li><span class="check">✓</span> Botão "EXTRAIR ÁUDIO": <strong> MP3 128/320 Kbps</strong></li>
                <li><span class="check">✓</span> Novo Logo Oficial Cordeiro Play aplicado</li>
                <li><span class="check">✓</span> APK assinado e certificado para instalação</li>
                <li><span class="check">✓</span> Motor yt-dlp nativo integrado</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

class DownloadHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            content = HTML_CONTENT.encode("utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/app-debug.apk":
            filepath = os.path.join(WORKSPACE_DIR, "app-debug.apk")
            if not os.path.exists(filepath):
                filepath = os.path.join(WORKSPACE_DIR, ".build-outputs", "app-debug.apk")
            self.serve_file(filepath, "application/vnd.android.package-archive", "app-debug.apk")
            return

        if path == "/cordeiro-play-export.zip":
            filepath = os.path.join(WORKSPACE_DIR, "cordeiro-play-export.zip")
            self.serve_file(filepath, "application/zip", "cordeiro-play-export.zip")
            return

        if path == "/logo_cordeiro_play.png":
            filepath = os.path.join(WORKSPACE_DIR, "logo_cordeiro_play.png")
            self.serve_file(filepath, "image/png", None)
            return

        self.send_error(404, "Arquivo nao encontrado")

    def serve_file(self, filepath, content_type, download_filename):
        if not os.path.exists(filepath):
            self.send_error(404, "Arquivo nao encontrado")
            return

        file_size = os.path.getsize(filepath)
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(file_size))
        if download_filename:
            self.send_header("Content-Disposition", f'attachment; filename="{download_filename}"')
        self.end_headers()

        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1024 * 512)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    break

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def run():
    with ReusableTCPServer(("0.0.0.0", PORT), DownloadHandler) as httpd:
        print(f"Servidor de download rodando na porta {PORT}...")
        httpd.serve_forever()

if __name__ == "__main__":
    run()
