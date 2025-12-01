import time
import random
import pyperclip # pyperclip 모듈 추가
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# PEP 8 가이드에 따라 함수 및 변수명은 소문자와 언더스코어(_)를 사용합니다.
# 클래스명은 CapWords 방식을 사용합니다.

class NaverCrawler:
    """
    네이버 사이트에 로그인하여 지정된 콘텐츠를 크롤링하는 클래스.
    """
    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
        self.driver = self._set_up_driver()

    def _set_up_driver(self):
        """
        웹드라이버를 설정하고 반환합니다.
        """
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        return driver

    def login_to_naver(self):
        """
        네이버에 로그인합니다.
        """
        print('네이버 로그인 페이지로 이동합니다.')
        self.driver.get('https://nid.naver.com/nidlogin.login')
        time.sleep(2)  # 페이지 로딩 대기

        try:
            # ActionChains를 사용하여 마우스 및 키보드 동작을 조합합니다.
            actions = ActionChains(self.driver)
            
            # 아이디 입력 필드를 찾아서 아이디를 입력합니다.
            id_input = self.driver.find_element(By.ID, 'id')
            
            # 마우스 커서를 아이디 입력 필드로 이동합니다.
            actions.move_to_element(id_input).perform()
            time.sleep(random.uniform(0.5, 1.5))
            
            # pyperclip으로 아이디를 복사하고 붙여넣습니다.
            pyperclip.copy(self.user_id)
            id_input.click()
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(random.uniform(0.5, 1.0))

            # 비밀번호 입력 필드로 Tab 키를 눌러 이동합니다.
            actions.send_keys(Keys.TAB).perform()
            time.sleep(random.uniform(0.5, 1.0))

            # 비밀번호 입력 필드를 찾습니다.
            pw_input = self.driver.find_element(By.ID, 'pw')
            
            # pyperclip으로 비밀번호를 복사하고 붙여넣습니다.
            pyperclip.copy(self.user_pw)
            actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            time.sleep(random.uniform(0.5, 1.0))
            
            # 로그인 버튼을 클릭합니다.
            pw_input.send_keys(Keys.RETURN)
            
            # 로그인 완료 후 페이지 이동 대기
            time.sleep(5)
            
            if '네이버' in self.driver.title:
                print('로그인에 성공했습니다.')
            else:
                print('로그인에 실패했거나 예기치 않은 오류가 발생했습니다.')

        except NoSuchElementException as e:
            print(f"로그인 중 오류 발생: {e}")
            self.driver.quit()
            return False
            
        return True

    def get_login_content(self):
        """
        로그인 후 보이는 콘텐츠를 크롤링합니다.
        """
        content_list = []
        try:
            print('로그인 후 콘텐츠를 확인합니다.')
            self.driver.get('https://www.naver.com')
            time.sleep(3)
            
            mail_titles = self.driver.find_elements(By.CSS_SELECTOR, '.mail_title')
            
            if mail_titles:
                for title in mail_titles:
                    content_list.append(title.text)
            else:
                print('로그인 후 보이는 메일 제목을 찾을 수 없습니다.')
                
        except NoSuchElementException as e:
            print(f"콘텐츠 크롤링 중 오류 발생: {e}")
        
        return content_list

    def close_driver(self):
        """
        웹드라이버를 종료합니다.
        """
        self.driver.quit()
        print('웹드라이버를 종료합니다.')

def main():
    """
    메인 실행 함수.
    """
    naver_id = '실제 아이디 입력'
    naver_pw = '실제 비밀번호 입력'

    crawler = NaverCrawler(naver_id, naver_pw)
    
    if crawler.login_to_naver():
        login_content = crawler.get_login_content()

        print('\n--- 로그인 후 가져온 콘텐츠 ---')
        if login_content:
            for content in login_content:
                print(f"  - {content}")
        else:
            print('가져온 콘텐츠가 없습니다.')
    
    crawler.close_driver()

if __name__ == '__main__':
    main()
