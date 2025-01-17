#注意事項 第一次執行時請幫我先執行
#create_table
#read_ptt_link_search_data_from_excel()
#read_ptt_subtopic_id_data_from_excel()
#這兩個funtion(在程式最下面三行) 以便建立基本資料 執行完確定資料庫有資料就幫我command掉
#接著只要執行update_ptt_data() 就可以進行ptt的爬蟲了
 
import requests 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import os
import time
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import datetime
import mysql.connector
#import emotion 

current_dir = os.getcwd()
driver_name = "chromedriver.exe"
driver_path = current_dir+"\\"+driver_name

host = '127.0.0.1'
user = 'root'
password = '109403502'
database = 'communews'
charset =  "utf8"


#這一邊要改成輸出到資料庫 需要輸出到 存放ptt內容的資料庫
def transfer_dictionary(sub_topics,titles,links,dates,page_indexes,emotion_scores):
   
    data_list = []
    for sub_topic,title,link,date,page_index in zip(sub_topics,titles,links,dates,page_indexes):
        data_list.append({'subtopic':sub_topic,'title':title,'link':link,'date':date,'page':int(page_index)},)
    print(data_list)
    return data_list

#將ptt網址的字串進行處理
def split_ptt_link(URL,already_get_index):
    split_url = URL.split("index")
    base_url = split_url[0]
    page_index = split_url[1].rstrip(".html")

    print("Base URL:", base_url)  
    print("Page Number:", page_index)  

    if int(page_index)>already_get_index:
        return True,page_index
    else:
        return False,page_index


def renew_ptt_subtopic_table_to_database(ptt_renewed_link_list):
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)
    cursor = connection.cursor()
    for ptt_renewed_link in ptt_renewed_link_list:

        # SQL更新语句
        update_query = "UPDATE tb_ptt_search_link SET page = %s WHERE id_ptt_link = %s"

        # 执行更新
        data = (ptt_renewed_link['id_ptt_link'], ptt_renewed_link['page'])
        cursor.execute(update_query, data)

        # 提交更改
        connection.commit()

    # 关闭连接
    connection.close()


def transfer_date_type(date_str):
    month, day = map(int, date_str.split('/'))
    current_datetime = datetime.datetime.now()

    # 从当前日期和时间中提取年份信息
    current_year = current_datetime.year
    # 使用指定的年份与月份、日期组合成新的日期
    new_date = datetime.date(current_year, month, day)

    # 将新的日期转换为字符串，格式为'YYYY-MM-DD'
    new_date_str = new_date.strftime('%Y-%m-%d')

    return new_date_str

def renew_ptt_subtopic_table_index(id_ptt_link,id_subtopic,subtopic,URL,page_index):
    dic = {'id_ptt_link':id_ptt_link,'id_subtopic':id_subtopic,'subtopic':subtopic,'ptt_url':URL,'page':page_index}
    return dic

def is_gossiping(id_subtopic):
    if id_subtopic==30:
        return True
    return False



def grab_ptt_article_everyday(df_ptt_subtopic):
    sub_topics=[]
    titles=[]
    links=[]
    dates=[]
    page_indexes=[]
    emotion_scores=[]

    new_list_ptt_subtopic = []
    
    options = webdriver.ChromeOptions()  
    prefs = {'profile.default_content_setting_values':{'notifications': 2}}
    options.add_experimental_option('prefs', prefs)
    options.add_argument("disable-infobars")
    driver = webdriver.Chrome(executable_path=driver_path,chrome_options=options)

    for id_ptt_link, id_subtopic, subtopic, URL, already_get_index in zip (df_ptt_subtopic['id_ptt_link'],df_ptt_subtopic['id_subtopic'],df_ptt_subtopic['subtopic'],df_ptt_subtopic['ptt_url'],df_ptt_subtopic['page']):
        count=1
        driver.get(URL)
        time.sleep(2)
        is_search_next_page = True
        while(is_search_next_page==True):
            if count==1 and is_gossiping(id_subtopic) :
                time.sleep(1)
                elem_yes = (driver.find_element(By.XPATH, '//html/body/div[2]/form/div[1]/button'))
                time.sleep(1)
                ActionChains(driver).click(elem_yes).perform()
                time.sleep(1)

            elem_last_page =  driver.find_element(By.XPATH, '//*[@id="action-bar-container"]/div/div[2]/a[2]')
            time.sleep(1)
            ActionChains(driver).click(elem_last_page).perform()
            time.sleep(3)
            current_url =driver.current_url
            is_search_next_page,page_index = split_ptt_link(current_url,already_get_index)
            elem_titles = driver.find_elements(By.CSS_SELECTOR, '#main-container > div> div> div.title >a')
            elem_dates = driver.find_elements(By.CSS_SELECTOR, '#main-container > div > div> div> div.date')
            elem_links = driver.find_elements(By.CSS_SELECTOR, '#main-container > div> div> div.title > a')
            if(count==1):
                new_list_ptt_subtopic.append(renew_ptt_subtopic_table_index(id_ptt_link,id_subtopic,subtopic,URL,page_index))
                count+=1
            print("這是關於"+subtopic+"的新聞：")
            if(is_search_next_page==True):
                for title,date,link in zip (elem_titles,elem_dates,elem_links):
                    sub_topics.append(subtopic)
                    titles.append(title.text)
                    links.append(link.get_attribute('href'))
                    transfer_date = transfer_date_type(date.text)
                    dates.append(transfer_date)
                    page_indexes.append(page_index)
                    print("標題是"+title.text)
                    

    datalist = transfer_dictionary(sub_topics,titles,links,dates,page_indexes,emotion_scores)
    #將更新到的頁數傳回置資

    return datalist,new_list_ptt_subtopic

def read_ptt_data():
    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

    cursor = connection.cursor()

    # SQL查询语句
    select_query = "SELECT * FROM tb_ptt_search_link"

    # 执行查询
    
    cursor.execute(select_query)

    # 获取所有结果
    result = cursor.fetchall()

    # 将结果转换为DataFrame
    ptt_link_df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

    print("我從資料庫把ptt_link的資訊抓出來了")

    # 打印DataFrame
    print(ptt_link_df)

    # 关闭连接
    connection.close()

    return ptt_link_df
    

def update_ptt_data():
    ptt_link_df = read_ptt_data()

    connection = mysql.connector.connect(host=host, user=user, password=password, database=database, charset=charset)

    cursor = connection.cursor()

    messages,new_list_ptt_subtopic = grab_ptt_article_everyday(ptt_link_df)
    
    for message in messages:
        insert_query = '''
            INSERT INTO tb_ptt_data (subtopic, title, link, date, page)
            VALUES (%s, %s, %s, %s, %s)
        '''
        data = (message['subtopic'], message['title'], message['link'], message['date'], message['page'])

        cursor.execute(insert_query, data)

    connection.commit()

    connection.close()

    renew_ptt_subtopic_table_to_database(new_list_ptt_subtopic)




#爬取ptt資料
update_ptt_data()
    
    


    






