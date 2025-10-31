// =============================
// CONFIGURAÇÕES GERAIS
// =============================
const M3U_URL = "http://americakg.xyz/get.php?username=djy7adcm&password=dbkauapt&type=m3u_plus&output=ts";

// =============================
// SPLASH SCREEN
// =============================
window.onload = () => {
    const splash = document.getElementById("splash");
    const loginSection = document.getElementById("login-section");

    if (splash && loginSection) {
        setTimeout(() => {
            splash.classList.add("hidden");
            loginSection.classList.remove("hidden");
        }, 2000);
    }
};

// =============================
// LOGIN
// =============================
function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const msg = document.getElementById("login-msg");

    if (!username || !password) {
        msg.innerText = "Preencha usuário e senha";
        return;
    }

    if (username === "Legacy.tv" && password === "Jtlm@043007") {
        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("content").classList.remove("hidden");
        msg.innerText = "";
        showSection('filmes');
    } else {
        msg.innerText = "Usuário ou senha inválidos";
    }
}

// =============================
// LISTAR ITENS DA PLAYLIST
// =============================
async function showSection(section) {
    const res = await fetch(M3U_URL);
    const text = await res.text();
    const lines = text.split("\n").filter(l => l.trim() !== "");
    const items = [];

    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith("#EXTINF:")) {
            const title = lines[i].split(",")[1] || "Sem título";
            const url = lines[i + 1] || "";

            if (section === 'filmes' && /movie|filme/i.test(title)) items.push({ title, url });
            else if (section === 'series' && /series|série/i.test(title)) items.push({ title, url });
            else if (section === 'canais' && !/movie|filme|series|série/i.test(title)) items.push({ title, url });
            else if (section === 'favoritos') items.push({ title, url });
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

// =============================
// PLAYER
// =============================
function play(url) {
    const player = document.getElementById("player");
    const playerSection = document.getElementById("player-section");

    if (player && playerSection) {
        player.src = url;
        player.play();
        playerSection.scrollIntoView({ behavior: "smooth" });
    }
}

// =============================
// PLANOS & CUPONS
// =============================
function goToPlanos() {
    window.location.href = "planos.html";
}

function comprar(plano) {
    alert(`Plano ${plano} selecionado!`);
}

function aplicarCupom() {
    const cupom = document.getElementById("cupom").value.trim();
    const msg = document.getElementById("msg-cupom");
    if (cupom.toLowerCase() === "gratis") msg.innerText = "+3 dias grátis aplicados!";
    else msg.innerText = "Cupom inválido";
}
