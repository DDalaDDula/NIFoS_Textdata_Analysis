import os
from module.func import basic_crawling
# 크롤링 함수 정의
def run_crawler(start_year, finish_year, query_text):  # 시작년도 ~ 최종년도(앞 두 숫자를 빼고 넣음 [ex-2018 ▶ 18]), 검색할 Text
    # 디렉토리 생성 함수
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)
    # 연도,월별 디렉토리를 생성할 경로 설정
    dataset_directory = os.path.join("./", "crawling_dataset") # 크롤링된 데이터를 저장하는 디렉토리 생성
    create_directory(dataset_directory)
    
    for Yr in range(start_year,finish_year+1):
        # crawling_dataset 디렉토리에 연도 디렉토리 생성
        year_directory = os.path.join(dataset_directory, f"20{Yr}")
        create_directory(year_directory)
        M1, M2 = 1, 12
        for Mth in range(M1,M2+1): # M1부터 M2까지 차례대로 반복
            month_directory = os.path.join(year_directory, f"{Mth}월")
            create_directory(month_directory)
            if Mth in [1,3,5,7,8,10,12]:
                crawl_df = basic_crawling(Yr,Mth,31, query_text)
            elif Mth in [4,6,9,11]:
                crawl_df = basic_crawling(Yr,Mth,30, query_text)
            elif Mth == 2 and Yr%4 == 0: # 윤년을 고려하여 2월 29일인 케이스 추가
                crawl_df = basic_crawling(Yr,Mth,29, query_text)
            elif Mth == 2 and Yr%4 != 0: # 윤년이 아닌 2월일 경우
                crawl_df = basic_crawling(Yr,Mth,28, query_text) 

            # 네이버블로그만 남기기 위해 재검사.
            link_list = crawl_df['url'].to_list()
            find_naver = [i for i in range(len(link_list)) if 'blog.naver.com' in link_list[i]] 

            NB_DF = crawl_df.iloc[find_naver]
            NB_DF.to_csv("./crawling_dataset/%s/%s월/%s_%s_%s월.csv"%("20"+str(Yr),Mth,query_text.strip(""""'"""),"20"+str(Yr),Mth), index=False, encoding='UTF-8')