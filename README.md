# FAKEBET

## Disciplina: COMPUTAÇÃO DISTRIBUÍDA
## Alunos: Alice Segatto, Aline Hoffmann, Ana Amaral, Pedro Segatto e Thaise Zanin.

O FakeBet é um projeto desenvolvido para praticar os conceitos de WebSocket e Computação Distribuída. A aplicação simula uma plataforma de apostas esportivas utilizando apenas valores fictícios, sem envolver dinheiro real.

O sistema utiliza Python com Tornado no servidor e HTML, CSS e JavaScript no cliente. A comunicação é realizada por meio de WebSocket, permitindo uma conexão contínua e bidirecional entre o navegador e o servidor.

## Comunicação via WebSocket

A comunicação entre o cliente e o servidor é realizada utilizando WebSocket.

Diferentemente de uma comunicação HTTP tradicional, o WebSocket mantém uma
conexão aberta entre o navegador e o servidor, permitindo a troca de
mensagens nos dois sentidos em tempo real.

No FakeBet, essa comunicação é utilizada para:

- registrar novos usuários;
- enviar apostas ao servidor;
- validar e processar as apostas;
- compartilhar novas apostas com os usuários conectados;
- informar os resultados das partidas;
- atualizar os saldos dos usuários.

Dessa forma, as informações podem ser atualizadas nos clientes conectados
sem a necessidade de recarregar a página.

Cada usuário começa com um saldo fictício de R$ 1.000,00 e pode escolher um time e informar o valor que deseja apostar. Quando uma aposta é realizada, o servidor valida as informações, e se forem válidas, desconta o valor do saldo e compartilha a aposta em tempo real com todos os usuários conectados.

Os resultados das partidas são previamente definidos e divulgados automaticamente 40 segundos após a primeira aposta em cada jogo. O servidor verifica quais apostas foram vencedoras, calcula os prêmios de acordo com as odds e atualiza os saldos dos usuários. Todas essas informações são enviadas automaticamente aos navegadores, sem a necessidade de atualizar a página.

### Para executar o projeto:

Primeiro, é necessário ter o Python instalado. No terminal, dentro da pasta do projeto, instale a biblioteca Tornado.
 ```
pip install tornado
```

Depois, inicie o servidor.
```
python main.py
```

Em seguida, no navegador, acesse:
```
http://localhost:8888
````
