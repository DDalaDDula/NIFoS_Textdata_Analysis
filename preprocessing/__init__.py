import re
import time
import pandas as pd
from tqdm import tqdm #for문 진행률
from kiwipiepy import Kiwi #문장 분리2
from soynlp.normalizer import * #반복되는 자음 제거

''' 불용어 제거 '''
def contents_clean(text): # 텍스트에는 contents나 corpus가 들어가야 함.
    text = re.sub('\n', ' ', string=str(text)) # 줄바꿈을 띄어쓰기 하나로
    text = re.compile('[^|ㄱ-ㅎ|ㅏ-ㅣ|A-Z|a-z|0-9|가-힣]+').sub(' ',text)
    text = repeat_normalize(text, num_repeats=1) # ↑ ㅋㅋㅋ, ㅎㅎㅎ 등의 의미 없는 자음 삭제. 반복 글자 중 1개만 남김(num_repeats)
    text = re.sub(r"^\s+|\s+$", "", text) # 문서 앞뒤 공백 제거
    text = text.split() # 문서 내 공백(1개 이상) 기준으로 자르기
    text = ' '.join(text) # 공백 기준으로 나뉜 문서를 다시 1개의 공백을 두고 붙임.(↑ 문서 내 다중 공백을 지우기 위함.)
    return text

''' 문장 분리 '''
def contents_separation(text): # 텍스트에는 contents나 corpus가 들어가야 함.
    kiwi = Kiwi() #kss보다 속도 빠름 
    split_list = kiwi.split_into_sents(text)
    return split_list

''' 문장 분리해서 데이터프레임으로 변환 '''
def distribution(idx, text_list):
    str_dic = {'str': [], 'idx': [idx]*len(text_list)}
    for sent in text_list:
        str_dic['str'].append(sent.text)
    df2 = pd.DataFrame(str_dic)
    return df2 # 데이터프레임 형식으로 return