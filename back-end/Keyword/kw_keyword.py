from ckip_transformers import __version__
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
# KeyBert
from keybert import KeyBERT

# Initialize drivers
print("Initializing drivers ... WS")
ws_driver = CkipWordSegmenter(model="bert-base", device=-1)
print("Initializing drivers ... POS")
pos_driver = CkipPosTagger(model="bert-base", device=-1)
print("Initializing drivers ... NER")
ner_driver = CkipNerChunker(model="bert-base", device=-1)
print("Initializing drivers ... all done")
print()

def clean(subtopic, sentence_ws, sentence_pos):
    short_with_pos = []
    short_sentence = []
    if subtopic in ['MLB']:
        stop_pos = set(['Neu','Neqa','Nh','Nep','Nd']) # 詞性不保留
        stop_word = set(['MLB','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word : #and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}")
    elif subtopic in ['中職']:
        stop_pos = set(['Nep', 'Nh', 'Neqa','Ncd','Nd','Neu']) #詞性不保留
        stop_word = set(['中職','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}")
    elif subtopic in ['日職']:
        stop_pos = set(['Neqa','Nf','Neu','Ng','Ncd','Nh','Nep','Nd']) # 詞性不保留
        stop_word = set(['日職','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}")
    elif subtopic in ['韓職']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd']) # 詞性不保留
        stop_word = set(['影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}")
    elif subtopic in ['中信兄弟','味全龍','統一獅','樂天桃猿','富邦悍將','台鋼雄鷹']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd']) # 詞性不保留
        stop_word = set(['中職','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word : #and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}")
    elif subtopic in ['MLB 洋基','MLB 紅襪','MLB 光芒','MLB 金鶯','MLB 藍鳥','MLB 守護者','MLB 白襪','MLB 皇家','MLB 老虎','MLB 雙城','MLB 太空人','MLB 運動家','MLB 水手','MLB 天使','MLB 遊騎兵','MLB 大都會','MLB 勇士','MLB 費城人','MLB 馬林魚','MLB 國民','MLB 釀酒人','MLB 紅雀','MLB 紅人','MLB 小熊','MLB 海盜','MLB 響尾蛇','MLB 道奇','MLB 落磯','MLB 巨人','MLB 教士']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd','Ncd']) # 
        stop_word = set(['MLB','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
            # 只留名詞和動詞
            is_N_or_V = pos.startswith("N") #or pos.startswith("V") 
            # 去掉名詞裡的某些詞性
            is_not_stop_pos = pos not in stop_pos
            # 去掉"中職"這個詞
            is_not_stop_word = ws not in stop_word
            # 只剩一個字的詞也不留
            #is_not_one_charactor = len(ws) != 1
            # 組成串列
            if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                short_with_pos.append(f"{ws}({pos})")
                short_sentence.append(f"{ws}") 
    elif subtopic in ['NBA']:
        stop_pos = set(['Neu','Neqa','Nh','Nep','Nd']) # 詞性不保留
        stop_word = set(['NBA','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['T1']:
        stop_pos = set(['Neu','Neqa','Nh','Nep','Nd']) # 詞性不保留
        stop_word = set(['T1','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['PLG']:
        stop_pos = set(['Neu','Neqa','Nh','Nep','Nd']) # 詞性不保留
        stop_word = set(['PLG','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['金州勇士',"波士頓塞爾蒂克","布魯克林籃網","紐約尼克","費城76人","多倫多暴龍","芝加哥公牛","克里夫蘭騎士",
                      "底特律活塞","印第安那溜馬","密爾瓦基公鹿","亞特蘭大老鷹","夏洛特黃蜂","邁阿密熱火","奧蘭多魔術","華盛頓巫師",
                      "洛杉磯快艇","洛杉磯湖人","鳳凰城太陽","沙加緬度國王","丹佛金塊","明尼蘇達灰狼","奧克拉荷馬雷霆","波特蘭拓荒者",
                      "猶他爵士","達拉斯獨行俠","休士頓火箭","曼斐斯灰熊","紐奧良鵜鶘","聖安東尼奧馬刺",]:
        stop_pos = set(['Nh','Nep','VH','VK','VC']) # 詞性不保留
        stop_word = set(['NBA','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['新北國王','臺北富邦勇士','桃園璞園領航猿','福爾摩沙台新夢想家','高雄17直播鋼鐵人','新竹街口攻城獅']:
        stop_pos = set(['Nh','Nep','VH','VK','VC']) # 詞性不保留
        stop_word = set(['PLG','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['新北中信特攻','臺南台鋼獵鷹','高雄全家海神','台灣啤酒英熊','臺中太陽','桃園永豐雲豹']:
        stop_pos = set(['Nh','Nep','VH','VHC','VC']) # 詞性不保留
        stop_word = set(['T1','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['足球']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd','Ncd']) # 
        stop_word = set(['足球','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") #or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['排球']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd','Ncd']) # 
        stop_word = set(['排球','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") #or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['田徑']:
        stop_pos = set(['Neu','Nf','Nh','Ng','Nes','Nep','Neqa','Nd','Ncd']) # 
        stop_word = set(['田徑','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") #or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")
    elif subtopic in ['氣象']:
        stop_pos = set(['Neu','Nf']) # 
        stop_word = set(['準氣象','氣象','快訊','影','圖']) # 停用詞
        for ws, pos in zip(sentence_ws, sentence_pos):
                # 只留名詞
                is_N_or_V = pos.startswith("N") #or pos.startswith("V")
                # 去掉名詞裡的某些詞性
                is_not_stop_pos = pos not in stop_pos
                # 去掉"中職"這個詞
                is_not_stop_word = ws not in stop_word
                # 只剩一個字的詞也不留
                #is_not_one_charactor = len(ws) != 1
                # 組成串列
                if is_N_or_V and is_not_stop_pos and is_not_stop_word :#and is_not_one_charactor
                    short_with_pos.append(f"{ws}({pos})")
                    short_sentence.append(f"{ws}")                  
    return (" ".join(short_sentence), " ".join(short_with_pos))

# ckip 斷詞
def break_word(subtopic,text):
    ws = ws_driver([text])
    pos = pos_driver(ws)

    ws_list = [] # 用來儲存斷詞結果的list

    for sentence, sentence_ws, sentence_pos in zip(text, ws, pos):
        (short, res) = clean(subtopic, sentence_ws, sentence_pos)  # 清理不需要的字詞
        ws_list.append(short)


    return ws_list # 回傳斷詞後的list, 不會有空行的問題 

# 抓關鍵字
def kw_get_keyword(subtopic, title):
    ws_list=break_word(subtopic,title)

    kw_model = KeyBERT()
    keywords = []
    for doc in ws_list:
        keywords_score = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1,1), use_mmr=True, diversity=0.2, top_n=3)
        doc_keywords = [keyword for keyword, score in keywords_score]
        keywords.append(" ".join(doc_keywords))

    return keywords

