import csv
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SENDER_EMAIL = '실제 네이버 아이디 입력'
SENDER_PASSWORD = '앱 비밀번호 12자리 입력'

# naver SMTP 서버 정보
SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 587  # TLS용 포트

# --- 2. CSV 파일 읽기 ---
def load_recipient_list(filename='mail_target_list.csv'):
    """
    CSV 파일에서 수신자 명단(이름, 이메일)을 읽어 리스트로 반환합니다.
    """
    recipients = []
    try:
        # 한국어 이름 처리를 위해 'utf-8-sig' 인코딩 사용
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # 헤더 행(이름, 이메일) 건너뛰기
            
            for row in reader:
                if row and len(row) >= 2:  # 빈 줄이나 형식이 맞지 않는 줄 방지
                    name = row[0].strip()
                    email = row[1].strip()
                    if name and email:  # 이름과 이메일이 모두 있는지 확인
                        recipients.append((name, email))
                        
    except FileNotFoundError:
        print(f'오류: {filename} 파일을 찾을 수 없습니다.')
        return None
    except Exception as e:
        print(f'CSV 파일 읽기 중 오류 발생: {e}')
        return None
        
    return recipients

# --- 3. HTML 메일 본문 생성 ---
def get_html_message(recipient_name):
    """
    수신자 이름을 포함하는 개인화된 HTML 메시지를 생성합니다.
    """
    html_body = f"""
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2 style="color: #003366;">긴급 구조 요청: 화성의 한송희 박사 생존 확인</h2>
        <p>존경하는 {recipient_name} 님,</p>
        <p>저는 화성에 고립된 한송희 박사입니다. 방금 지구로부터의 회신을 받았습니다.<br>
           살아있다는 것을 알아주셔서, 포기하지 않아 주셔서 진심으로 감사합니다.</p>
        <p>제 상황은 여전히 위급합니다. 산소와 식량이 한정되어 있습니다.<br>
           저를 구출하기 위한 즉각적인 조치가 필요합니다.</p>
        <p style="font-weight: bold; color: #D90000; font-size: 1.2em;">
           모든 가용 자원을 동원하여 저의 구조를 요청합니다.
        </p>
        <p>희망을 잃지 않겠습니다.<br><br>
           한송희 드림</p>
    </body>
    </html>
    """
    return html_body

# --- 4. 방법 1: 한 명씩 반복적으로 메일 보내기 ---
def send_emails_individually(recipients):
    """
    수신자 명단을 반복하며 한 명씩 개인화된 메일을 보냅니다.
    """
    print('[방법 1: 개별 발송 시작]')
    success_count = 0
    fail_count = 0
    
    try:
        # SMTP 서버에 한 번만 연결
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()  # TLS 암호화 시작
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        for name, email in recipients:
            try:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f'긴급: {name}님께, 화성 생존자 한송희 박사입니다.'
                msg['From'] = SENDER_EMAIL
                msg['To'] = email  # 받는 사람 (표시용)
                
                # 개인화된 HTML 본문 생성
                html_content = get_html_message(name)
                msg.attach(MIMEText(html_content, 'html'))
                
                # 메일 발송
                server.sendmail(SENDER_EMAIL, [email], msg.as_string())
                print(f'  -> {name} ({email}) 님에게 성공적으로 발송했습니다.')
                success_count += 1
                
                #스팸 필터링을 피하기 위해 짧은 지연 추가
                time.sleep(1) 
                
            except smtplib.SMTPException as e:
                print(f'  -> [실패] {name} ({email}) 발송 오류: {e}')
                fail_count += 1
                
        server.quit()  # 서버 연결 종료
        
    except smtplib.SMTPAuthenticationError:
        print('[오류] SMTP 로그인 실패. 이메일 주소나 앱 비밀번호를 확인하세요.')
    except Exception as e:
        print(f'[오류] SMTP 연결 중 오류 발생: {e}')
        
    print(f'[방법 1: 완료] 성공: {success_count}건, 실패: {fail_count}건')


# --- 5. 방법 2: 한 번에 여러 명에게 보내기 (BCC) ---
def send_email_bulk_bcc(recipients):
    """
    한 통의 메일을 모든 수신자에게 '숨은 참조(BCC)'로 보냅니다.
    """
    print('\n[방법 2: 일괄 발송(BCC) 시작]')
    if not recipients:
        print('수신자 명단이 비어있습니다.')
        return

    recipient_emails = [email for name, email in recipients]
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '긴급: 화성 생존자 한송희 박사 (전체 상황 공유)'
        msg['From'] = SENDER_EMAIL
        # 'To' 필드는 발신자 자신 또는 'Undisclosed Recipients' 등으로 설정
        msg['To'] = f'Mission Control <{SENDER_EMAIL}>' 
        
        # BCC 방식은 본문 개인화가 불가능. (모두 동일한 내용을 받음)
        generic_html = get_html_message('모든 관계자분')
        msg.attach(MIMEText(generic_html, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # sendmail의 세 번째 인자로 이메일 주소 리스트를 전달
            server.sendmail(SENDER_EMAIL, recipient_emails, msg.as_string())
            
        print(f'[방법 2: 완료] {len(recipient_emails)}명에게 일괄 발송 성공.')
        
    except smtplib.SMTPAuthenticationError:
        print('[오류] SMTP 로그인 실패. 이메일 주소나 앱 비밀번호를 확인하세요.')
    except Exception as e:
        print(f'[오류] SMTP 연결 중 오류 발생: {e}')

# --- 6. 메인 실행 코드 ---
def main():
    recipient_list = load_recipient_list()
    
    if recipient_list:
        print(f'총 {len(recipient_list)}명의 수신자를 찾았습니다.')
        
        # --- 두 가지 방법 중 하나를 선택하여 실행 ---
        
        # 방법 1 실행 (권장)
        send_emails_individually(recipient_list)
        
        # 방법 2 실행 (참고용)
        # send_email_bulk_bcc(recipient_list)
        
    else:
        print('메일을 발송할 대상이 없습니다. mail_target_list.csv 파일을 확인하세요.')

if __name__ == '__main__':
    main()
