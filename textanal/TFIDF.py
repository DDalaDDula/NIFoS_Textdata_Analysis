import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer # scikit-learn에서 제공하는 TF-IDF 생성 패키지 import

def TF_IDF(df_morph, df_josa, only_kor=False):
    josa_list = df_josa["josa"].tolist() # 조사를 불용어 list로 사용함, list 중 '이다'와 '보다'는 제거.
    josa_list.remove("이다")
    josa_list.remove("보다")
    
    # 형태소 단위로 나뉜 리스트를 한 문장으로 합치고 문장 column 생성
    df_morph['joined_morphs'] = df_morph['morphs'].apply(lambda x: ' '.join(x))
    # 같은 인덱스인(같은 본문인) 문장들을 합치고 본문 column 생성
    df_morph['joined_sentences'] = df_morph.groupby('idx')['joined_morphs'].transform(lambda x: ' '.join(x))
    
    # 원본 인덱스와 문장 column들만 남긴 데이터프레임 생성(중복제거 및 인덱스 초기화)
    df_tf = df_morph[['idx', 'joined_sentences']].drop_duplicates()
    df_tf.reset_index(drop=True, inplace=True)
    
    # 데이터 프레임에서 분석할 문서를 가져와서 쓸 경우 꼭 list 형식으로 변환해서 담아줘야 함.
    corpus = df_tf['joined_sentences'].to_list()
    
    # stop_words에는 위에서 조사만 추출해서 만든 불용어 리스트 사용
    tfidf = TfidfVectorizer(stop_words = josa_list, token_pattern=r'\w{1,}')
    tdm = tfidf.fit_transform(corpus)
    tfidf_array = tdm.toarray()
    # tfidf_array데이터프레임의 컬럼명은 숫자로 되어 있기 때문에, 이를 feature_names로 바꿔줘야 함.
    tfidf_DF = pd.DataFrame(tfidf_array, columns=tfidf.get_feature_names_out())
    
    # only_kor 값에 따라 달라짐. 한글로만 이루어진 TF-IDF로 출력할 것인지에 대한 옵션.
    if only_kor:
        # 데이터프레임에서 한글로만 이루어진 column 필터링을 위한 정규표현식 패턴
        pattern = r'^[ㄱ-ㅎㅏ-ㅣ가-힣\s]+$'
        # 한글로만 이루어진 column으로 된 데이터프레임 생성
        korean_df = tfidf_DF[[column for column in tfidf_DF.columns if re.match(pattern, column)]]
        # 각 단어에 대한 TF-IDF의 합
        word_count = pd.DataFrame({
            '단어': tfidf.get_feature_names_out(),
            'tf-idf': tdm.sum(axis=0).flat
        })
        return word_count, korean_df
    
    else:
        # 각 단어에 대한 TF-IDF의 합
        word_count = pd.DataFrame({
            '단어': tfidf.get_feature_names_out(),
            'tf-idf': tdm.sum(axis=0).flat
        })
        return word_count, tfidf_DF