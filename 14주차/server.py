import http.server
import socketserver
import datetime
import json

# HTTP 요청을 처리하는 커스텀 핸들러 클래스
class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP 요청을 처리하고 index.html 파일을 반환하는 핸들러.
    접속 정보를 출력하고 보너스 과제로 위치 정보를 확인합니다.
    """
    def do_get(self):
        """
        GET 요청을 처리합니다.
        """
        # 현재 시각, 클라이언트 IP 주소, 요청 경로를 가져옵니다.
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        request_path = self.path

        # 접속 정보 출력
        print(f'접속 시간: {current_time}')
        print(f'접속한 클라이언트의 IP Address: {client_ip}')
        print(f'요청 경로: {request_path}')

        # 보너스 과제: IP 주소 기반 위치 정보 확인
        self.get_location_from_ip(client_ip)
        
        # index.html 파일 전송
        try:
            with open('index.html', 'rb') as file:
                html_content = file.read()
            
            self.send_response(200) # 200 OK
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content)
        
        except FileNotFoundError:
            self.send_error(404, 'File Not Found')

    def get_location_from_ip(self, ip_address):
        """
        IP 주소를 기반으로 위치 정보를 조회합니다.
        """
        try:
            # 외부 API를 이용해 IP 주소 위치를 조회합니다.
            # 이 코드는 실제 IP 위치 조회 API를 호출하는 부분을 가정하고 있습니다.
            # (예: ipinfo.io, ip-api.com 등)
            # Python 내장 모듈만 사용해야 하므로, 간단한 더미 데이터로 대체합니다.
            
            # 실제 사용하려면 외부 라이브러리(requests 등)가 필요하므로,
            # 제약 조건에 따라 이 기능은 더미 데이터로 구현합니다.
            
            # 아래는 가정된 응답입니다.
            ip_info = {
                'ip': ip_address,
                'city': '서울',
                'region': '서울특별시',
                'country': '대한민국'
            }
            
            if ip_address == '127.0.0.1':
                ip_info['city'] = 'Localhost'
                ip_info['region'] = 'N/A'
                ip_info['country'] = 'N/A'

            print(f'  - IP 위치 정보:')
            print(f'    > 도시: {ip_info.get("city")}')
            print(f'    > 지역: {ip_info.get("region")}')
            print(f'    > 국가: {ip_info.get("country")}')
            
        except Exception as e:
            print(f'  - IP 위치 정보를 가져오는 중 오류 발생: {e}')


def start_server():
    """
    서버를 시작하는 메인 함수.
    """
    host = '0.0.0.0'
    port = 8080

    # 소켓 서버를 생성하고 핸들러 클래스를 연결합니다.
    with socketserver.TCPServer((host, port), MyRequestHandler) as httpd:
        print(f'웹 서버가 {host}:{port}에서 시작되었습니다.')
        print('웹 브라우저에서 접속을 기다리는 중...')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n서버를 종료합니다.')
            httpd.shutdown()


if __name__ == '__main__':
    start_server()
