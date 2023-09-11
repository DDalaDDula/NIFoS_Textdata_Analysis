import pandas as pd
import numpy as np
from tqdm import tqdm

def coocur(df_morph, df_noun):
    docs = df_morph['morphs'].to_list()
    # 중복 단어 제거하여 리스트 생성
    unique_lines = [list(set(line)) for line in tqdm(docs)]
    
    #### 전체 단어쌍 빈도 dict 형식으로 생성
    freq_count = {}   #동시출현 빈도가 저장될 dict
    for words in tqdm(unique_lines):
        # 전체 단어에 대한 동시 출현 빈도
        for i, a in enumerate(words):
            for b in words[i+1:]:
                if a == b: continue
                elif a>b:
                    freq_count[b, a] = freq_count.get((b, a),0) + 1
                else :
                    freq_count[a, b] = freq_count.get((a, b),0) + 1

    #### 딕셔너리를 데이터프레임에 담기
    tt_freq_df=pd.DataFrame.from_dict(freq_count, orient='index')
    #### dict형식을 컬럼명 지정해서 데이터프레임으로 만들기
    list1 = [(tt_freq_df.index[i][0], tt_freq_df.index[i][1], tt_freq_df[0][i]) for i in tqdm(range(len(tt_freq_df)))]
    freq_df2 = pd.DataFrame(list1, columns=["term1","term2","freq"])
    
    # 명사 빈도 상위 50개 추출
    topwords50 = df_noun['noun'].to_list()[:50]
    #### 50위 이내에 속한 단어들로 이루어진 Dataframe을 추출
    list2 =[(freq_df2.loc[i][0], freq_df2.loc[i][1], freq_df2.loc[i][2]) for i in tqdm(range(len(freq_df2))) if (freq_df2['term1'][i] in topwords50) &(freq_df2['term2'][i] in topwords50)]
    freq_df3 = pd.DataFrame(list2, columns=["term1","term2","freq"])
    
    #### 공출현빈도(1-mode matrix) 만들기
    word_co_matx = np.zeros((50,50))
    mat_idx = topwords50 # 단어동시출현행렬이니까 인덱스와 칼럼을 동일하게 지정
    mat_col = topwords50
    word_co_matx = pd.DataFrame(word_co_matx, index=mat_idx, columns=mat_col)
    #### 단어쌍의 첫 번째 단어가 인덱스와 같다 and 두 번째 단어가 칼럼과 같다 → 단어쌍빈도를 해당 셀 값에 삽입
    for n in tqdm(range(len(freq_df3))):
        for idx in mat_idx:
            if idx == freq_df3['term1'][n]:
                for col in mat_col:
                    if col == freq_df3['term2'][n]:
                        word_co_matx.loc[idx, col] = freq_df3['freq'][n]
                        word_co_matx.loc[col, idx] = freq_df3['freq'][n]
    
    return freq_df2, freq_df3, word_co_matx # 원본 dataframe, 상위50단어 dataframe, 공출현빈도(1-mode matrix) 순으로 출력