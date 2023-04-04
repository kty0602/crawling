# KB차차차 국산 분류
urlList = ['&sort=-orderDate&gas=004001','&sort=-orderDate&gas=004002','&sort=-orderDate&gas=004003','&sort=-orderDate&gas=004007']
urlList2 = ['&useCode=002001','&useCode=002002','&useCode=002003','&useCode=002004','&useCode=002005','&useCode=002006','&useCode=002007','&useCode=002008','&useCode=002009']
url = 'https://www.kbchachacha.com/public/search/main.kbc#!?countryOrder=1&page='


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

options = Options()
options.add_experimental_option("detach", True) # 브라우저 바로 닫힘 방지
options.add_experimental_option("excludeSwitches", ['enable-loging'])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
driver.implicitly_wait(5)
driver.maximize_window()  #창 최대화

# 1. 페이지 이동
driver.get(url)
driver.execute_script("window.scrollTo(0, 700)")
plattform = 'KB차차차'
tag = '국산'
# # 2. 파일 생성
f = open(r"C:\Users\User\Desktop\vscode(python)\kb차차차(국산)_data.csv", 'w', encoding ='utf-8-sig', newline='')
csvWriter = csv.writer(f)        
items_to_select2 = ['가솔린', '디젤', 'LPG', '전기']
items_to_select3 = ['경차','소형차','준중형차','중형차','대형차','스포츠카','RV','SUV','승합차']
for i in range(4):      
    for z in range(9):
        time.sleep(1)
        for idx in range(1, 41):
        # 3. 데이터 추출
            driver.get(url+str(idx)+urlList[i]+urlList2[z])
            time.sleep(1)
            items = driver.find_elements(By.CLASS_NAME, 'area')
            for item in items:
                try:
                    name = item.find_element(By.CLASS_NAME, 'tit').text             # 차 이름
                    if '실차주 ' in name:
                        name = name.strip('실차주 ')
                    if '직거래' in name:
                        name = name.strip('직거래')
                    brand = name.split()                                            # 브랜드 풀 이름에서 분류
                    price = item.find_element(By.CLASS_NAME, 'pay').text            # 가격
                    if ' ' in price:
                        price, price1 = price.split()
                    price = price.replace(",", "")
                    rprice = price.replace("만원", "0000")                  # 가격 범위 지정값 
                    year = item.find_element(By.CLASS_NAME, 'first').text           # 연식
                    info = item.find_element(By.CLASS_NAME, 'data-in').text         # 정보
                    link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')    # 링크
                    img = item.find_element(By.TAG_NAME, 'img').get_attribute('src')    # 사진
                    year, year1, year2 = year.split()
                    year = year.replace("년", "")
                    km,region = info.split()
                    km = km.replace(",","")
                    rkm = km.replace("km","")
                    oilType = items_to_select2[i]
                    type = items_to_select3[z]
                except:
                    continue
                csvWriter.writerow([plattform, tag, type, brand[0], name, price, rprice, year, km, rkm, oilType, region, link, img])
                time.sleep(1)
        

# 4. 파일 닫기
f.close()
driver.close()
