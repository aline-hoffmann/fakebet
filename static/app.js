let socket;

let jogoSelecionado = null;

let timeSelecionado = null;

let oddSelecionada = null;

let usuarioRegistrado = false;


function conectar() {

    socket = new WebSocket(
        "ws://" +
        window.location.host +
        "/websocket"
    );


    socket.onopen = function() {

        console.log(
            "Conectado ao servidor WebSocket"
        );

    };


    socket.onmessage = function(event) {

        const mensagem =
            JSON.parse(event.data);


        if (
            mensagem.tipo ===
            "usuario_registrado"
        ) {

            usuarioRegistrado = true;


            atualizarSaldo(
                mensagem.dados.saldo
            );


            document.getElementById(
                "usuario"
            ).disabled = true;


            document.getElementById(
                "botaoEntrar"
            ).disabled = true;


            adicionarMensagem(
                "Você entrou como " +
                mensagem.dados.usuario
            );

        }


        else if (
            mensagem.tipo ===
            "saldo_atualizado"
        ) {

            atualizarSaldo(
                mensagem.dados.saldo
            );

        }


        else if (
            mensagem.tipo ===
            "nova_aposta"
        ) {

            mostrarAposta(
                mensagem.dados
            );

        }


        else if (
            mensagem.tipo ===
            "resultado_jogo"
        ) {

            mostrarResultado(
                mensagem.dados
            );

        }


        else if (
            mensagem.tipo ===
            "erro"
        ) {

            alert(
                mensagem.dados.mensagem
            );

        }

    };


    socket.onclose = function() {

        console.log(
            "Conexão WebSocket encerrada"
        );


        adicionarMensagem(
            "Conexão com o servidor encerrada."
        );

    };


    socket.onerror = function() {

        console.log(
            "Erro na conexão WebSocket"
        );

    };

}


function entrar() {

    const usuario =
        document.getElementById(
            "usuario"
        ).value.trim();


    if (!usuario) {

        alert(
            "Digite seu nome."
        );

        return;

    }


    if (
        socket.readyState !==
        WebSocket.OPEN
    ) {

        alert(
            "O servidor ainda não está conectado."
        );

        return;

    }


    const mensagem = {

        tipo: "entrar",

        dados: {

            usuario: usuario

        }

    };


    socket.send(
        JSON.stringify(
            mensagem
        )
    );

}


function selecionarTime(
    jogo,
    time,
    odd
) {

    jogoSelecionado = jogo;

    timeSelecionado = time;

    oddSelecionada = odd;


    document.getElementById(
        "timeSelecionado"
    ).textContent =
        time +
        " - odd " +
        odd;

}


function apostar() {

    if (!usuarioRegistrado) {

        alert(
            "Entre no sistema primeiro."
        );

        return;

    }


    if (!timeSelecionado) {

        alert(
            "Escolha um time."
        );

        return;

    }


    const valor =
        Number(
            document.getElementById(
                "valor"
            ).value
        );


    if (
        !valor ||
        valor <= 0
    ) {

        alert(
            "Digite um valor válido."
        );

        return;

    }


    const aposta = {

        tipo: "aposta",

        dados: {

            jogo:
                jogoSelecionado,

            time:
                timeSelecionado,

            valor:
                valor,

            odd:
                oddSelecionada

        }

    };


    socket.send(
        JSON.stringify(
            aposta
        )
    );


    document.getElementById(
        "valor"
    ).value = "";

}


function atualizarSaldo(
    saldo
) {

    document.getElementById(
        "saldo"
    ).textContent =
        Number(
            saldo
        ).toFixed(2);

}


function mostrarAposta(
    aposta
) {

    const mensagens =
        document.getElementById(
            "mensagens"
        );


    const elemento =
        document.createElement(
            "div"
        );


    elemento.className =
        "mensagem";


    elemento.innerHTML = `
        <strong>
            ${aposta.usuario}
        </strong>

        apostou

        <strong>
            R$
            ${Number(
                aposta.valor
            ).toFixed(2)}
        </strong>

        em

        <strong>
            ${aposta.time}
        </strong>

        (odd ${aposta.odd})
    `;


    mensagens.prepend(
        elemento
    );

}


function mostrarResultado(
    dados
) {

    const elemento =
        document.getElementById(
            "resultado-" +
            dados.jogo
        );


    if (elemento) {

        elemento.textContent =
            "Resultado: " +
            dados.vencedor +
            " venceu!";

        elemento.classList.add(
            "finalizado"
        );

    }


    adicionarMensagem(
        "🏆 " +
        dados.vencedor +
        " venceu a partida!"
    );

}


function adicionarMensagem(
    texto
) {

    const mensagens =
        document.getElementById(
            "mensagens"
        );


    const elemento =
        document.createElement(
            "div"
        );


    elemento.className =
        "mensagem";


    elemento.textContent =
        texto;


    mensagens.prepend(
        elemento
    );

}


conectar();