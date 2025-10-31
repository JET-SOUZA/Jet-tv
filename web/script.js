const M3U_URL = "http://americakg.xyz/get.php?username=djy7adcm&password=dbkauapt&type=m3u_plus&output=ts";

// Splash screen
window.onload = () => {
    setTimeout(() => {
        document.getElementById("splash").classList.add("hidden");
        document.getElementById("login-section").classList.remove("hidden");
    }, 2000);
};

// Login
function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("login-msg");

    if (!username || !password) {
        msg.innerText = "Preencha usuário e senha";
        return;
    }

    if(username === "Legacy.tv" && password === "Jtlm@043007") {
        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("content").classList.remove("hidden");
        msg.innerText = "";
        showSection('filmes');
    } else {
        msg.innerText = "Usuário ou senha inválidos";
    }
}

// Mostrar seção e listar itens da playlist M3U
async function showSection(section) {
    const res = await fetch(M3U_URL);
    const text = await res.text();
    const lines = text.split("\n").filter(l => l.trim() !== "");
    const items = [];

    for(let i=0;i<lines.length;i++){
        if(lines[i].startsWith("#EXTINF:")) {
            const title = lines[i].split(",")[1] || "Sem título";
            const url = lines[i+1] || "";
            if(section==='filmes' && /movie|filme/i.test(title)) items.push({title,url});
            else if(section==='series' && /series|série/i.test(title)) items.push({title,url});
            else if(section==='canais' && !/movie|filme|series|série/i.test(title)) items.push({title,url});
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

// Player embutido
function play(url) {
    const player = document.getElementById("player");
    if(player){
        player.src = url;
        player.play();
        player.scrollIntoView({ behavior: "smooth" });
    }
}

// Redirecionar para tela de planos
function goToPlanos() { window.location.href = "planos.html"; }

// Comprar plano
function comprar(plano){ alert(`Plano ${plano} selecionado!`); }

// Aplicar cupom
function aplicarCupom(){
    const cupo
