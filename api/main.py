from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
import logging
import requests

app = FastAPI()

# ===========================
# CONFIGURAÇÕES
# ===========================
M3U_FILE = os.getenv("M3U_FILE", "playlist_djy7adcm_ts.m3u")

# Logger do servidor
logger = logging.getLogger("uvicorn.error")

# Permitir acesso ao frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Função para carregar playlist
# ===========================
def carregar_playlist(caminho: str):
    canais = []

    # 1️⃣ Caso seja URL (http ou https)
    if caminho.startswith(("http://", "https://")):
        try:
            logger.info(f"Baixando playlist de {caminho} ...")
            response = requests.get(caminho, timeout=15)
            response.raise_for_status()
            lines = response.text.splitlines()
        except Exception as e:
            logger.warning(f"❌ Falha ao baixar playlist: {e}")
            return canais

    # 2️⃣ Caso seja arquivo local
    else:
        p = Path(caminho)
        if not p.exists():
            logger.warning(f"⚠️ Arquivo de playlist não encontrado: {p}")
            return canais
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception as e:
            logger.warning(f"❌ Erro ao ler playlist: {e}")
            return canais

    # 3️⃣ Processar linhas da M3U
    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            try:
                title = lines[i].split(",")[1].strip()
                url = lines[i + 1].strip()

                if "movie" in title.lower() or "filme" in title.lower():
                    categoria = "filmes"
                elif "series" in title.lower() or "série" in title.lower():
                    categoria = "series"
                else:
                    categoria = "canais"

                canais.append({
                    "id": len(canais) + 1,
                    "title": title,
                    "url": url,
                    "categoria": categoria
                })
            except IndexError:
                continue  # Linha incompleta, ignora

    logger.info(f"✅ {len(canais)} canais carregados com sucesso!")
    return canais


# ===========================
# Carregar Playlist
# ===========================
CANAIS = carregar_playlist(M3U_FILE)

# ===========================
# Página Web IPTV
# ===========================
@app.get("/", response_class=HTMLResponse)
async def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Legacy IPTV</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Roboto', sans-serif; background: #f0f2f5; margin:0; padding:0; }}
            header {{ background:#007bff; color:#fff; padding:20px; text-align:center; }}
            .menu {{ display:flex; justify-content:center; gap:10px; margin:10px; flex-wrap:wrap; }}
            .menu button {{ padding:10px 20px; border:none; border-radius:5px; background:#0056b3; color:#fff; cursor:pointer; transition:0.3s; }}
            .menu button.active {{ background:#ff5722; }}
            .menu button:hover {{ opacity:0.9; }}
            .cards-container {{ display:flex; flex-wrap:wrap; justify-content:center; gap:15px; padding:10px; }}
            .card {{ background:#fff; padding:10px; border-radius:10px; width:180px; text-align:center; cursor:pointer; box-shadow:0 2px 6px rgba(0,0,0,0.2); transition:transform 0.2s; }}
            .card:hover {{ transform:scale(1.05); }}
            .card img {{ width:100%; border-radius:10px; }}
            #player-container {{ text-align:center; margin:20px; }}
            video {{ width:90%; max-width:800px; border-radius:10px; background:#000; }}
        </style>
    </head>
    <body>
        <header>
            <h1>Legacy IPTV</h1>
        </header>

        <div class="menu">
            <button onclick="showSection('canais')" id="btn-canais" class="active">Ao Vivo</button>
            <button onclick="showSection('filmes')" id="btn-filmes">Filmes</button>
            <button onclick="showSection('series')" id="btn-series">Séries</button>
        </div>

        <div id="player-container">
            <video id="player" controls></video>
        </div>

        <div class="cards-container" id="cards"></div>

        <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        <script>
            const canais = {CANAIS};

            function play(url) {{
                const video = document.getElementById('player');
                if (Hls.isSupported()) {{
                    const hls = new Hls();
                    hls.loadSource(url);
                    hls.attachMedia(video);
                    hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
                }} else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
                    video.src = url;
                    video.play();
                }}
            }}

            function showSection(section) {{
                document.querySelectorAll('.menu button').forEach(btn => btn.classList.remove('active'));
                document.getElementById('btn-' + section).classList.add('active');

                const container = document.getElementById('cards');
                container.innerHTML = '';
                canais.filter(c => c.categoria === section).forEach(c => {{
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.onclick = () => play(c.url);

                    const img = document.createElement('img');
                    img.src = 'static/images/canais/' + c.title + '.png';
                    img.onerror = function(){{ this.src = 'static/images/canais/default.png'; }}
                    card.appendChild(img);

                    const h3 = document.createElement('h3');
                    h3.innerText = c.title;
                    card.appendChild(h3);

                    container.appendChild(card);
                }});
            }}

            showSection('canais');
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)
