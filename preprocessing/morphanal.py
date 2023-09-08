import pandas as pd
from tqdm import tqdm
from konlpy.tag import Okt
from collections import Counter # 형태소별 빈도 구할 때 사용

def analyze_corpus(df):
    corpus = df['str'].to_list()
    nouns = []
    verbs = []
    adjs = []
    josas = []  # 불용어 목록에 사용할 조사 리스트.
    morphs = []  # 품사 태깅 없이 형태소만 추출. 이 데이터는 TF-IDF, N-gram 등의 텍스트 분석에 사용될 수 있습니다.
    pos_list = []  # 감성 분석에 필요한 목록.
    
    okt = Okt()  # Okt 객체 초기화
    
    for i in tqdm(range(len(corpus))):
        # 답변에서 형태소/품사 추출
        try:
            a = okt.pos(corpus[i], norm=True, stem=True)  # 단어 정규화와 어간 추출을 실행 (True).
            m = okt.morphs(corpus[i], norm=True, stem=False)
            morphs.append(m)  # 형태소 추가
            pos_list.append(a)  # 형태소/품사 추가
            for x, y in a:
                # 품사가 명사인 경우, 명사 리스트에 단어 추가
                if y == 'Noun':
                    nouns.append(x)
                # 품사가 동사인 경우, 동사 리스트에 단어 추가
                elif y == 'Verb':
                    verbs.append(x)
                # 품사가 형용사인 경우, 형용사 리스트에 단어 추가
                elif y == 'Adjective':
                    adjs.append(x)
                # 품사가 조사인 경우, 조사 리스트에 단어 추가
                elif y == 'Josa':
                    josas.append(x)
        except:
            pass
    
    ''' 명사 df 생성 '''
    noun_cnt = Counter(nouns).most_common()
    noun = []
    noun_count = []
    for a, b in noun_cnt:
        noun.append(a)
        noun_count.append(b)
    # 단어와 빈도를 가지고 판다스 데이터프레임(엑셀 표와 비슷) 생성
    noun_df = pd.DataFrame({'noun':noun, 'noun_count':noun_count})
    
    ''' 동사 df 생성 '''
    verb_cnt = Counter(verbs).most_common()
    verb = []
    verb_count = []
    for a, b in verb_cnt:
        verb.append(a)
        verb_count.append(b)
    # 단어와 빈도를 가지고 판다스 데이터프레임(엑셀 표와 비슷) 생성
    verb_df = pd.DataFrame({'verb':verb, 'verb_count':verb_count})
    
    ''' 형용사 df 생성 '''
    adj_cnt = Counter(adjs).most_common()
    adj = []
    adj_count = []
    for a, b in adj_cnt:
        adj.append(a)
        adj_count.append(b)
    # 단어와 빈도를 가지고 판다스 데이터프레임(엑셀 표와 비슷) 생성
    adj_df = pd.DataFrame({'adj':adj, 'adj_count':adj_count})
    
    ''' 조사 df 생성 '''
    josa_cnt = Counter(josas).most_common()
    josa = []
    josa_count = []
    for a, b in josa_cnt:
        josa.append(a)
        josa_count.append(b)
    # 단어와 빈도를 가지고 판다스 데이터프레임(엑셀 표와 비슷) 생성
    josa_df = pd.DataFrame({'josa':josa, 'josa_count':josa_count})
    df["morphs"] = morphs
    df["pos_tag"] = pos_list
    return noun_df, verb_df, adj_df, josa_df, df
