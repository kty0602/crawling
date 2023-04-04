from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
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

# 1 페이지 이동
url = 'https://www.kcar.com/bc/search?gclid=EAIaIQobChMIpIvNm_fO_QIVWXRgCh2p3wbyEAAYASAAEgICGvD_BwE'
driver.get(url)
plattform = 'K-Car'
type = 'RV'
                                                
# 2. 조회 항목 설정 [직영차] 정보만 보여주기

radios3 = driver.find_elements(By.CLASS_NAME, 'el-checkbox__label')
items_to_select3 = ['RV']       

for radio3 in radios3:
    parent3 = radio3.find_element(By.XPATH, '..')
    label = parent3.find_element(By.CLASS_NAME, 'el-checkbox__label')
    if label.text in items_to_select3:
        radio3.click()

driver.execute_script("window.scrollTo(0, 500)")
        
radios1 = driver.find_elements(By.CLASS_NAME, 'el-radio__label')
items_to_select1 = ['직영차']

for radio1 in radios1:
    parent1 = radio1.find_element(By.XPATH, '..') # 부모 element찾기
    label = parent1.find_element(By.CLASS_NAME, 'el-radio__label')
    # print(label.text) # 이름 확인
    if label.text in items_to_select1:
        radio1.click()

radios2 = driver.find_elements(By.CLASS_NAME, 'el-checkbox__label')
items_to_select2 = ['현대', '제네시스', '기아', '쉐보레(GM대우)', '르노코리아(삼성)', '쌍용']

for radio2 in radios2:
    parent2 = radio2.find_element(By.XPATH, '..')
    label = parent2.find_element(By.CLASS_NAME, 'el-checkbox__label')
    if label.text in items_to_select2:
        radio2.click()
time.sleep(1)        

# 3. csv파일 생성
f = open(r"C:\Users\User\Desktop\vscode(python)\kcar_data(직영차_국산_RV).csv", 'w', encoding ='utf-8-sig', newline='')
csvWriter = csv.writer(f)
link = ""
tag = "국산"
button = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[2]/div[4]/div[1]/div[7]/div/ul/li[12]/button')
a = 20
for idx in range(1, 16):                    #몇 페이지까지 뽑아낼 것인가?
# 4. 데이터 추출

    items = driver.find_elements(By.CLASS_NAME, 'detailInfo')

    for item in items:
        fullname = item.find_element(By.ID, 'mkt_clickCarNm').text    # 풀 이름
        brand = fullname.split()
        price = item.find_element(By.CLASS_NAME, 'carExp').text       # 가격
        if '리스' in price:                                           # 가격text값에 리스라는 단어가 있으면 그 데이터 제외 다음 데이터 추출
            continue 
        else:
            if ' ' in price:                                               # 전 할인가 금액 제거
                price, price1 = price.split()
            if ',' in price:    
                price = price.replace(",", "")                             # 문자열에서 , 제거  1,922만원
            if '(삼성)' in brand[0]:
                brand[0] = brand[0].replace("(삼성)","")
            elif '(GM대우)' in brand[0]:
                brand[0] = brand[0].replace("(GM대우)","") 
            rprice = price.replace("만원", "0000")                  # 가격 범위 지정값
            info = item.find_element(By.CLASS_NAME, 'detailCarCon').text    # 연식, 주행거리, 연료, 판매지역
            year, km, oilType, region = info.split('\n')
            year, year1 = year.split()
            year, year1_1 =year.split('년')
            data = ['20', year]
            ryear = "".join(data)
            km = km.replace(",", "")
            rkm = km.replace("km","")  
            img = item.find_element(By.XPATH, '//*[@id="mkt_clickCar"]/img').get_attribute('src')   # 이미지 링크
            csvWriter.writerow([plattform, tag, type, brand[0], fullname, price, rprice, ryear, km, rkm, oilType, region, link, img])                                   
    button.send_keys(Keys.ENTER)
    time.sleep(1.5)
    
        
# 5. 파일 닫기
f.close()  
driver.close()