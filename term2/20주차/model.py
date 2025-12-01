from pydantic import BaseModel

# 클래스 이름은 CapWord(PascalCase) 규약을 따릅니다.
class TodoItem(BaseModel):
    """
    Todo 항목 생성을 위한 모델 (id가 없음)
    수정(PUT) 및 생성(POST) 시 Request Body로 사용됩니다.
    """
    item: str
