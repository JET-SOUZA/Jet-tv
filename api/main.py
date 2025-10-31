from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# ===========================
# Função para ler a playlist
# ===========================
CANAIS = []

with open("playlist_djy7adcm_ts (1) (1).m3u", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i in range(len(lines)):
    if lines[i].startswith("#EXTINF"):
        title = lines[i].split(",")[1].strip()
        url = lines[i + 1].strip()
        CANAIS.append({"id": len(CANAIS)+1, "title": title, "url": url})

print(f"{len(CANAIS)} canais carregados!")

# ===========================
# Rota principal (interface)
# ===========================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    html = """
    <html>
        <head>
            <title>Legacy IPTV</title>
            <style>
                body { font-family: Arial, sans-serif; background: #f0f2f5; padding: 20px; text-align:center;}
                h1 { color: #333; }
                .cards-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 20px; }
                .card { background: #fff; padding: 15px; border-radius: 10px; width: 250px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);}
                button { margin-top: 10px; padding: 10px; border:none; background:#007bff; color:#fff; border-radius:5px; cursor:pointer;}
                video { width:100%; margin-top:10px; border-radius:10px; }
            </style>
        </head>
        <body>
            <h1>Legacy IPTV</h1>
            <div class="cards-container">
    """
    for canal in CANAIS:
        html += f"""
        <div class="card">
            <h3>{canal['title']}</h3>
            <video controls>
                <source src="{canal['url']}" type="application/x-mpegURL">
            </video>
        </div>
        """

    html += """
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

# ===========================
# Rodar localmente
# ===========================
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
