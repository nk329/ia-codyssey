import sys  # 시스템 관련 기능 사용 (명령줄 인자 등)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit  # PyQt5 위젯 임포트
from PyQt5.QtGui import QFont  # 폰트 관련 클래스 임포트
from PyQt5.QtCore import Qt  # Qt의 상수(정렬 옵션 등) 임포트


class CalculatorCore:  # 계산 기능만 담당하는 코어 클래스
    def __init__(self):
        self.reset()  # 시작할 때 값 초기화

    def reset(self):
        self.current = '0'  # 현재 입력된 값 (기본 '0')
        self.operator = None  # 현재 선택된 연산자
        self.operand = None  # 첫 번째 피연산자
        self.result_shown = False  # 결과가 화면에 표시된 상태 여부

    def input_number(self, num):  # 숫자 버튼을 눌렀을 때 처리
        if self.result_shown:  # 결과가 이미 나왔으면 새로 입력 시작
            self.current = num
            self.result_shown = False
        else:
            if self.current == '0':  # '0'이면 덮어쓰기
                self.current = num
            else:  # 그 외엔 뒤에 붙이기
                self.current += num

    def input_dot(self):  # 소수점 입력
        if '.' not in self.current:  # 이미 소수점이 없다면 추가
            self.current += '.'

    def set_operator(self, operator):  # 연산자 버튼 누를 때
        if self.operator and not self.result_shown:  # 기존에 연산자가 있으면 먼저 계산
            self.calculate()
        self.operand = self.current  # 현재 값을 operand로 저장
        self.operator = operator  # 연산자 설정
        self.result_shown = False
        self.current = '0'  # 다음 입력을 위해 current 리셋

    def calculate(self):  # '=' 누르거나 연산자 누를 때 계산
        try:
            if self.operator is None:
                return

            a = float(self.operand)  # 첫 번째 숫자
            b = float(self.current)  # 두 번째 숫자

            if self.operator == '+':
                result = a + b
            elif self.operator == '-':
                result = a - b
            elif self.operator == '×':
                result = a * b
            elif self.operator == '÷':
                if b == 0:  # 0으로 나누면 오류 처리
                    self.current = '0으로 나눌 수 없습니다'
                    return
                result = a / b
            else:
                result = b  # 연산자가 없으면 그냥 두 번째 숫자

            if isinstance(result, float):  # 결과가 소수이면
                self.current = str(round(result, 6))  # 소수점 6자리까지만 반올림
            else:
                self.current = str(result)

            self.result_shown = True  # 결과 표시 상태로 변경
            self.operator = None  # 연산자 초기화

        except Exception:  # 모든 예외 처리
            self.current = 'Error'

    def toggle_sign(self):  # '+/-' 버튼 처리
        if self.current.startswith('-'):
            self.current = self.current[1:]  # '-'를 제거
        else:
            if self.current != '0':
                self.current = '-' + self.current  # 앞에 '-' 추가

    def percent(self):  # '%' 버튼 처리
        try:
            value = float(self.current) / 100  # 100으로 나누기
            self.current = str(round(value, 6))  # 소수점 6자리로
        except Exception:
            self.current = 'Error'


class Calculator(QWidget):  # 실제 GUI를 담당하는 메인 클래스
    def __init__(self):
        super().__init__()
        self.setWindowTitle('JNK Calculator')  # 윈도우 제목 설정
        self.setFixedSize(320, 480)  # 고정 사이즈 설정

        self.calculator = CalculatorCore()  # 계산기 코어 생성

        self.init_ui()  # UI 초기화

    def init_ui(self):
        self.display = QLineEdit()  # 숫자나 결과를 표시할 화면
        self.display.setReadOnly(True)  # 읽기 전용
        self.display.setAlignment(Qt.AlignRight)  # 오른쪽 정렬
        self.display.setFont(QFont('Arial', 32))  # 폰트 설정
        self.display.setStyleSheet('background-color: black; color: white; border: none;')  # 스타일
        self.display.setFixedHeight(80)  # 높이 고정

        grid = QGridLayout()  # 버튼을 그리드로 배치할 레이아웃
        buttons = [  # 버튼 텍스트 배열
            ['AC', '+/-', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        for row in range(len(buttons)):  # 버튼 생성 반복
            for col in range(len(buttons[row])):
                text = buttons[row][col]
                button = QPushButton(text)  # 버튼 객체 생성
                button.setFont(QFont('Arial', 18))
                button.setFixedSize(70, 70)

                # 버튼 색상 스타일 지정
                if text in ['AC', '+/-', '%']:
                    button.setStyleSheet('background-color: #a5a5a5; color: black; border-radius: 35px;')
                elif text in ['÷', '×', '-', '+', '=']:
                    button.setStyleSheet('background-color: #ff9500; color: white; border-radius: 35px;')
                else:
                    button.setStyleSheet('background-color: #333333; color: white; border-radius: 35px;')

                button.clicked.connect(self.button_clicked)  # 버튼 클릭 연결

                # 버튼 위치 배치 (특수: 0번 버튼은 두 칸 차지)
                if text == '0':
                    grid.addWidget(button, row, 0, 1, 2)
                elif text == '.' and row == 4:
                    grid.addWidget(button, row, 2)
                elif text == '=' and row == 4:
                    grid.addWidget(button, row, 3)
                else:
                    if text != '0':
                        grid.addWidget(button, row, col)

        layout = QVBoxLayout()  # 세로 박스 레이아웃
        layout.addWidget(self.display)  # 위에 디스플레이 추가
        layout.addLayout(grid)  # 아래에 버튼 그리드 추가
        self.setLayout(layout)
        self.setStyleSheet('background-color: black;')  # 전체 배경 검정
        self.update_display()  # 디스플레이 갱신

    def button_clicked(self):  # 버튼 클릭 시 처리
        clicked_button = self.sender()  # 누른 버튼 찾기
        value = clicked_button.text()  # 버튼 텍스트 읽기

        if value == 'AC':
            self.calculator.reset()
        elif value == '+/-':
            self.calculator.toggle_sign()
        elif value == '%':
            self.calculator.percent()
        elif value in ['+', '-', '×', '÷']:
            self.calculator.set_operator(value)
        elif value == '=':
            self.calculator.calculate()
        elif value == '.':
            self.calculator.input_dot()
        else:
            self.calculator.input_number(value)

        self.update_display()  # 클릭 후 화면 업데이트

    def update_display(self):  # 디스플레이 새로 고침
        text = self.calculator.current  # 현재 값을 읽음

        # 결과 길이에 따라 폰트 크기 자동 조정 (보너스 과제)
        if len(text) > 12:
            font_size = 18
        elif len(text) > 8:
            font_size = 24
        else:
            font_size = 32

        self.display.setFont(QFont('Arial', font_size))  # 폰트 재설정
        self.display.setText(text)  # 텍스트 표시


if __name__ == '__main__':  # 메인 실행 진입점
    app = QApplication(sys.argv)  # 앱 객체 생성
    calc = Calculator()  # 계산기 생성
    calc.show()  # 윈도우 띄우기
    sys.exit(app.exec_())  # 이벤트 루프 실행
