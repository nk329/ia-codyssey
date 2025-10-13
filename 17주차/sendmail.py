import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os


def send_mail(sender_email, sender_password, receiver_email, subject, body, attachment_path=None):
    """SMTP를 이용해 Gmail로 메일을 전송하는 함수"""

    try:
        # 메일 기본 구성
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 본문 추가
        msg.attach(MIMEText(body, 'plain'))

        # 첨부 파일이 있는 경우
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

        # Gmail SMTP 서버 연결 (포트 587: STARTTLS)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 보안 연결
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('로그인에 실패했습니다. 이메일 주소나 앱 비밀번호를 확인하세요.')
    except FileNotFoundError:
        print('첨부 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'메일 전송 중 오류가 발생했습니다: {e}')


def main():
    """메일 전송 프로그램 메인 함수"""
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_app_password'  # Gmail 앱 비밀번호 사용
    receiver_email = 'receiver@example.com'

    subject = '테스트 메일'
    body = '이 메일은 Python의 smtplib을 사용하여 전송되었습니다.'
    attachment_path = None  # 예: 'C:/Users/username/Desktop/test.txt'

    send_mail(sender_email, sender_password, receiver_email, subject, body, attachment_path)


if __name__ == '__main__':
    main()
