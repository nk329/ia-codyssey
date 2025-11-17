# main.py
import csv
import os
from fastapi import FastAPI, HTTPException
from model import TodoItem # model.py에서 TodoItem 모델 가져오기

# PEP 8 가이드 준수 (대입문 = 앞뒤 공백)
app = FastAPI()

# 상수는 대문자로 표기
TODO_FILE = 'todo.csv'
FIELDNAMES = ['id', 'item']

# 데이터베이스 대신 사용할 인메모리 리스트
todos_db = []

# --- CSV Helper Functions ---

def load_db():
    """
    앱 시작 시 todo.csv 파일에서 데이터를 읽어 todos_db 리스트에 로드합니다.
    """
    global todos_db
    todos_db = [] # 기존 리스트 초기화
    
    # 파일이 존재하지 않으면, 헤더만 있는 빈 파일 생성
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        return

    # 파일 읽기
    with open(TODO_FILE, mode='r', newline='', encoding='utf-8') as f:
        # csv 파일을 딕셔너리 형태로 읽어옵니다.
        reader = csv.DictReader(f)
        for row in reader:
            # id는 정수형(int)으로 변환
            try:
                row['id'] = int(row['id'])
                todos_db.append(row)
            except (ValueError, TypeError):
                # ID가 숫자가 아닌 잘못된 데이터는 건너뜁니다.
                continue

def save_db():
    """
    현재 todos_db 리스트의 내용을 todo.csv 파일에 덮어씁니다.
    """
    with open(TODO_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader() # CSV 헤더(id, item) 작성
        writer.writerows(todos_db) # 데이터 전체 작성

# --- Helper Functions ---

def find_todo_by_id(todo_id: int):
    """
    todos_db 리스트에서 id로 todo 항목을 찾습니다.
    """
    for todo in todos_db:
        if todo['id'] == todo_id:
            return todo
    return None # 찾지 못하면 None 반환

def get_next_id():
    """
    새로운 todo 항목에 할당할 다음 ID를 계산합니다.
    """
    if not todos_db:
        return 1
    # todos_db에서 'id' 값 중 최대값을 찾아 1을 더합니다.
    return max(todo['id'] for todo in todos_db) + 1

# --- FastAPI Events ---

@app.on_event('startup')
def on_startup():
    """
    FastAPI 앱이 시작될 때 CSV 파일에서 데이터를 로드합니다.
    """
    load_db()

# --- API Endpoints ---

# (참고) 이전에 구현했던 전체 조회 기능
@app.get('/todos')
def get_all_todos():
    """
    모든 todo 항목을 반환합니다.
    """
    return todos_db

# (참고) 이전에 구현했던 생성 기능
@app.post('/todos')
def create_todo(todo_item: TodoItem):
    """
    새로운 todo 항목을 생성합니다.
    """
    new_todo = {
        'id': get_next_id(),
        'item': todo_item.item
    }
    todos_db.append(new_todo)
    save_db() # 변경 사항을 CSV 파일에 저장
    return new_todo


@app.get('/todos/{todo_id}')
def get_single_todo(todo_id: int):
    """
    경로 매개변수 todo_id를 받아 개별 todo 항목을 조회합니다.
    """
    todo = find_todo_by_id(todo_id)
    if todo is None:
        # 항목이 없으면 404 Not Found 오류 발생
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo


@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, todo_item: TodoItem):
    """
    경로 매개변수 todo_id와 요청 본문(TodoItem)을 받아
    기존 todo 항목을 수정합니다.
    """
    todo = find_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    # 인메모리 리스트(todos_db)의 항목을 직접 수정
    todo['item'] = todo_item.item
    
    save_db() # 변경 사항을 CSV 파일에 저장
    return todo


@app.delete('/todos/{todo_id}')
def delete_single_todo(todo_id: int):
    """
    경로 매개변수 todo_id를 받아 해당 todo 항목을 삭제합니다.
    """
    global todos_db
    todo = find_todo_by_id(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    # 리스트 컴프리헨션을 사용하여 해당 id를 제외한 새 리스트 생성
    # PEP 8 준수: 비교 연산자 '!=' 앞뒤 공백
    todos_db = [t for t in todos_db if t['id'] != todo_id]
    
    save_db() # 변경 사항을 CSV 파일에 저장
    
    # 삭제 성공 시 간단한 메시지 반환
    return {'message': 'Todo deleted successfully'}
