# IPTV Starter
Plataforma IPTV web e mobile, com player embutido, login, planos e playlist M3U.

## Estrutura do projeto
Jet-tv/
├─ web/           # Frontend HTML, CSS, JS
├─ api/           # Backend FastAPI (playlist)
├─ mobile/        # Flutter app (em desenvolvimento)
├─ .gitignore
├─ LICENSE
└─ README.md

## Funcionalidades
- Tela de login com splash screen
- Menu: Filmes, Séries, Canais Ao Vivo, Favoritos, Cupons, Recarga
- Player embutido para streaming M3U
- Tela de planos com destaque “HOT”
- Sistema de cupons
- Tema moderno: cores predominantes preto e laranja

## Rodando localmente

### Web
```bash
cd Jet-tv/web
# Se tiver Node.js, instalar dependências
npm install
# Abrir index.html no navegador
