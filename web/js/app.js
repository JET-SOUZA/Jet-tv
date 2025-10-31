const M3U_URL = "http://americakg.xyz/get.php?username=djy7adcm&password=dbkauapt&type=m3u_plus&output=ts";

window.onload = () => {
    setTimeout(() => {
        document.getElementById("splash").classList.add("hidden");
        document.getElementById("login-section").classList.remove("hidden");
    }, 2000);
};

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    if(username && password){
        document.getElementById("login-section").classList.add("hidden");
        document.getElementById("content").classList.remove("hidden");
        showSection('filmes');
    } else {
        document.getElementById("login-msg").innerText = "Preencha usuário e senha";
    }
}

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
            else if(section==='favoritos') items.push({title,url}); // demo
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

// Redirecionar para tela de planos
function goToPlanos() {
    window.location.href = "planos.html";
}

// Planos
function comprar(plano){
    alert(`Plano ${plano} selecionado!`);
}

// Cupons
function aplicarCupom(){
    const cupom = document.getElementById("cupom").value;
    const msg = document.getElementById("msg-cupom");
    if(cupom.toLowerCase() === "gratis") msg.innerText = "+3 dias grátis aplicados!";
    else msg.innerText = "Cupom inválido";
}
