from numpy import NAN, mod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx'   

#Thư mục chứa kết quả
COURSE_COLLECTION_FOLDER = "../assets"

# Select Webbrowser. 1 =Firefox, 2 = Chrome, 3 = Edge
WebBrowserSelector=3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Crawl():
    def crawldata():
        #Them 1 so option cho trinh duyet gia lap
        chrome_option=Options()
        chrome_option.add_argument("--incognito") #An danh
        chrome_option.add_argument("--headless") #khong hien thi UI


        #Khai bao bien browser điều khiển quá trình crawl
        browser = NAN
        if WebBrowserSelector == 1:
            browser = webdriver.Firefox()   # import browser firefox}    
        elif WebBrowserSelector == 2:   
            browser = webdriver.Chrome(chrome_options=chrome_option, opexecutable_path="./BrowserDrivers/chromedriver.exe")
        elif WebBrowserSelector == 3:   
            browser = webdriver.Edge(executable_path=r'./BrowserDrivers/msedgedriver.exe')   # import browser firefox}    
        
        #Mo trang web
        browser.get(BASE_URL)
        sleep(2)
        # Dang nhap (ko can thiet)
        # userName="20183694"
        # passWord="**************"
        # browser.find_element(By.ID, "cLogIn1_tb_cLogIn_User_I").send_keys(userName)
        # browser.find_element(By.ID, "cLogIn1_tb_cLogIn_Pass_I").send_keys(passWord)
        # browser.find_element(By.ID, "cLogIn1_bt_cLogIn_CD").send_keys(Keys.ENTER)

        
        dataid=[]
        # mảng chứa thông tin về một course
        datacrawl=[]    
        # mảng chứa thông tin các học phần phụ thuộc
        dataextendcrawl=[]
        #Xác định số trang thông tqua thông tin
        PagerBottom= browser.find_element(By.XPATH, '//*[@id="MainContent_gvCoursesGrid_DXPagerBottom"]/b[1]').get_attribute('innerHTML')
        pageCount =  int(PagerBottom[PagerBottom.find("of")+3:PagerBottom.find("(")-1])
        courseCount = int(PagerBottom[PagerBottom.find("(")+1:PagerBottom.find("items")-1])
        print("Có {page} page với {course} học phần".format(page=pageCount, course=courseCount))

        #Chỉ số của page 
        pageIndex = 0;
        #Chỉ số của course
        courseIndex = 0;
        for i in range(pageCount):
            #Vòng lặp lấy du lieu học phần và lưu vào cấu trúc datacrawl
            # Ví dụ MI1010	Giải tích I	3(3-2-0-6)	3	5	0.7
            courses =browser.find_elements(By.XPATH, '//*[starts-with(@id,"MainContent_gvCoursesGrid_DXDataRow")]') # lay duong dan cua cac du lieu
            #Thông báo đang crawl ở page nào
            pageIndex = pageIndex+1
            print("Crawling page {pageIndex}/{pageCount} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(pageIndex=pageIndex, pageCount=pageCount))
            #Số lượng course trong một page
            num_in_page = len(courses)
            index = 0
            for course in courses:
                index = index + 1
                data=course.find_elements(By.CLASS_NAME,'dxgv')
                dataid.append(course.get_attribute("id")[35:])
                datacourse={'STT': courseIndex,
                            'Mã học phần':  data[1].text,
                            'Tên học phần': data[2].text,
                            'Thời lượng':   data[3].text,
                            'Số tín chỉ':   data[4].text,
                            'TC học phí':   data[5].text,
                            'Trọng số':     data[6].text
                            }
                print("---- " + str(index) + "/" + str(num_in_page) +": " + data[2].text)
                datacrawl.append(datacourse)
            # Kết thúc vòng lặp lấy dữ liệu học phần
            
            #Vòng lặp lấy du lieu mở rộng và lưu vào cấu trúc dataextendcrawl
            #Ví dụ: 	Học phần điều kiện:
            #           Tên tiếng anh: Calculus I
            #           Tên viết tắt: Giải tích I
            #           Viện quản lý: KTTD
            index = 0
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
                extendcourse={'id': extenddata.get_attribute("id")[32:],
                              'Học phần điều kiện': ex[0].text,
                              'Tên tiếng anh': ex[1].text,
                              'Tên viết tắt': ex[2].text,
                              'Viện Quản lý': ex[3].text
                              }
                datacrawl[courseIndex]['Học phần điều kiện'] =  ex[0].text
                datacrawl[courseIndex]['Tên tiếng anh'] =  ex[1].text
                datacrawl[courseIndex]['Tên viết tắt'] =  ex[2].text
                datacrawl[courseIndex]['Viện Quản lý'] =  ex[3].text
                index = index + 1
                courseIndex = courseIndex + 1
                print("---- {index}/{num_in_page}  {courseIndex}/{courseCount}: {name}".format(index=index, num_in_page=num_in_page, courseIndex=courseIndex, courseCount=courseCount, name=ex[1].text))
            #Kết thúc vòng lặp lấy du lieu mở rộng và lưu vào cấu trúc dataextendcrawl
            
            #Sang trang mới
            print("done page " + str(pageIndex) + "/" + str(pageCount))
            dataid.clear()
            nextpage = browser.find_element(By.XPATH, '//img[@alt="Next"]')  # nut chuyen trang
            nextpage.click()  # Trang ke tiep
            sleep(1)#Dung de load du lieu
 
            if pageIndex % 5 == 0: 
                df= pd.DataFrame(datacrawl)
                df.to_csv(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv')
            
        #Ghi du lieu
        #print(datacrawl)
        df= pd.DataFrame(datacrawl)
        df.to_csv(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv')
        #dong trinh duyet
        sleep(1)
        browser.close()

Crawl.crawldata()