import requests
from bs4 import BeautifulSoup

def get_kbs_headlines():
    """
    KBS 뉴스 웹사이트에서 주요 헤드라인을 크롤링하여 반환합니다.

    Returns:
        list: 뉴스 헤드라인 제목을 담은 리스트.
    """
    url = 'http://news.kbs.co.kr'
    headers = {'User-Agent': 'Mozilla/5.0'}  # User-Agent 설정으로 접근 차단 방지

    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # KBS 뉴스 페이지의 헤드라인 HTML 구조를 분석하여 찾아낸 셀렉터
        headlines = soup.select('ul.headline_list li div.title_area a span.text')
        
        # 헤드라인 제목을 저장할 리스트 생성
        headline_list = []
        for headline in headlines:
            headline_list.append(headline.get_text(strip = True))
            
        return headline_list

    except requests.exceptions.RequestException as e:
        print(f"웹사이트 접속 오류가 발생했습니다: {e}")
        return []

def main():
    """
    메인 함수: KBS 헤드라인을 가져와서 화면에 출력합니다.
    """
    print("--- KBS 주요 헤드라인 뉴스 ---")
    headlines = get_kbs_headlines()
    
    if headlines:
        for i, title in enumerate(headlines, 1):
            print(f"{i}. {title}")
    else:
        print("헤드라인 정보를 가져오지 못했습니다.")

if __name__ == '__main__':
    main()
