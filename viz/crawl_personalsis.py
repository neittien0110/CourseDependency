from numpy import NAN, mod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import html2text
import pandas as pd
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'https://ctt-sis.hust.edu.vn/pub/CourseLists.aspx'    #20167995
LOGIN_USERNAME = "20167995"
LOGIN_PASSWORD = "20167995"

#Thư mục chứa kết quả
COURSE_COLLECTION_FOLDER = "../assets"

#Số lượng course trong mỗi trang thông tin.
COURSE_PER_PAGE = 15

# Select Webbrowser. 1 =Firefox, 2 = Chrome, 3 = Edge
WebBrowserSelector=3

#Khai bao bien browser điều khiển quá trình crawl
browser = NAN
browser_actions = NAN

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Crawl():

    def autologin(Username, Password, ExpectedTitle = ""):  
        """_summary_
            Phụ trách nhập thông tin tài khoản đăng nhập
        Args:
            Username (string): tên tài khoản
            Password (string): mật khẩu
            ExpectedTitle (string): một phần trong tiêu đề của trang web sau đăng nhập, nhằm xác định việc đăng nhập là thành công.
        """        
        global browser
        global browser_actions
        
        #Them 1 so option cho trinh duyet gia lap
        chrome_option=Options()
        chrome_option.add_argument("--incognito") #An danh
        # chrome_option.add_argument("--headless") #khong hien thi UI
        chrome_option.add_argument("start-maximized");      # Phóng to để tránh giao diện thay đổi theo kích cỡ màn hình


        if WebBrowserSelector == 1:
            browser = webdriver.Firefox()   # import browser firefox}    
        elif WebBrowserSelector == 2:   
            browser = webdriver.Chrome(chrome_options=chrome_option, executable_path=r"./BrowserDrivers/chromedriver.exe")
        elif WebBrowserSelector == 3:   
            browser = webdriver.Edge(executable_path=r'./BrowserDrivers/msedgedriver.exe')   # import browser firefox}    
        
        #Mo trang web
        browser.get(BASE_URL)
        sleep(2)
        
        browser_actions = ActionChains(browser); 
        
        #---------------------------------------------------
        #---   ĐĂNG NHẬP
        #---------------------------------------------------
        
        # Nhập username
        browser.find_element(By.ID, "ctl00_ctl00_contentPane_MainPanel_MainContent_tbUserName_I").send_keys(Username)
        
        # Nhập mật khẩu. 
        # Lưu ý: phải dùng tương tác bàn phím vì không tìm được đối tượng ctl00_ctl00_contentPane_MainPanel_MainContent_tbPassword_I 
        if (Password != "") and (Password != NAN ):
            browser_actions.send_keys(Keys.TAB)
            browser_actions.send_keys(Password)
            browser_actions.send_keys(Keys.PAGE_DOWN)
            browser_actions.send_keys(Keys.TAB)
            browser_actions.send_keys(Keys.TAB)
            browser_actions.perform()
        else:
            print("Please type the password")

        # Nhập captcha
        print("Please type the captcha")
        print("and submit")
        
        # browser.find_element(By.ID, "cLogIn1_bt_cLogIn_CD").send_keys(Keys.ENTER)
        try:
            elem = WebDriverWait(browser, 30).until(
                # Đợi cho tới khi title của trình duyệt đổi tên mới. Đã chạy tốt
                EC.title_contains(ExpectedTitle)
                # Đợi cho tới khi một handle được tìm thấy. Đã chạy tốt
                #EC.presence_of_element_located((By.ID, "ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses_DXPagerBottom_PBN")) #This is a dummy element
            )
            print("Login successfully.")
        except:
            print("Login process is out of time. Please do it again.")
            browser.quit()          
        print("AutoLogin finished.")            
        
        

    
    #-----------------------------------------------------------------------------------------------------
    # Thử nghiệm:
    #    Ở trang course-list: trên browser, mở console, chỉ cần gọi trực tiếp hàm 
    #         ASPx.GVPagerOnClick('ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses','PN479')
    #    và thay PN479 bằng PN334, là sẽ gọi được tới đúng từng trang.
    #-----------------------------------------------------------------------------------------------------
    def crawldata():
                
        def document_initialised(driver):
            return driver.execute_script("return initialised")
        global browser
        global browser_actions
        
        dataid=[]
        # mảng chứa thông tin về một course
        datacrawl=[]    
        # mảng chứa thông tin các học phần phụ thuộc
        dataextendcrawl=[]
        #Xác định số trang thông tqua thông tin
        PagerBottom= browser.find_element(By.XPATH, '//*[@id="ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses_DXPagerBottom"]/b[1]').get_attribute('innerHTML')
        pageCount =  int(PagerBottom[PagerBottom.find("of")+3:PagerBottom.find("(")-1])
        courseCount = int(PagerBottom[PagerBottom.find("(")+1:PagerBottom.find("items")-1])
        print("Có {page} page với {course} học phần".format(page=pageCount, course=courseCount))


        #Chỉ số của course trong toanf bộ các môn học
        courseIndex = NAN;
        
        #Chỉ số của course trong bảng của 1 trang
        courseRow = NAN; 
        
        #Vòng lặp to, chạy qua tất cả các trang web chứa thông tin học phần
        for pageIndex in range(1, pageCount+1):
            # Nhảy tới trang tiếp theo
            browser.execute_script("ASPx.GVPagerOnClick('ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses','PN{0}');".format(pageIndex-1))
            sleep(1)

            # Khắc phục vấn đề nhảy trang
            courseIndex = (pageIndex-1) * COURSE_PER_PAGE
            
            #Thông báo đang crawl ở page nào
            print("Crawling page {pageIndex}/{pageCount} ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~".format(pageIndex=pageIndex, pageCount=pageCount))
            
            #if pageIndex ==3:
            #    print("Stop to debug at page {p}".format(p=pageIndex))
            
            #Vòng lặp nhỏ, chạy qua tất cả các dòng thông tin về 1 course trong 1 trang web
            for courseRow in range(COURSE_PER_PAGE):
                
                myCourse = NAN
                myCourseTarget = NAN
                myCourseDetail = NAN
                try:
                    # Lấy ra thông tin về một course
                    myCourse = WebDriverWait(browser,5).until(
                        lambda browser: browser.find_element(By.ID,'ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses_DXDataRow{0}'.format(courseIndex))
                    )
                    # Và các thông tin mở rộng: mục tiêu
                    myCourseTarget = WebDriverWait(browser,2).until(
                        lambda browser: browser.find_element(By.ID,'ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses_pr{0}_lbGoals'.format(courseIndex))
                    )
                    # Và các thông tin mở rộng: nội dung
                    myCourseDetail = WebDriverWait(browser,2).until(
                        lambda browser: browser.find_element(By.ID,'ctl00_ctl00_contentPane_MainPanel_MainContent_gvCourses_pr{0}_ASPxLabel1'.format(courseIndex))
                    )
                                       
                except:
                    print("    Not found couse {i} at page {p}".format(i=courseIndex+1, p = pageIndex))
                    continue
                        
                try:
                    #print(myCourse.get_attribute('innerHTML'))
                    #print(myCourseTarget.get_attribute('innerHTML'))
                    #print(myCourseDetail.get_attribute('innerHTML'))
                                       
                    #Phân tích dữ liệu course và đưa vào danh sách
                    data=myCourse.find_elements(By.CLASS_NAME,'dxgv')
                    coursetarget=html2text.html2text(myCourseTarget.get_attribute('innerHTML')).strip()
                    coursedetail=html2text.html2text(myCourseDetail.get_attribute('innerHTML')).strip()
                    
                    #Tạo cấu trúc lưu trữ
                    datacourse={'STT': courseIndex,
                                'Mã học phần':  data[0].text,
                                'Tên học phần': data[1].text,
                                'Thời lượng':   data[2].text,
                                'Số tín chỉ':   data[3].text,
                                'TC học phí':   data[4].text,
                                'Viện Quản lý': data[5].text,
                                'Học phần điều kiện': data[6].text,
                                'Tên tiếng anh': data[7].text,
                                'Trọng số':     data[8].text,
                                'Mục tiêu':     coursetarget,
                                'Nội dung':     coursedetail
                                }
                    
                    print("---- "  + str(courseRow) + "," + str(courseIndex+1) + "/" + str(courseCount) +": " + str(data[1].text))
                    datacrawl.append(datacourse)
                                                   
                    # Chuyển sang môn học tiếp theo trong cùng trang web
                    courseRow = courseRow + 1
                    
                    # Kiểm tra xem đã hết các loại học phần chưa
                    if (courseIndex+1 == courseCount):
                        print("End of crawling. Successful.")
                        break
                # Kết thúc vòng lặp lấy dữ liệu học phần                    
                    
                except:
                    # Nếu không tìm thấy dòng nữa thì hết thông tin trang. Chuyển sang trang mới
                    break
                finally:
                    # Tăng biến đếm số lượng course đã tìm ra thông tin.
                    # Không sử dụng courseRow thì có thể sẽ loại bỏ courseRow trong tương lai, vì mục tiêu
                    # của courseRow chỉ là lặp bao nhiêu lần thôi
                    courseIndex = courseIndex + 1
                pass
                
            #Kết thúc Vòng lặp nhỏ, chạy qua tất cả các dòng thông tin về 1 course trong 1 trang web
            
                        
            if pageIndex % 5 == 0: 
                df= pd.DataFrame(datacrawl)
                df.to_csv(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv',index = None, header=True, sep=',', encoding='utf-8-sig')
        pass
        #Kết thúc Vòng lặp to, qua tất cả các page
            
        #Ghi du lieu
        #print(datacrawl)
        df= pd.DataFrame(datacrawl)
        df.to_csv(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv',index = None, header=True, sep=',', encoding='utf-8-sig')
        #dong trinh duyet
        browser.close()


#Chuyển đổi đường dẫn tương đối thành tuyệt đối
if __debug__: 
    COURSE_COLLECTION_FOLDER = os.getcwd() + '/' + COURSE_COLLECTION_FOLDER
else:
    COURSE_COLLECTION_FOLDER = os.getcwd() + '/../' + COURSE_COLLECTION_FOLDER

Crawl.autologin(LOGIN_USERNAME, LOGIN_PASSWORD, "Courses List")
Crawl.crawldata()
