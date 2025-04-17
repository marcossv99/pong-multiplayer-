# 🕹️ Pong Multiplayer Terminal - Sincronização com Sockets TCP

Este projeto implementa uma versão multiplayer do clássico jogo Pong em um ambiente de terminal. Dois jogadores podem jogar simultaneamente por meio de uma conexão TCP, com toda a lógica do jogo controlada por um servidor central.

---

## 🎮 Estrutura do Jogo

### 🧠 Servidor

- Mantém o **estado global do jogo**, incluindo:
  - Posição da bola
  - Posições das raquetes
  - Pontuação dos jogadores
- Envia atualizações em tempo real para os clientes conectados.
- Gerencia a comunicação entre jogadores via **protocolo TCP**.

### 🧍 Cliente

- Envia comandos de controle ao servidor (movimentação das raquetes).
- Recebe do servidor as atualizações da posição da bola, das raquetes e do placar.
- Desenha o jogo no terminal usando a biblioteca `curses`.
- Permite que os jogadores controlem suas raquetes com:
  - `W`: mover para cima
  - `S`: mover para baixo

---

## ⚙️ Funcionamento Interno

### 🔁 Estado Inicial

O estado do jogo é armazenado em variáveis globais:
- `ball_pos`: posição da bola
- `paddle1_pos`, `paddle2_pos`: posições das raquetes
- `score1`, `score2`: placar

### 💬 Comunicação Cliente-Servidor

Cada cliente envia comandos como `UP`, `DOWN`, `UP2`, `DOWN2`, dependendo do jogador.

O servidor recebe esses comandos, atualiza o estado do jogo, e envia as novas posições da bola, raquetes e placar para todos os clientes conectados.

### 🧱 Física Simples da Bola

- A bola se move automaticamente no eixo X e Y.
- Quando colide com as bordas superior ou inferior, ela rebate verticalmente.
- Se a bola ultrapassar uma das laterais sem ser interceptada pela raquete, o outro jogador marca ponto.
- A bola é reiniciada no centro após cada ponto.

---

## 📦 Requisitos

- Python 3.6+
- Terminal compatível com a biblioteca `curses` (Linux, macOS, ou WSL no Windows)

---

## 🚀 Como Executar

### 1. Inicie o servidor

```bash
python servidor.py


!!! IMPORTANTE

### Entre na pasta do projeto, digite cmd na 'barra de pesquisa' do explorador de arquivos, ao abrir o cmd digite python cliente.py para iniciar como o jogador 1 ###