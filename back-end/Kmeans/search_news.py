from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient
from DB.mongodb import get_subject_col_data

from Kmeans.kmeans import calculate_tfidf, convert_to_dataframe, hot_run_kmeans_from_df, newest_run_kmeans_from_df

total_subject = ['健康', '國際', '娛樂', '生活', '社會地方', '科技', '財經', '運動']
client = MongoClient("mongodb+srv://user1:user1@cluster0.ronm576.mongodb.net/TodayNews?retryWrites=true&w=majority")
db_daily = client['關鍵每一天']
db=client['News']

def newest_news_serch(combined_data):
    df = pd.DataFrame(combined_data)
    print(len(df))
    news_list= newest_run_kmeans_from_df(df,len(df)//5)
    # 按照timestamp字段排序
    sorted_data = sorted(news_list, key=lambda x: x['timestamp'], reverse=True)
    return sorted_data

def hot_all_search_news(option):
    all_keywords = get_subject_col_data("綜合全部", option)
    selected_news = {}  # 存儲最相似的新聞

    current_datetime = datetime.now()

    if option == 'daily':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=30)
    print("新聞找:大於等於",start_datetime,"小於",end_datetime)
    for keyword in all_keywords:
        
        # 進行聚合查詢，使用一個關鍵字來查詢新聞
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'},
                    'timestamp': {"$gte": start_datetime, "$lt": end_datetime}
                }
            },
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]

        # 建立一個空的列表來保存查詢結果
        keyword_news_data = []

        for collection_name in total_subject:
                news_data = list(db[collection_name].aggregate(pipeline))
                keyword_news_data.extend(news_data)  # 把查詢結果加入列表
                
        # 提取新聞標題和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 計算TF-IDF相似性分數
        similarity_scores = calculate_tfidf(news_text, keyword)

        
        # 把相似性分數加回每個新聞的資料中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        
        result = hot_run_kmeans_from_df(df_keyword_news_data,int(len(df_keyword_news_data)/2))
        # 按照相似度和時間戳排序
        
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)

          
        if keyword_news_data:
            selected_news[keyword] = [news for news in result]
    return selected_news,start_datetime,end_datetime

def hot_topic_search_news(collection_name, option):
    all_keywords = get_subject_col_data(collection_name, option)
    selected_news = {}  # 存储最相似的新闻

    current_datetime = datetime.now()

    if option == 'daily':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=1)
    elif option == 'weekly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=7)
    elif option == 'monthly':
        end_datetime = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = end_datetime - timedelta(days=30)
    print("新聞找:大於等於", start_datetime, "小於", end_datetime)
    
    for keyword in all_keywords:
        pipeline = [
            {
                '$match': {
                    'title': {'$regex': f'.*{keyword}.*', '$options': 'i'},
                    'timestamp': {"$gte": start_datetime, "$lt": end_datetime}
                }
            },
            {
                '$project': {
                    'document': '$$ROOT',  # 將整個文檔添加到document欄位中
                    'combined_text': {'$concat': ['$title', ' ', '$summary']},  # 新增combined_text字段
                    'timestamp': '$timestamp'  # 保存時間戳
                }
            },
            {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
        ]
        news_data = list(db[collection_name].aggregate(pipeline))
        print("原本:")
        print(len(news_data))
        if len(news_data) < 20:
            print("不夠")
            pipeline = [
        {
            '$match': {
                '$or': [
                    {'title': {'$regex': f'.*{keyword}.*', '$options': 'i'}},
                    {'summary': {'$regex': f'.*{keyword}.*', '$options': 'i'}}
                ],
                'timestamp': {"$gte": start_datetime, "$lt": end_datetime}
            }
        },
        {
            '$project': {
                'document': '$$ROOT',
                'combined_text': {'$concat': ['$title', ' ', '$summary']},
                'timestamp': '$timestamp'
            }
        },
        {
                '$match': {
                    'combined_text': {'$exists': True}
                }
            }
    ]
            news_data = list(db[collection_name].aggregate(pipeline))
            print("後來:")
            print(len(news_data))
        # 建立一个空的列表来保存查询结果
        keyword_news_data = []
        keyword_news_data.extend(news_data)  # 把查询结果加入列表

       

        # 提取新闻标题和摘要文本
        news_text = [news['combined_text'] for news in keyword_news_data]

        # 计算TF-IDF相似性分数
        similarity_scores = calculate_tfidf(news_text, keyword)

        # 把相似性分数加回每个新闻的数据中
        for i, news in enumerate(keyword_news_data):
            news['document']['similarity'] = similarity_scores[i]

        df_keyword_news_data = convert_to_dataframe(keyword_news_data)
        if int(len(df_keyword_news_data) / 2) == 0 :
            result = hot_run_kmeans_from_df(df_keyword_news_data, 1)
        else:
            result = hot_run_kmeans_from_df(df_keyword_news_data, int(len(df_keyword_news_data) / 2))

        # 按照相似度和时间戳排序
        result.sort(key=lambda x: (x['similarity'], x['timestamp']), reverse=True)
        if keyword_news_data:
            selected_news[keyword] = [news for news in result]

    return selected_news,start_datetime,end_datetime