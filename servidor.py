import socket
import threading
import time

# estado inicial do jogo
ball_pos = [40, 12]  # Inicializa a bolinha no centro
ball_dir = [1, 1]
paddle1_pos = 10
paddle2_pos = 10
score1 = 0
score2 = 0

clients = []
client_ids = {}  # socket: player_id
lock = threading.Lock()

# Função para centralizar a bolinha na tela
def center_ball():
    max_x, max_y = 80, 24  # Defina as dimensões máximas da janela
    return [max_x // 2, max_y // 2]  # Centraliza a bolinha

# envia estado do jogo a todos os clientes
def broadcast_state():
    msg = f"UPDATE {ball_pos[0]} {ball_pos[1]} {paddle1_pos} {paddle2_pos} {score1} {score2}\n"
    for client in clients:
        try:
            client.sendall(msg.encode())
        except:
            continue

# atualiza a lógica do jogo (movimento da bola, colisões, etc)
def game_loop():
    global ball_pos, ball_dir, paddle1_pos, paddle2_pos, score1, score2

    max_x, max_y = 80, 24  # Defina as dimensões máximas da janela

    while True:
        with lock:
            # Inicializa a bolinha se ainda não foi inicializada
            if not ball_pos:
                ball_pos = center_ball()  # Centraliza a bolinha

            # movimenta a bola
            ball_pos[0] += ball_dir[0]
            ball_pos[1] += ball_dir[1]

            # colisão com o topo/baixo
            if ball_pos[1] <= 0 or ball_pos[1] >= max_y - 1:
                ball_dir[1] = -ball_dir[1]

            # colisão com as raquetes
            if ball_pos[0] == 2 and paddle1_pos <= ball_pos[1] <= paddle1_pos + 3:
                ball_dir[0] = -ball_dir[0]
            elif ball_pos[0] == 77 and paddle2_pos <= ball_pos[1] <= paddle2_pos + 3:
                ball_dir[0] = -ball_dir[0]

            # pontuação
            if ball_pos[0] <= 0:
                score2 += 1
                ball_pos = center_ball()  # Reposiciona no centro
                ball_dir = [1, 1]
            elif ball_pos[0] >= max_x - 1:
                score1 += 1
                ball_pos = center_ball()  # Reposiciona no centro
                ball_dir = [-1, 1]

            broadcast_state()

        time.sleep(0.05)

# função para gerenciar cada cliente
def handle_client(client_socket, addr):
    global paddle1_pos, paddle2_pos

    with lock:
        if len(client_ids) == 0:
            player_id = 1
        elif len(client_ids) == 1:
            player_id = 2
        else:
            client_socket.send(b"Servidor cheio.\n")
            client_socket.close()
            return

        client_ids[client_socket] = player_id
        clients.append(client_socket)

    print(f"Jogador {player_id} conectado de {addr}")
    client_socket.send(f"ID {player_id}\n".encode())
    client_socket.send(f"START {ball_pos[0]} {ball_pos[1]} {paddle1_pos} {paddle2_pos} {score1} {score2}\n".encode())

    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            with lock:
                if data == 'UP' and player_id == 1:
                    paddle1_pos = max(0, paddle1_pos - 1)
                elif data == 'DOWN' and player_id == 1:
                    paddle1_pos = min(23, paddle1_pos + 1)
                elif data == 'UP2' and player_id == 2:
                    paddle2_pos = max(0, paddle2_pos - 1)
                elif data == 'DOWN2' and player_id == 2:
                    paddle2_pos = min(23, paddle2_pos + 1)

    except Exception as e:
        print(f"Erro com o cliente {addr}: {e}")

    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
        if client_socket in client_ids:
            del client_ids[client_socket]
        client_socket.close()
    print(f"Jogador {player_id} ({addr}) desconectado")

# inicializa o servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)
    print("Aguardando conexões...")

    # inicia o loop do jogo em uma thread separada
    threading.Thread(target=game_loop, daemon=True).start()

    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
