# Fakebet

O FakeBet é um projeto desenvolvido para praticar os conceitos de WebSocket e Computação Distribuída. A aplicação simula uma plataforma de apostas esportivas utilizando apenas valores fictícios, sem envolver dinheiro real.

O sistema utiliza Python com Tornado no servidor e HTML, CSS e JavaScript no cliente. A comunicação entre navegador e servidor é feita através de WebSocket, permitindo uma conexão contínua e bidirecional, conforme estudado em aula.

Cada usuário começa com um saldo fictício de R$ 1.000,00 e pode escolher um time e informar o valor que deseja apostar. Quando uma aposta é realizada, ela é enviada ao servidor e distribuída em tempo real para todos os usuários conectados, permitindo visualizar as apostas simultaneamente em diferentes abas ou navegadores.

O objetivo principal do projeto é demonstrar de forma simples o funcionamento da comunicação cliente-servidor em tempo real, utilizando mensagens em JSON e uma conexão WebSocket persistente.
