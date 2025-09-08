import socket
import threading

def receive_messages(sock):
    """서버로부터 메시지를 수신하는 함수"""
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def main():
    host = '127.0.0.1'  # 서버 IP (로컬 환경이므로 127.0.0.1)
    port = 8888         # 서버 포트

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # 메시지 수신 스레드 시작
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    print("채팅 서버에 연결되었습니다. '/종료'를 입력해 종료하세요.")
    print("귓속말은 '/귓속말 [대상 IP:Port] [메시지]' 형식으로 입력하세요.")

    while True:
        try:
            message = input('')
            if message == '/종료':
                client_socket.sendall(message.encode())
                break
            client_socket.sendall(message.encode())
        except EOFError:
            break
        except Exception as e:
            print(f"오류 발생: {e}")
            break

    client_socket.close()

if __name__ == '__main__':
    main()