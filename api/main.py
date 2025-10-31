from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Permitir que o front-end acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Usuário de login
USERNAME = "Legacy.tv"
PASSWORD = "Jtlm@043007"

# Modelos
class LoginRequest(BaseModel):
    username: str
    password: str

# Dados de exemplo (você pode substituir por DB real)
FILMES = [
    {"id": 1, "title": "Filme 1", "url": "https://path-to-video1.m3u8"},
    {"id": 2, "title": "Filme 2", "url": "https://path-to-video2.m3u8"}
]

SERIES = [
    {"id": 1, "title": "Série 1", "url": "https://path-to-serie1.m3u8"},
    {"id": 2, "title": "Série 2", "url": "https://path-to-serie2.m3u8"}
]

CANAIS = [
    {"id": 1, "title": "Canal 1", "url": "https://path-to-live1.m3u8"},
    {"id": 2, "title": "Canal 2", "url": "https://path-to-live2.m3u8"}
]

# Rotas
@app.get("/")
def root():
    return {"ok": True}

@app.post("/login")
def login(data: LoginRequest):
    if data.username == USERNAME and data.password == PASSWORD:
        return {"success": True, "message": "Login realizado com sucesso"}
    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

@app.get("/filmes")
def get_filmes():
    return FILMES

@app.get("/series")
def get_series():
    return SERIES

@app.get("/canais")
def get_canais():
    return CANAIS
