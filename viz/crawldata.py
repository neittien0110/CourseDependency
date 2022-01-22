from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
class Crawl():
    def crawldata():
        #Them 1 so option cho trinh duyet gia lap
        chrome_option=Options()
        chrome_option.add_argument("--incognito") #An danh
        chrome_option.add_argument("--headless") #khong hien thi UI

        #Khai bao bien browser
        browser = webdriver.Chrome(chrome_options=chrome_option,executable_path="chromedriver.exe")

        #Mo trang web
        browser.get("http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx")
        sleep(2)
        # Dang nhap (ko can thiet)
        # userName="20183694"
        # passWord="**************"
        # browser.find_element(By.ID, "cLogIn1_tb_cLogIn_User_I").send_keys(userName)
        # browser.find_element(By.ID, "cLogIn1_tb_cLogIn_Pass_I").send_keys(passWord)
        # browser.find_element(By.ID, "cLogIn1_bt_cLogIn_CD").send_keys(Keys.ENTER)

        #Lay du lieu
        dataid=[]
        datacrawl=[]
        dataextendcrawl=[]
        for i in range(10):
            courses =browser.find_elements(By.XPATH, '//*[starts-with(@id,"MainContent_gvCoursesGrid_DXDataRow")]') # lay duong dan cua cac du lieu
            for course in courses:
                data=course.find_elements(By.CLASS_NAME,'dxgv')
                dataid.append(course.get_attribute("id")[35:])
                datacourse={'id': course.get_attribute("id")[35:],
                            'Mã học phần':  data[1].text,
                            'Tên học phần': data[2].text,
                            'Thời lượng':   data[3].text,
                            'Số tín chỉ':   data[4].text,
                            'TC học phí':   data[5].text,
                            'Trọng số':     data[6].text
                            }
                datacrawl.append(datacourse)
        #Lay du lieu mo rong
            for j in range(len(dataid)):
                showrow = browser.find_elements(By.XPATH,'//*[starts-with(@id,"MainContent_gvCoursesGrid_DXDataRow")]/td/img')  # nut show phan mo rong
                showrow[j].click()
                sleep(0.1)
                try:
                    extenddata = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH, '//*[starts-with(@id,"MainContent_gvCoursesGrid_tcdxdt'+dataid[j]+'")]')))
                except:
                    sleep(1)
                    extenddata = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.XPATH, '//*[starts-with(@id,"MainContent_gvCoursesGrid_tcdxdt'+dataid[j]+'")]')))

                # extenddata = browser.find_element(By.XPATH, '//*[starts-with(@id,"MainContent_gvCoursesGrid_tcdxdt'+dataid[j]+'")]')
                ex=extenddata.find_elements(By.CSS_SELECTOR, 'b')
                print(ex[1].text)
                extendcourse={'id': extenddata.get_attribute("id")[32:],
                              'Học phần điều kiện': ex[0].text,
                              'Tên tiếng anh': ex[1].text,
                              'Tên viết tắt': ex[2].text,
                              'Viện Quản lý': ex[3].text
                              }
                dataextendcrawl.append(extendcourse)
        #Sang trang
            print("done page"+str(i+1))
            dataid.clear()
            nextpage = browser.find_element(By.XPATH, '//img[@alt="Next"]')  # nut chuyen trang
            nextpage.click()  # Trang ke tiep
            sleep(1.5)#Dung de load du lieu

        #Ghi du lieu
        print(datacrawl)
        df= pd.DataFrame(datacrawl)
        df.to_csv('CourseListdata1.csv')
        df=pd.DataFrame(dataextendcrawl)
        df.to_csv('CourseListdataextend1.csv')

        #dong trinh duyet
        sleep(3)
        browser.close()
# Crawl.crawldata()