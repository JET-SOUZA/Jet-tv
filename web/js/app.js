const API_URL = "https://legacy-iptv-api.onrender.com/playlist";

// Splash
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

    if(!username || !password){
        msg.innerText = "Preencha usuário e senha";
        return;
    }

    if(username === "Legacy.tv" && password === "Jtlm@043007") {
        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("content").classList.remove("hidden");
        msg.innerText = "";
        showSection("filmes");
    } else {
        msg.innerText = "Usuário ou senha inválidos";
    }
}

// Mostrar seção
async function showSection(section) {
    const res = await fetch(`${API_URL}?section=${section}`);
    const data = await res.json();

    const container = document.getElementById("items");
    container.innerHTML = "";

    data.items.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<img src="assets/images/background.jpg" alt=""><h3>${item.title}</h3>`;
        card.onclick = () => play(item.url);
        container.appendChild(card);
    });
}

// Player único
function play(url) {
    const player = document.getElementById("player");
    player.src = url;
    player.play();
    document.getElementById("player-section").scrollIntoView({behavior:"smooth"});
}

// Planos
function goToPlanos() { window.location.href = "planos.html"; }
function comprar(plano){ alert(`Plano ${plano} selecionado!`); }
function aplicarCupom(){
    const cupom = document.getElementById("cupom").value.trim();
    const msg = document.getElementById("msg-cupom");
    if(cupom.toLowerCase() === "gratis") msg.innerText = "+3 dias grátis aplicados!";
    else msg.innerText = "Cupom inválido";
}
