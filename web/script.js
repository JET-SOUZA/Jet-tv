const M3U_URL = "http://americakg.xyz/get.php?username=djy7adcm&password=dbkauapt&type=m3u_plus&output=ts";

window.onload = () => {
    // Após 2s, esconder splash e mostrar login
    setTimeout(() => {
        document.getElementById("splash").classList.add("hidden");
        document.getElementById("login-section").classList.remove("hidden");
    }, 2000);
};

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Login fake apenas para protótipo
    if(username && password) {
        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("content").classList.remove("hidden");
        showSection('filmes');
    } else {
        document.getElementById("login-msg").innerText = "Preencha usuário e senha";
    }
}

// Carregar M3U e mostrar cards
async function showSection(section) {
    const res = await fetch(M3U_URL);
    const text = await res.text();
    const lines = text.split("\n").filter(l => l.trim() !== "");

    const items = [];
    let currentCategory = '';
    for(let i=0;i<lines.length;i++){
        if(lines[i].startsWith("#EXTINF:")) {
            const title = lines[i].split(",")[1] || "Sem título";
            const url = lines[i+1] || "";
            // Categoria simples pelo tipo de seção
            if(section === 'filmes' && title.toLowerCase().includes("movie")) currentCategory = 'Filmes';
            else if(section === 'series' && title.toLowerCase().includes("series")) currentCategory = 'Séries';
            else if(section === 'canais' && !title.toLowerCase().includes("movie") && !title.toLowerCase().includes("series")) currentCategory = 'Ao Vivo';
            else continue;
            items.push({title, url});
        }
    }

    const container = document.getElementById("items");
    container.innerHTML = "";
    items.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerText = item.title;
        card.onclick = () => play(item.url);
        container.appendChild(card);
    });
}

function play(url) {
    const player = document.getElementById("player");
    player.src = url;
    player.play();
}
