from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permitir que o front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # você pode limitar ao domínio do front-end
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arquivo M3U (pode ser variável de ambiente)
M3U_FILE = os.getenv("M3U_FILE", "playlist_djy7adcm_ts (1) (1).m3u")

# Carregar canais
CANAIS = []
with open(M3U_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        title = lines[i].split(",")[1].strip()
        url = lines[i+1].strip()
        if "movie" in title.lower() or "filme" in title.lower():
            categoria = "filmes"
        elif "series" in title.lower() or "série" in title.lower():
            categoria = "series"
        else:
            categoria = "canais"
        CANAIS.append({"id": len(CANAIS)+1, "title": title, "url": url, "categoria": categoria})

print(f"{len(CANAIS)} canais carregados!")

# ===========================
# API JSON
# ===========================
@app.get("/playlist")
async def playlist(section: str = None):
    if section:
        filtered = [c for c in CANAIS if c["categoria"] == section]
        return {"items": filtered}
    return {"items": CANAIS}

# ===========================
# Rodar localmente
# ===========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
