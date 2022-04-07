# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Thuật toán được phát triển bởi
#     Bùi Đức Chế, 20183694, https://github.com/buiducche/project3
#  Syntax:
#         cd viz
#         python ./graphcoursemoredetail.py
#  Output ../assets/*.png
#  Issue: thuật toán đệ qui và không tái sử dụng việc phân tích cấu trúc csv đầu vào
#         nên bị chậm
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import random
import pandas as pd
import graphviz
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx'   

#Thư mục chứa kết quả
COURSE_COLLECTION_FOLDER = "/../assets"
#COURSE_COLLECTION_FOLDER = "/assets"

lineColors=["blue","#34084D","#00539B","#183b0b","#93585e"];

MAX_DEPENDANCY = 50
COMMON_NAME = "so many"

def spliit(ss):
    """_summary_
        Chuẩn hóa cú pháp của phòng đào tạo thành cú pháp riêng.
    Args:
        ss (_type_): _description_
    Returns:
        _type_: _description_
    """    
    if ss.find("OR") != -1 or ss.find("AND") != -1:
        ss = ss.replace("AND", ",").replace("OR", "/")
    if ss.find("(") != -1:
        subss = []
        sps = ""
        tick = 0;
        seq = ""
        check = False
        for i in range(len(ss)):
            if check == True:
                if ss[i] == "," or ss[i] == "/":
                    seq = seq + ss[i]
                check = False
            else:
                if (tick == 1 and ss[i] == ")") or (tick == 0 and ss[i] == "("):
                    if sps != "":
                        subss.append(sps)
                        check = True
                    sps = sps + ss[i]
                    sps = ""
                else:
                    if (tick == 0 and (ss[i] == "," or ss[i] == "/")):
                        subss.append(sps)
                        seq = seq + ss[i]
                        sps = ""
                    else:
                        sps = sps + ss[i]
            if ss[i] == "(": tick += 1
            if ss[i] == ")": tick -= 1
        if sps != "": subss.append(sps)
        data = ""
        seqposition = 0
        for sub in subss:
            subrp = sub.replace(",", "AND").replace("/", "OR")
            data = data + subrp
            if seqposition != len(seq): data = data + seq[seqposition]
            seqposition = seqposition + 1
        return data
    else:
        return ss


def handlesubchildnode(dot, subchildnode, clustername, setHP, HP, dota):
    a = spliit(subchildnode).split(",")
    if len(a) > 1:
        for i in range(len(a)):
            with dot.subgraph(name=clustername + str(i)) as c:
                c.attr(label='cluster' + HP + "_" + str(i),color='red')
                handlesubchildnode(c, a[i], c.name,setHP,HP,dot)
            # Tạo đường nối giữa các cluster ngang hàng    
            #if i > 0:
            #    dot.edge(clustername + str(i), clustername + str(i - 1), arrowhead='none', color=random.choice(lineColors))

    else:
        if subchildnode.find("OR") == -1 and subchildnode.find("AND") == -1 and subchildnode.find(
                ",") == -1 and subchildnode.find("/") == -1:
            if spliit(subchildnode) in setHP:
                dota.edge(HP, spliit(subchildnode), label='', arrowhead='none', color=random.choice(lineColors))
            else:
                dot.node(spliit(subchildnode))
            setHP.add(spliit(subchildnode))
        else:
            b = spliit(subchildnode).split("/")
            if len(b) > 1:
                for j in b:
                    if j in setHP:
                        dota.edge(HP, j, label='', color=random.choice(lineColors))
                    else:
                        dot.node(j)
                        f = finddependent(j)
                        findedge(j, dot, setHP, f )


def findedge(HP, dot, setHP, dependentHP):
    """_summary_
        Tìm kiếm các cạnh phụ thuộc của 1 học phần, đệ qui
    Args:
        HP (_type_): Mã học phần cần tìm. Ví dụ IT3030
        dot (_type_): handler điều khiển graphviz
        setHP (set): tập hợp chứ các cạnh phụ thuộc
        dependentHP (string): text mô tả sự phụ thuộc của sis
    """    
    
    # Điều kiện dừng đệ qui: khi học phần là nút lá
    if dependentHP == "":
        setHP.add(HP)
        return
    # Điều kiện dừng đệ qui: khi học phần đã có trong danh sách cạnh
    if HP in setHP:
        return
    else:
        setHP.add(HP)
    # Điều kiện dừng đệ qui: kích thước đã quá l
    if len(setHP) > MAX_DEPENDANCY:
        dot.attr('node', shape='folder')
        dot.node(COMMON_NAME, label=COMMON_NAME)
        dot.attr('node', shape='box')       
        return
        
    #Phân tích text chứa thông tin học phần theo kiểu của sis        
    a = spliit(dependentHP).split(",")
    j = 0
    pre = ""
    nex = ""
    for i in range(len(a)):
        if a[i].find("(") == -1 and a[i].find(")") == -1:
            # Nếu chuỗi text (mã học phần đang xét) là đơn độc
            dot.edge(HP, spliit(a[i]), label='', arrowhead='none', color=random.choice(lineColors))
            f = finddependent(a[i])
            findedge(a[i], dot, setHP, f)
            if i == 0:
                pre = a[i]
            else:
                nex = a[i]
                # Hai anh này ngang cấp nhau. Không cần nối
                # dot.edge(pre, nex, arrowhead='none')
                pre = nex
        else:
            # Nếu kí tự đang xét là kí tự thường
            with dot.subgraph(name='cluster' + HP + "_"  + str(j)) as c:
                c.attr(label='cluster' + HP + "_"  + str(j),color='red')
                dot.edge(HP, 'cluster' + HP + "_"  + str(j), arrowhead='none', color=random.choice(lineColors))
                subchildnodes = a[i].split("/")
                for subchildnode in subchildnodes:
                    handlesubchildnode(c, subchildnode, c.name, setHP, HP, dot)
            if i == 0:
                pre = 'cluster' + HP + "_"  + str(j)
            else:
                nex = 'cluster' + HP + "_"  + str(j)
                # Ngang hàng thì không phải nối
                #dot.edge(pre, nex, arrowhead='odiamond')
                pre = nex
            j = j + 1

def finddependent(HP):
    a = ""
    for index, row in course_relationship.iterrows():
        if HP == row['X']:
            a = str(row['Y']).replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    return a

def findCaller(HP, dot, setHP):
    """_summary_
        Tìm kiếm các môn học bị phụ thuộc vào môn hiện thời
    Args:
        HP (_type_): Mã học phần cần tìm. Ví dụ IT3030
        dot (_type_): handler điều khiển graphviz
        setHP (set): tập hợp chứa các cạnh phụ thuộc
    """    

    # Hàng đợi cần tìm kiếm phụ thuộc
    caller_queue = []
    caller_queue.append(HP)

    #Giới hạn số lượt quét học phần phụ thuộc
    limited = 0;
    while len(caller_queue)>0 :
        myCourse = caller_queue.pop();
        
        for index, row in course_relationship.iterrows():
            # Tìm xem học phần này có môn nào phụ thuộc không
            pos = str(row['Y']).find(myCourse)
            if pos < 0 :
                continue
            if (limited > MAX_DEPENDANCY):
                Caller = COMMON_NAME
            else:    
                Caller = row['X']
    
            # Điều kiện dừng đệ qui: khi học phần đã có trong danh sách cạnh
            if Caller in setHP:
               continue
            else:
               setHP.add(Caller);
                       
            #Nếu có môn phụ thuộc, lại kiểm tra xem môn đó là phụ thuộc 100%, hay là OR.
            halfCaller = False;
            if (pos>0 and row['Y'][pos-1] == "/"):   
                halfCaller = True      
            if (pos < len(row['Y'])-1 and row['Y'][pos+1] == "/"):   
                halfCaller = True 
            
            # Thêm vào đồ thị    
            if halfCaller:
                dot.edge(Caller, myCourse, style="dotted")
            else:
                dot.edge(Caller, myCourse)     
            
            # Mở rộng danh sách cần đệ qui 
            if (limited <= MAX_DEPENDANCY):
                limited = limited + 1
                caller_queue.append(Caller);
        # Kết thúc vòng lặp tìm xem có môn học nào phụ thuộc vào myCourse không?           
    if (limited > MAX_DEPENDANCY):    
        dot.attr('node', shape='folder')
        dot.node(COMMON_NAME, label=COMMON_NAME)
        dot.attr('node', shape='box')
    return
    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import graphviz

#Chuyển đổi đường dẫn tương đối thành tuyệt đối
COURSE_COLLECTION_FOLDER = os.getcwd() + COURSE_COLLECTION_FOLDER

#Load dữ liệu học phần
courses = pd.read_csv(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv')
#courses = pd.read_csv("E:\StProjects/2020-2021/BuiDucChe_CrawlVaVeCayPhuThuocHocPhan/sources/assets/CourseListdata.csv")

# data[['id', 'Mã học phần']]

#Bố trí lại thông tin phụ thuộc
standardizedCourses = [];
for index, row in courses.iterrows():
    dk=str(row['Học phần điều kiện']);
    dependency=dk.replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    myCourse={'index':index, 
              'HP':row['Mã học phần'], 
              "Dep":dependency
              }
    standardizedCourses.append(myCourse)
#print(standardizedCourses);


# Lấy thành phần để xây dựng đồ thị
course_relationship=courses[['Mã học phần','Học phần điều kiện']].rename({'Mã học phần': 'X', 'Học phần điều kiện': 'Y'}, axis=1)

setHP = set()
for index, row in course_relationship.iterrows():
    setHP.clear();
    dot = graphviz.Digraph('G', 
                           node_attr={'shape': 'record',}, 
                           edge_attr={'len': '2.0'}
                           )
    # Nén: các node cluster sẽ lồng vào nhau
    dot.attr(compound='true')
    
    # Đưa nút gốc, mã học phần gốc vào, với màu sắc chỉ định
    # Tham khảo: https://graphviz.org/doc/info/shapes.html
    dot.attr('node', shape='house', color='red:orange', style='filled', gradientangle='270', fontcolor='white')
    dot.node(row['X'], label=row['X'])
    

    # Chuẩn hóa dữ liệu từ file csv
    #   - bỏ kí tự "*= !"
    b=str(row['Y']).replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    print("Vẽ đồ thị: HP " + row['X']+ " --dk--> " + b)
    
    # Lần theo dấu vết các cạnh là các học phần phụ thuộc
    dot.attr('node', shape='box', color='lightblue', style='filled', fontcolor='black')    
    dot.edge_attr.update(arrowhead='none', arrowsize='1')
    findedge(row["X"], dot, setHP, b)
    
    # Lần theo dấu vết các cạnh là các học phần cần môn này
    dot.attr('node', shape='box', color='#ff000042', style='filled', fontcolor='black')    
    dot.edge_attr.update(arrowhead='inv', arrowsize='1',)
    findCaller(row["X"], dot, setHP)
    
    #Vẽ đồ thị
    dot.render(COURSE_COLLECTION_FOLDER+ '/' + row['X'], view=False,format='png')
    dot.clear()