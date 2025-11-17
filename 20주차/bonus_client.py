import urllib.request
import json
import sys # PEP 8 준수를 위해 import는 파일 상단에 모아서 작성

BASE_URL = 'http://127.0.0.1:8000'

def request_helper(url, method='GET', data=None):
    """
    urllib.request를 사용해 API를 호출하는 헬퍼 함수
    """
    # PEP 8 준수: 괄호 안에서는 = 앞뒤 공백 생략 가능하나, 일관성을 위해 추가
    req = urllib.request.Request(url, method=method)
    
    body = None
    if data:
        # 데이터가 있으면 JSON 문자열로 변환 후 bytes로 인코딩
        body = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Content-Length', len(body))
    
    try:
        # data 매개변수는 POST/PUT 요청의 본문을 의미
        with urllib.request.urlopen(req, data=body) as response:
            response_body = response.read().decode('utf-8')
            # 응답이 비어있지 않으면 JSON 파싱
            if response_body:
                return json.loads(response_body)
            return {'status': response.status, 'message': 'Success (No Content)'}
            
    except urllib.error.HTTPError as e:
        # HTTP 오류 발생 시
        print(f'[Error] {e.code}: {e.read().decode("utf-8")}', file=sys.stderr)
        return None
    except Exception as e:
        print(f'[Client Error] {e}', file=sys.stderr)
        return None

def main():
    """
    클라이언트 앱 실행 메인 함수
    """
    print('--- 1. 현재 모든 Todo 조회 (GET /todos) ---')
    todos = request_helper(f'{BASE_URL}/todos')
    if todos:
        print(f'-> 응답: {todos}\n')

    print('--- 2. ID 3번 항목 수정 (PUT /todos/3) ---')
    update_data = {'item': '저녁 장보기 (수정됨)'}
    updated = request_helper(f'{BASE_URL}/todos/3', method='PUT', data=update_data)
    if updated:
        print(f'-> 응답: {updated}\n')

    print('--- 3. ID 1번 항목 삭제 (DELETE /todos/1) ---')
    deleted = request_helper(f'{BASE_URL}/todos/1', method='DELETE')
    if deleted:
        print(f'-> 응답: {deleted}\n')

    print('--- 4. 최종 Todo 목록 확인 (GET /todos) ---')
    final_todos = request_helper(f'{BASE_URL}/todos')
    if final_todos:
        print(f'-> 응답: {final_todos}\n')

# 이 스크립트가 직접 실행될 때만 main() 함수 호출
if __name__ == '__main__':
    # 서버가 실행 중인지 확인
    print(f'FastAPI 서버 ({BASE_URL})에 연결을 시도합니다...')
    print('서버가 실행 중이 아니면 (uvicorn main:app --reload)를 먼저 실행하세요.\n')
    main()
