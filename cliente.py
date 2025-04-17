import socket
import curses
import time
import threading

# Estado compartilhado
ball_pos = [40, 12]
paddle1_pos = 10
paddle2_pos = 10
score1 = 0
score2 = 0
player_id = None
lock = threading.Lock()

# Desenha o estado do jogo no terminal
def draw_game(stdscr):
    global ball_pos, paddle1_pos, paddle2_pos, score1, score2, player_id

    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        with lock:
            stdscr.clear()
            height, width = stdscr.getmaxyx()

            # Bola
            stdscr.addstr(ball_pos[1], ball_pos[0], 'O')

            # Raquetes
            for i in range(paddle1_pos, paddle1_pos + 4):
                if 0 <= i < height:
                    stdscr.addstr(i, 1, '|')
            for i in range(paddle2_pos, paddle2_pos + 4):
                if 0 <= i < height:
                    stdscr.addstr(i, width - 2, '|')

            # Placar
            stdscr.addstr(0, width // 2 - 12, f"Jogador 1: {score1} | Jogador 2: {score2}")

            # Mostra o ID do jogador
            if player_id:
                stdscr.addstr(1, width // 2 - 5, f"Você é o Jogador {player_id}")

            stdscr.refresh()

        time.sleep(0.05)

# thread que recebe os dados do servidor
def receive_data(client):
    global ball_pos, paddle1_pos, paddle2_pos, score1, score2, player_id

    while True:
        try:
            data = client.recv(1024).decode().strip()
            if not data:
                break

            with lock:
                for line in data.split('\n'):
                    if line.startswith("ID"):
                        _, pid = line.split()
                        player_id = int(pid)

                    elif line.startswith("START") or line.startswith("UPDATE"):
                        parts = line.split()
                        ball_pos = [int(parts[1]), int(parts[2])]
                        paddle1_pos = int(parts[3])
                        paddle2_pos = int(parts[4])
                        score1 = int(parts[5])
                        score2 = int(parts[6])

        except Exception as e:
            print(f"[ERRO] {e}")
            break

# Loop principal do jogo
def game_loop(stdscr):
    global player_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    # Inicia thread para receber dados
    threading.Thread(target=receive_data, args=(client,), daemon=True).start()

    # Inicia thread para desenhar o jogo
    threading.Thread(target=draw_game, args=(stdscr,), daemon=True).start()

    # Espera até o player_id ser recebido
    while player_id is None:
        time.sleep(0.1)

    # Loop de controle
    while True:
        key = stdscr.getch()

        if key in [ord('w'), curses.KEY_UP, 72]:  # Movimento para cima
            if player_id == 1:
                client.sendall(b'UP\n')
            elif player_id == 2:
                client.sendall(b'UP2\n')
        elif key in [ord('s'), curses.KEY_DOWN, 80]:  # Movimento para baixo
            if player_id == 1:
                client.sendall(b'DOWN\n')
            elif player_id == 2:
                client.sendall(b'DOWN2\n')

        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(game_loop)
