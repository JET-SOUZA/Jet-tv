const API_URL = "https://jet-tv.onrender.com";

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            document.getElementById("login-section").style.display = "none";
            document.getElementById("content").style.display = "block";
            showSection("filmes");
        } else {
            document.getElementById("login-msg").innerText = "Usuário ou senha inválidos";
        }
    })
    .catch(err => console.error(err));
}

function showSection(section) {
    fetch(`${API_URL}/${section}`)
        .then(res => res.json())
        .then(items => {
            const container = document.getElementById("items");
            container.innerHTML = "";
            items.forEach(item => {
                const card = document.createElement("div");
                card.className = "card";
                card.innerText = item.title;
                card.onclick = () => play(item.url);
                container.appendChild(card);
            });
        });
}

function play(url) {
    const player = document.getElementById("player");
    player.src = url;
    player.play();
}
