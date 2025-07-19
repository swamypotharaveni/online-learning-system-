# # valu=[1,2,3,4,5]
# # result= [i**2 if i %2 ==0 else i**3 for i in valu]
# # print(result)

# # set1={1,23,34,6,78}

# # set1={1,23,34,6,78}


# # input=[[1,2,3,4],5,[6],(7,9),9,0]
# # value=[]
# # for i in input:
# #     if isinstance(i,list):
# #         value.extend(i)
# #     elif isinstance(i,tuple):
# #         value.extend(i)
# #     else:
# #         value.append(i)
# # print(value)

# import requests
# from bs4 import BeautifulSoup
# # basu_url='https://www.amazon.jobs/en/search.json?offset=0&result_limit=100&sort=relevant&country=&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&region=&county=&query_options='
# # res=requests.get(basu_url)
# # jobs=res.json()
# # print(jobs['jobs'])
# base_url='https://jobs.aldi-hofer.com/search?q=&sortColumn=referencedate&sortDirection=desc&startrow=0'
# res=requests.get(base_url)
# soup=BeautifulSoup(res.text,'html.parser')
# all_data=soup.find_all("tr",class_="data-row")
# for i in all_data:
#     title=i.find("span").text
#     print(title)
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
option=Options()
open.a