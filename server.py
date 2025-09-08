import socket
import threading

# 클라이언트 리스트와 락
clients = []
lock = threading.Lock()


def broadcast(message, sender_socket=None):
    """
    모든 클라이언트에게 메시지를 브로드캐스트합니다.
    """
    with lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode())
                except:
                    # 연결 끊긴 클라이언트는 리스트에서 제거
                    client.close()
                    clients.remove(client)


def handle_client(client_socket, addr):
    """
    개별 클라이언트의 연결을 처리하는 함수입니다.
    """
    print(f'새로운 연결: {addr}')

    # 클라이언트 입장 메시지 브로드캐스트
    entry_message = f'📢 {addr[0]}:{addr[1]}님이 입장하셨습니다.'.encode()
    broadcast(entry_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                break
            
            # /종료 명령어 처리
            if message.strip() == '/종료':
                print(f'{addr}님이 연결을 종료했습니다.')
                break
            
            # 귓속말 기능 처리: /귓속말 [대상 IP:Port] [메시지]
            if message.strip().startswith('/귓속말'):
                parts = message.split(' ', 2)
                if len(parts) == 3:
                    target_addr_str = parts[1]
                    whisper_message = parts[2]
                    whisper_to_client(target_addr_str, whisper_message, addr)
            else:
                # 일반 메시지 브로드캐스트
                formatted_message = f'👤 {addr[0]}:{addr[1]}> {message}'
                print(formatted_message)
                broadcast(formatted_message.encode(), client_socket)

        except ConnectionResetError:
            print(f'{addr}님이 강제로 연결을 종료했습니다.')
            break
        except Exception as e:
            print(f'에러 발생: {e}')
            break

    # 연결 종료 시 클라이언트 리스트에서 제거 및 소켓 닫기
    with lock:
        if client_socket in clients:
            clients.remove(client_socket)
            print(f'현재 접속자 수: {len(clients)}명')
    
    # 퇴장 메시지 브로드캐스트
    exit_message = f'🚪 {addr[0]}:{addr[1]}님이 퇴장하셨습니다.'.encode()
    broadcast(exit_message)

    client_socket.close()


def whisper_to_client(target_addr_str, message, sender_addr):
    """
    특정 클라이언트에게만 귓속말을 보냅니다.
    """
    target_found = False
    with lock:
        for client in clients:
            if f'{client.getpeername()[0]}:{client.getpeername()[1]}' == target_addr_str:
                try:
                    whisper = f'(귓속말) 🤫 {sender_addr[0]}:{sender_addr[1]}> {message}'.encode()
                    client.sendall(whisper)
                    target_found = True
                    break
                except Exception as e:
                    print(f'귓속말 전송 에러: {e}')
    
    # 귓속말을 보낸 클라이언트에게 성공 또는 실패 메시지 전송
    sender_socket = None
    with lock:
        for client in clients:
            if client.getpeername() == sender_addr:
                sender_socket = client
                break
    
    if sender_socket:
        if target_found:
            sender_socket.sendall(f'[INFO] {target_addr_str}에게 귓속말을 보냈습니다.'.encode())
        else:
            sender_socket.sendall(f'[INFO] {target_addr_str}를 찾을 수 없습니다.'.encode())


def main():
    """
    서버를 시작하고 클라이언트의 연결을 기다립니다.
    """
    host = '0.0.0.0'  # 모든 IP로부터 접속 허용
    port = 8888       # 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    
    print(f'채팅 서버가 {host}:{port}에서 시작되었습니다.')
    print('클라이언트의 연결을 기다리는 중...')

    try:
        while True:
            client_socket, addr = server_socket.accept()
            with lock:
                clients.append(client_socket)
                print(f'현재 접속자 수: {len(clients)}명')
            
            # 클라이언트 처리를 위한 스레드 생성
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True # 메인 스레드 종료 시 함께 종료
            client_thread.start()

    except KeyboardInterrupt:
        print('서버를 종료합니다.')
    finally:
        server_socket.close()
        for client in clients:
            client.close()


if __name__ == '__main__':
    main()