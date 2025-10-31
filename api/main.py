from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

# Permitir que o frontend acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# Carregar M3U via variável de ambiente ou arquivo local
# ===========================
M3U_FILE = os.getenv("M3U_FILE", "playlist_djy7adcm_ts (1) (1).m3u")
CANAIS = []

with open(M3U_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        title = lines[i].split(",")[1].strip()
        url = lines[i + 1].strip()
        # Categorizar
        if "movie" in title.lower() or "filme" in title.lower():
            categoria = "filmes"
        elif "series" in title.lower() or "série" in title.lower():
            categoria = "series"
        else:
            categoria = "canais"
        CANAIS.append({"id": len(CANAIS)+1, "title": title, "url": url, "categoria": categoria})

print(f"{len(CANAIS)} canais carregados!")

# ===========================
# API para playlist filtrável
# ===========================
@app.get("/playlist")
async def playlist(section: str = None):
    if section:
        filtered = [c for c in CANAIS if c["categoria"] == section]
        return {"items": filtered}
    return {"items": CANAIS}

# ===========================
# Interface web
# ===========================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = """
    <html>
    <head>
        <title>Legacy IPTV</title>
        <style>
            body { font-family: Arial, sans-serif; background:#f0f2f5; margin:0; padding:0; }
            header { background:#007bff; color:#fff; padding:15px; text-align:center; font-size:24px; }
            nav { display:flex; justify-content:center; gap:10px; margin:15px 0; }
            nav button { padding:10px 20px; border:none; border-radius:5px; cursor:pointer; background:#007bff; color:#fff; }
            nav button.active { background:#0056b3; }
            .cards-container { display:flex; flex-wrap:wrap; justify-content:center; gap:15px; padding:0 15px; }
            .card { background:#fff; padding:15px; border-radius:10px; width:250px; box-shadow:0 2px 6px rgba(0,0,0,0.2); cursor:pointer; text-align:center; }
            #player-container { margin:20px auto; width:80%; max-width:800px; }
            video { width:100%; border-radius:10px; }
        </style>
    </head>
    <body>
        <header>Legacy IPTV</header>
        <nav>
            <button onclick="showSection('canais')" id="btn-canais" class="active">Ao Vivo</button>
            <button onclick="showSection('filmes')" id="btn-filmes">Filmes</button>
            <button onclick="showSection('series')" id="btn-series">Séries</button>
        </nav>
        <div id="player-container">
            <video id="player" controls></video>
        </div>
        <div class="cards-container" id="items"></div>

        <script>
            let currentSection = 'canais';

            async function showSection(section) {
                currentSection = section;
                document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));
                document.getElementById('btn-' + section).classList.add('active');

                const res = await fetch(`/playlist?section=${section}`);
                const data = await res.json();
                const container = document.getElementById('items');
                container.innerHTML = '';
                data.items.forEach(item => {
                    const card = document.createElement('div');
                    card.className = 'card';
                    card.innerText = item.title;
                    card.onclick = () => play(item.url);
                    container.appendChild(card);
                });
            }

            function play(url) {
                const player = document.getElementById('player');
                player.src = url;
                player.play();
                window.scrollTo({ top:0, behavior:'smooth' });
            }

            // Carregar seção inicial
            showSection(currentSection);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ===========================
# Rodar localmente
# ===========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
