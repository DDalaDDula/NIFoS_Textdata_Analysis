import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# year=연도(연도에 지정된 숫자! 2018년은 16), month=월(1~12), days=해당 월의 일수
def basic_crawling(year, month, days, query_text):
    # 웹드라이버 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument('lang=ko_KR') # 사용언어 한국어
    chrome_options.add_argument('disable-gpu') # 하드웨어 가속 안함
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('headless') # 창 숨기기
    global driver
    driver = webdriver.Chrome(executable_path ='./crawler/chromedriver_win32/chromedriver.exe',options = chrome_options)
    driver.get("https://www.naver.com/")
    driver.implicitly_wait(10)
    time.sleep(2)

    element = driver.find_element(By.ID, "query");
    element.send_keys(query_text)
    element.submit()
    driver.implicitly_wait(10)
    time.sleep(1)
    day_list = list(range(days,0,-1))
    
    driver.find_element(By.LINK_TEXT, "VIEW").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "블로그").click()
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "옵션").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "#snb > div.api_group_option_sort._search_option_detail_wrap > ul > li.bx.lineup > div > div > a:nth-child(2)").click()
    time.sleep(2)
    
    # 옵션 > 기간 >  직접입력 클릭
    driver.find_element(By.CSS_SELECTOR, "#snb > div.api_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.option > a.txt.txt_option._calendar_select_trigger").click()
    time.sleep(2)

    # 기간 직접입력 시작과 끝의 앞부분 동일 CSS 코드 변수로 담기 (코드 단순화용)
    GS_head_css = "#snb > div.api_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.api_select_option.type_calendar._calendar_select_layer > "
    # 기간 직접입력 년월일 앞 CSS 코드 변수로 담기 (코드 단순화용)
    GSYMD_head_css = "#snb > div.api_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.api_select_option.type_calendar._calendar_select_layer > div.select_wrap._root > "
    
    for day in day_list:
        if day == days:
            print('{}일 작성글 검색 후 수집중 . . .'.format(day))
        #  ★☆★☆ 맨 처음 기간설정 할 때 ☆★☆★
            #### 기간 설정시작 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.set_calendar > span:nth-child(1) > a").click()
            time.sleep(1)
            # 연도는 year
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(1) > div > div > div > ul > li:nth-child({})".format(year-2)).click()
            time.sleep(1)
            # 월은 month
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(2) > div > div > div > ul > li:nth-child({})".format(month)).click()
            time.sleep(1)
            # 일자는 days. 마지막 일자 부터 검색해서 저장할 것이기 때문!
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(3) > div > div > div > ul > li:nth-child({})".format(days)).click()
            time.sleep(1)

            #### 기간 설정끝 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.set_calendar > span:nth-child(3) > a").click()
            time.sleep(1)
            # 연도는 year
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(1) > div > div > div > ul > li:nth-child({})".format(year-2)).click()
            time.sleep(1)
            # 월은 month
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(2) > div > div > div > ul > li:nth-child({})".format(month)).click()
            time.sleep(1)
            # 일자는 days. 마지막 일자 부터 검색해서 저장할 것이기 때문!
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(3) > div > div > div > ul > li:nth-child({})".format(days)).click()
            time.sleep(1)

            #### 기간 설정란 적용 버튼 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.btn_area > button").click()
            time.sleep(1)
            
            # 첫 번째 스크롤&전역변수 선언&제목/링크/날짜 저장
            scroll_first()
            time.sleep(2)

        
        else:
        # 두 번째부터는 스크롤 맨 위로 올려서 일자만 바꾸기!
            print('{}일 작성글 검색 후 수집중 . . .'.format(day))
            # 스크롤 맨 위로 올리기
            driver.execute_script('window.scrollTo(0,0)')
            time.sleep(1)
            # 옵션 > 기간 >  직접입력 클릭
            driver.find_element(By.CSS_SELECTOR, "#snb > div.api_group_option_sort._search_option_detail_wrap > ul > li.bx.term > div > div.option > a.txt.txt_option._calendar_select_trigger").click()
            driver.implicitly_wait(10)
            time.sleep(1)
            # 기간 설정시작 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.set_calendar > span:nth-child(1) > a").click()
            driver.implicitly_wait(10)
            time.sleep(1)
            # # 일자는 day_list에서 for 문 돌면서 i번째 숫자 가져오기
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(3) > div > div > div > ul > li:nth-child({})".format(day)).click()
            driver.implicitly_wait(10)
            time.sleep(1)
            # 기간 설정끝 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.set_calendar > span:nth-child(3) > a").click()
            driver.implicitly_wait(10)
            time.sleep(1)
            # # 일자는 day_list에서 for 문 돌면서 i번째 숫자 가져오기
            driver.find_element(By.CSS_SELECTOR, GSYMD_head_css + "div:nth-child(3) > div > div > div > ul > li:nth-child({})".format(day)).click()
            # 기간 설정란 적용 버튼 클릭
            driver.find_element(By.CSS_SELECTOR, GS_head_css + "div.btn_area > button").click()
            driver.implicitly_wait(10)
            time.sleep(1)
            
            # 두 번째 스크롤&제목/링크/날짜 저장
            scroll_next()
            
    driver.quit()
    global crawl_df
    crawl_df = pd.DataFrame({'url': url_list, 'title':title_list, 'date':date_list})
    crawl_df.drop_duplicates(inplace=True) #중복제거
    crawl_df = crawl_df[::-1] # 역순 크롤링이기 때문에 reverse시킴
    crawl_df = crawl_df.reset_index(drop=True) #인덱스 초기화
    return crawl_df

#셀레니움 스크롤 끝까지 내려도 계속 내리는 페이지라면
def scroll_first():
    prev_height = driver.execute_script("return document. body.scrollHeight")

    while True:
        #첫번째로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #시간대기
        time.sleep(2)
        #현재높이 저장
        current_height = driver.execute_script("return document. body.scrollHeight")
        #현재높이와 끝의 높이가 같으면 탈출
        if(current_height == prev_height):
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")

    # 검색 결과 블로그글 url과 제목 가져오기
    class_articles = ".api_txt_lines.total_tit"
    url_link = driver.find_elements(By.CSS_SELECTOR, class_articles)
    # 글 작성 일자 가져오기
    class_datetime = ".sub_time.sub_txt"
    date_time = driver.find_elements(By.CSS_SELECTOR, class_datetime)
    
    global url_list
    global title_list
    global date_list

    url_list = []
    title_list = []
    date_list = []

    for article in url_link:
        url = article.get_attribute('href')
        url_list.append(url)
    for article in url_link:
        title = article.text
        title_list.append(title)
    for date in date_time:
        datetime = date.text
        date_list.append(datetime)

#셀레니움 스크롤 끝까지 내려도 계속 내리는 페이지라면
def scroll_next():
    prev_height = driver.execute_script("return document. body.scrollHeight")

    while True:
        #첫번째로 스크롤 내리기
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #시간대기
        time.sleep(2)
        #현재높이 저장
        current_height = driver.execute_script("return document. body.scrollHeight")
        #현재높이와 끝의 높이가 끝이면 탈출
        if(current_height == prev_height):
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")

    # 검색 결과 블로그글 url과 제목 가져오기
    class_articles = ".api_txt_lines.total_tit"
    url_link = driver.find_elements(By.CSS_SELECTOR, class_articles)
    # 글 작성 일자 가져오기
    class_datetime = ".sub_time.sub_txt"
    date_time = driver.find_elements(By.CSS_SELECTOR, class_datetime)

    for article in url_link:
        url = article.get_attribute('href')
        url_list.append(url)
    for article in url_link:
        title = article.text
        title_list.append(title)
    for date in date_time:
        datetime = date.text
        date_list.append(datetime)