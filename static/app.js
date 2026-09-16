let socket;

let timeSelecionado = null;

let oddSelecionada = null;

let saldo = 1000;


function conectar() {

    socket = new WebSocket(
        "ws://" + window.location.host + "/websocket"
    );


    socket.onopen = function() {

        console.log("Conectado ao servidor WebSocket");

    };


    socket.onmessage = function(event) {

        const mensagem = JSON.parse(event.data);

        if (mensagem.tipo === "nova_aposta") {

            mostrarAposta(mensagem.dados);

        }

    };


    socket.onclose = function() {

        console.log("Conexão encerrada");

    };

}


function selecionarTime(time, odd) {

    timeSelecionado = time;

    oddSelecionada = odd;

    document.getElementById(
        "timeSelecionado"
    ).textContent = time + " - odd " + odd;

}


function apostar() {

    const usuario =
        document.getElementById("usuario").value.trim();

    const valor =
        Number(document.getElementById("valor").value);


    if (!usuario) {

        alert("Digite seu nome.");

        return;

    }


    if (!timeSelecionado) {

        alert("Escolha um time.");

        return;

    }


    if (!valor || valor <= 0) {

        alert("Digite um valor válido.");

        return;

    }


    if (valor > saldo) {

        alert("Saldo insuficiente.");

        return;

    }


    saldo = saldo - valor;

    document.getElementById(
        "saldo"
    ).textContent = saldo.toFixed(2);


    const aposta = {

        tipo: "aposta",

        dados: {

            usuario: usuario,

            time: timeSelecionado,

            valor: valor,

            odd: oddSelecionada

        }

    };


    socket.send(
        JSON.stringify(aposta)
    );


    document.getElementById("valor").value = "";

}


function mostrarAposta(aposta) {

    const mensagens =
        document.getElementById("mensagens");


    const elemento =
        document.createElement("div");


    elemento.className = "mensagem";


    elemento.innerHTML = `
        <strong>${aposta.usuario}</strong>
        apostou
        <strong>R$ ${Number(aposta.valor).toFixed(2)}</strong>
        em
        <strong>${aposta.time}</strong>
        (odd ${aposta.odd})
    `;


    mensagens.prepend(elemento);

}


conectar();