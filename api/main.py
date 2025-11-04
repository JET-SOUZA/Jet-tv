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
M3U_FILE = os.getenv("M3U_FILE", os.path.join(os.path.dirname(__file__), "playlist_djy7adcm_ts.m3u"))

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

    if caminho.startswith(("http://", "https://")):
        try:
            logger.info(f"Baixando playlist de {caminho} ...")
            response = requests.get(caminho, timeout=15)
            response.raise_for_status()
            lines = response.text.splitlines()
        except Exception as e:
            logger.warning(f"❌ Falha ao baixar playlist: {e}")
            return canais
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
                continue
    logger.info(f"✅ {len(canais)} canais carregados com sucesso!")
    return canais


# ===========================
# Carregar Playlist
# ===========================
CANAIS = carregar_playlist(M3U_FILE)

# ===========================
# Página Web estilo UniTVnet
# ===========================
@app.get("/", response_class=HTMLResponse)
async def home():
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Legacy IPTV</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                margin: 0;
                font-family: 'Roboto', sans-serif;
                background-color: #0b0c10;
                color: white;
                overflow-x: hidden;
            }}
            header {{
                background: linear-gradient(90deg, #007bff, #00b4d8);
                padding: 20px;
                text-align: center;
                font-size: 28px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            nav {{
                display: flex;
                justify-content: center;
                background-color: #1f2833;
                padding: 10px;
                flex-wrap: wrap;
            }}
            nav button {{
                margin: 5px;
                padding: 10px 20px;
                border: none;
                background-color: #0d6efd;
                color: white;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                transition: all 0.2s;
            }}
            nav button.active, nav button:hover {{
                background-color: #ff5722;
            }}
            .cards-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 15px;
                padding: 20px;
            }}
            .card {{
                background-color: #1f2833;
                border-radius: 12px;
                padding: 10px;
                cursor: pointer;
                text-align: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                transition: transform 0.2s;
            }}
            .card:hover {{
                transform: scale(1.05);
            }}
            .card img {{
                width: 100%;
                border-radius: 10px;
                height: 120px;
                object-fit: cover;
            }}
            .card h3 {{
                font-size: 15px;
                margin: 10px 0 0;
                color: #ddd;
            }}
            #player-container {{
                text-align: center;
                margin-top: 15px;
            }}
            video {{
                width: 90%;
                max-width: 1000px;
                border-radius: 10px;
                background: #000;
            }}
        </style>
    </head>
    <body>
        <header>📺 Legacy IPTV</header>
        <nav>
            <button onclick="showSection('canais')" id="btn-canais" class="active">Ao Vivo</button>
            <button onclick="showSection('filmes')" id="btn-filmes">Filmes</button>
            <button onclick="showSection('series')" id="btn-series">Séries</button>
        </nav>

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
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}

            function showSection(section) {{
                document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
                document.getElementById('btn-' + section).classList.add('active');

                const container = document.getElementById('cards');
                container.innerHTML = '';
                canais.filter(c => c.categoria === section).forEach(c => {{
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.onclick = () => play(c.url);

                    const img = document.createElement('img');
                    img.src = 'https://picsum.photos/200/120?random=' + c.id;
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
