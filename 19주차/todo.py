# todo.py

import csv
import os
from typing import Dict, List, Any
from fastapi import FastAPI, APIRouter, HTTPException, status

# --- CSV 파일 설정 및 헬퍼 함수 ---

# 제약사항: CSV 파일을 사용해 데이터 저장
CSV_FILE = 'todos.csv'

def load_todos() -> List[Dict[str, Any]]:
    """
    앱 시작 시 CSV 파일에서 할 일 목록을 로드합니다.
    """
    if not os.path.exists(CSV_FILE):
        return []
    
    todos = []
    try:
        # PEP 8 준수: ' ' 사용
        with open(CSV_FILE, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                todos.append(row)
    except Exception:
        # 파일이 비어있거나 헤더가 없는 경우
        return []
    return todos

def save_todos(todos: List[Dict[str, Any]]):
    """
    새로운 할 일이 추가될 때 전체 목록을 CSV 파일에 저장합니다.
    """
    if not todos:
        # 리스트가 비어있으면 빈 파일로 덮어씁니다.
         with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
             f.write('')
         return

    # PEP 8 준수: = 앞뒤 공백
    # 첫 번째 항목의 키를 헤더(fieldnames)로 사용
    fieldnames = todos[0].keys()
    
    with open(CSV_FILE, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todos)

# --- FastAPI 애플리케이션 설정 ---

app = FastAPI()
router = APIRouter()

# 리스트 객체 'todo_list' (앱 시작 시 CSV에서 로드)
todo_list: List[Dict[str, Any]] = load_todos()


# --- API 라우트 정의 (APIRouter 사용) ---

@router.post('/add_todo', response_model=Dict[str, str])
async def add_todo(todo: Dict[str, Any]) -> Dict[str, str]:
    
    # 보너스 과제: 입력되는 Dict 타입이 빈값이면 경고를 돌려줌
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Input dictionary cannot be empty.'
        )
    
    # 헤더(키)가 일치하는지 확인 (간단한 검사)
    if todo_list and todo.keys() != todo_list[0].keys():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Input keys do not match existing structure: {list(todo_list[0].keys())}'
        )

    todo_list.append(todo)
    save_todos(todo_list)  # CSV 파일에 즉시 저장
    
    return {'message': 'Todo added successfully.'}


# 2. Todo 목록 조회 (GET)
# 제약사항: 입출력은 Dict 타입
@router.get('/retrieve_todo', response_model=Dict[str, List[Dict[str, Any]]])
async def retrieve_todo() -> Dict[str, List[Dict[str, Any]]]:
    return {'data': todo_list}


# 생성한 라우터를 기본 앱에 포함
app.include_router(router)
