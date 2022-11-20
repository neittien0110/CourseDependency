# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Thuật toán được phát triển bởi
#     Bùi Đức Chế, 20183694, https://github.com/buiducche/project3
#     Nguyễn Đức Tiến, https://github.com/neittien0110
#  Syntax:
#         cd viz
#         python ./gentree.py
#  Output ../assets/*.png
#  Log:
#      - Tăng tốc độ bằng cách hiệu chỉnh file đầu vào csv một lần, rồi áp dụng cho 
#        thuật toán phía sau
#      - Giải đệ qui bằng vòng lặp lan theo chiều rộng. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from enum import Enum
import random
from numpy import NAN
import pandas as pd
import graphviz
import os
import regex as re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx'   

#Thư mục chứa file đâu vào
COURSE_COLLECTION_FOLDER = "assets"
#Thư mục chứa file đâu ra
OUTPUT_FOLDER = COURSE_COLLECTION_FOLDER + "/graph0"

lineColors=["blue","#34084D","#00539B","#183b0b","#93585e"];

MAX_DEPENDANCY = 100
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
    """_summary_

    Args:
        dot (Graphviz):   Đối tượng quản lý đồ thị Graphviz. Do tính đệ qui của đồ thị nên dot có thể là một vùng con.
        subchildnode (_type_): _description_
        clustername (_type_): _description_
        setHP (_type_): _description_
        HP (_type_): _description_
        dota (_type_): _description_
    """
    spliit_subchildnode = spliit(subchildnode)
    a = spliit_subchildnode.split(",")
    if len(a) > 1:
        for i in range(len(a)):
            with dot.subgraph(name=clustername + str(i)) as c:
                handlesubchildnode(c, a[i], c.name,setHP,HP,dot)
            # Nối giữa các cluster với nhau để chứng tỏ ngang hàng. Không cần    
            #if i > 0: 
            #    dot.edge(clustername + str(i), clustername + str(i - 1), arrowhead='none', color=random.choice(lineColors))

    else:
        if subchildnode.find("OR") == -1 and subchildnode.find("AND") == -1 and subchildnode.find(
                ",") == -1 and subchildnode.find("/") == -1:
            if spliit_subchildnode in setHP:
                #Chưa thành công
                #RegisterAndRenderNode(dota, spliit_subchildnode, style=NodeStyle.Dependency)                    
                dota.edge(HP, spliit_subchildnode, label='', arrowhead='none', color=random.choice(lineColors))
            else:
                ''' Đăng kí học phần điều kiện. từ trên xuống'''
                RegisterAndRenderNode(dot, spliit_subchildnode, style=NodeStyle.Dependency)   
                #dot.node(spliit_subchildnode)
            setHP.add(spliit_subchildnode)
        else:
            b = spliit_subchildnode.split("/")
            if len(b) > 1:
                for j in b:
                    if j in setHP:
                        #Chưa thành công
                        #RegisterAndRenderNode(dota, j, style=NodeStyle.Dependency)                   
                        dota.edge(HP, j, label='', color=random.choice(lineColors))
                    else:
                        #RegisterAndRenderNode(dot, j, style=NodeStyle.Caller)   
                        dot.node(j)
                        f = getDependent(j)
                        findedge(j, dot, setHP, f )


def findedge(HP, dot, setHP, dependentText):
    """_summary_
        Tìm kiếm các cạnh phụ thuộc của 1 học phần, đệ qui
    Args:
        HP (_type_): Mã học phần cần tìm. Ví dụ IT3030
        dot (_type_): handler điều khiển graphviz
        setHP (set): tập hợp chứ các cạnh phụ thuộc
        dependentHP (string): text mô tả sự phụ thuộc của sis
    """    
    
    # Điều kiện dừng đệ qui: khi học phần là nút lá
    if dependentText == "":
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
    dependentHPs = spliit(dependentText).split(",")
    j = 0
    pre = ""
    nex = ""
    
    for i in range(len(dependentHPs)):
        if dependentHPs[i].find("OR") >= 0 or dependentHPs[i].find("/") >= 0: 
            conditionOR = True 
        else: 
            conditionOR = False
        if dependentHPs[i].find("AND") >= 0 or dependentHPs[i].find(",") >= 0: 
            conditionAND = True 
        else: 
            conditionAND = False
                        
        if (not conditionOR and  not conditionAND) :
            # Nếu chuỗi text (mã học phần đang xét) là đơn độc. Ví dụ IT1110
            dot.edge(HP, spliit(dependentHPs[i]), label='', arrowhead='none', color=random.choice(lineColors))
            f = getDependent(dependentHPs[i])
            findedge(dependentHPs[i], dot, setHP, f)
            #Hai anh này ngang cấp nhau. Không cần nối
            #if i == 0:
            #    pre = a[i]
            #else:
            #    nex = a[i]
            #    dot.edge(pre, nex, arrowhead='none')
            #    pre = nex
        else:
            # Nếu kí tự đang xét là kí tự thường
            clusterName = 'cluster' + HP + "_"  + str(j)
            with dot.subgraph(name=clusterName) as c:
                #Đặt tên cho nhóm cluster các môn học phụ thuộc
                if conditionOR:
                    c.attr(label="ĐIỀU KIỆN HOẶC",color='red')
                elif conditionAND:
                    c.attr(label="ĐIỀU KIỆN VÀ TẤT CẢ",color='red')
                    
                #Tạo một node tượng trưng, đại diện cho cluster, vì Graphviz không cho phép cạnh với cluster
                RegisterAndRenderNode(c, clusterName, style=NodeStyle.DependencyCluster)
                
                # Vẽ đường bao cho nhóm các học phần điều kiện
                dot.edge(HP, clusterName, lhead=clusterName, arrowhead='none', color=random.choice(lineColors))
                subchildnodes = dependentHPs[i].split("/")
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

def getDependent(HP):
    for myCourse in standardizedCourses:
        if HP == myCourse['X']:
            return myCourse['Y']
    return ""

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
        victim = caller_queue.pop();
        
        for myCourse in standardizedCourses:
            # Tìm xem học phần này có môn nào phụ thuộc không
            pos = str(myCourse['Y']).find(victim)
            if pos < 0 :
                continue
            if (limited > MAX_DEPENDANCY):
                Caller = COMMON_NAME
            else:    
                Caller = myCourse['X']
    
            # Điều kiện dừng đệ qui: khi học phần đã có trong danh sách cạnh
            if Caller in setHP:
               continue
            else:
               setHP.add(Caller);
                       
            #Nếu có môn phụ thuộc, lại kiểm tra xem môn đó là phụ thuộc 100%, hay là OR.
            halfCaller = False;
            if (pos>0 and myCourse['Y'][pos-1] == "/"):   
                halfCaller = True      
            if (pos < len(myCourse['Y'])-1 and myCourse['Y'][pos+1] == "/"):   
                halfCaller = True 

            # Tạo node caller và..
            RegisterAndRenderNode(dot, Caller, NodeStyle.Caller)   
            
            # .. và vẽ thêm cạnh nối vào đồ thị    
            if halfCaller:
                dot.edge(Caller, victim, style="dotted")
            else: 
                dot.edge(Caller, victim)  
                
            
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
    

class NodeStyle(Enum):
    ''' Các loại node để vẽ đồ thị'''
    Root = 0
    Caller =1
    CallerCluster =2
    Dependency = -1
    DependencyCluster = -2


def FindFullCourse(courseId):
    ''' Tìm cấu trúc chứa thông tin đầy đủ về một mã học phần nào đó'''
    global standardizedCourses; 
    for x in standardizedCourses:
        if x['X']==courseId:
            return x  
    return 0 

def RegisterAndRenderNode(dot, coureId, style):
    """_summary_
        Vẽ thông tin node lên đồ thị 
    Args:
        dot (Graphviz):   Đối tượng quản lý đồ thị Graphviz. Do tính đệ qui của đồ thị nên dot có thể là một vùng con.
        coureId (string): Mã học phần. Ví dụ IT1110.
        style (NodeStyle): kiểu hiển thị
    """   
    if (style == NodeStyle.CallerCluster or style == NodeStyle.DependencyCluster):
        myCourse = 0
    else:
        myCourse = FindFullCourse(coureId)
    
    ''' Cấu trúc chứa thông tin cần vẽ '''
    graphtype = 1

    if myCourse != 0: 
        if graphtype == 0:
            if (style == NodeStyle.Root):
                dot.attr('node', shape='house', color='red:orange', style='filled', gradientangle='270', fontcolor='white')
            if (style == NodeStyle.Caller):
                pass
            if (style == NodeStyle.Dependency):
                dot.attr('node', shape='record', color='lightblue', style='filled', fontcolor='black')
                pass        
            dot.node(myCourse['Mã học phần'], label=myCourse['Mã học phần']) 
        elif graphtype == 1:        
            # Trường hợp là node của học phần gốc cần tính toán
            if (style == NodeStyle.Root):
                dot.attr('node', shape='record', color='red:orange', style='filled', gradientangle='270', fontcolor='white', fontsize="18", fontname="Tahoma")
            # Trường hợp là node của học phần bị phụ thuộc vào học phần hiện tại
            if (style == NodeStyle.Caller):
                dot.attr('node', shape='record', color='#ff000042', style='filled', fontcolor='black', fontsize="14", fontname="Tahoma")
                pass
            # Trường hợp là node của học phần điều kiện
            if (style == NodeStyle.Dependency):
                dot.attr('node', shape='record', color='lightblue', style='filled', fontcolor='black', fontsize="14", fontname="Tahoma")
                pass
            try: 
                dot.node(myCourse['Mã học phần'], label="{" + "{id} | {name} | {credit}".format(
                id = myCourse['Mã học phần'],
                name=myCourse['Tên học phần'],
                credit=myCourse['Thời lượng'] + " / " + str(myCourse['TC học phí']) + "đ / " + str(myCourse['Trọng số'])  ,
                ) + "}")          
            except:
                # Ghi nhận lỗi với node có tên là "so many"
                print ("Không vẽ được với " + str(coureId))    
    else:
        dot.attr(shape='box', style='rounded' ,color='blue')
        dot.attr('node', shape='record', color='lightblue', style='filled', fontcolor='black', fontsize="14", fontname="Tahoma")
        # Trường hợp là khung của nhóm môn học thì không có thông tin credit
        dot.edge_attr.update(arrowhead='inv', arrowsize='1',)
        dot.node(coureId)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import graphviz

import csv

  


#Chuyển đổi đường dẫn tương đối thành tuyệt đối
COURSE_COLLECTION_FOLDER = os.getcwd() + '/../' + COURSE_COLLECTION_FOLDER
OUTPUT_FOLDER = os.getcwd() + '/../' +  OUTPUT_FOLDER

csvfile = open(COURSE_COLLECTION_FOLDER + '/CourseListdata.csv', 'r',encoding="utf-8-sig")
'''File dữ liệu đầu vào, kết quả của quá trình crawl dữ liệu trang sis'''
#csvfile = open("E:\StProjects/2020-2021\BuiDucChe_CrawlVaVeCayPhuThuocHocPhan\sources/assets/CourseListdata.csv", 'r',encoding="utf-8")

reader = csv.DictReader(csvfile)

standardizedCourses = []; 
''' Danh sách đầy đủ các course với thông tin đã được chuẩn hoá.'''

#Bố trí lại thông tin phụ thuộc
for myCourse in reader:
    dk=str(myCourse['Học phần điều kiện']);
    dependency=dk.replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    
    myCourse['X']= myCourse['Mã học phần'] #Mã học phần chính, trùng lặp dữ liệu để tiện cho thuật toán tìm quan hệ
    myCourse['Y']= dependency       #Mã học phần điều kiện, trùng lặp dữ liệu để tiện cho thuật toán tìm quan hệ
    #if len(dependency) > 60:
    #    print(myCourse)
    standardizedCourses.append(myCourse)
#print(standardizedCourses[12]['HP']);


setHP = set()
courseIndex = 0
for myCourse in standardizedCourses:
    courseIndex  = courseIndex + 1;
    
    #if not ((myCourse['X'] == 'IT1110') or (myCourse['X'] == 'IT3030') or (myCourse['X'] == 'IT4015') or (myCourse['X']=='IT3150')):
    #    continue        
    #if courseIndex < 2520: 
    #    continue
    #if (myCourse['X'] != 'IT3030'):
    #   continue        
                    
    setHP.clear();
    dot = graphviz.Digraph('G', 
                           node_attr={'shape': 'record',}, 
                           edge_attr={'len': '2.0'}
                           )
    # Nén: các node cluster sẽ lồng vào nhau
    dot.attr(compound='true')
    
    # Đưa nút gốc, mã học phần gốc vào, với màu sắc chỉ định
    # Tham khảo: https://graphviz.org/doc/info/shapes.html
    RegisterAndRenderNode(dot, myCourse['X'], style=NodeStyle.Root)   

    # Chuẩn hóa dữ liệu từ file csv
    print("Vẽ đồ thị: HP " + myCourse['X']+ " --dk--> " + myCourse['Y'])
    
    # Lần theo dấu vết các cạnh là các học phần phụ thuộc
    dot.attr('node', shape='box', color='white', style='filled', fontcolor='black')     # Không hiểu sao phải thiết lập thuộc tính ở đây, nếu không thì node đại diện cho cluster sẽ kông đổi atrribute được
    dot.edge_attr.update(arrowhead='none', arrowsize='1')
    findedge(myCourse["X"], dot, setHP, myCourse['Y'])
    
    # Lần theo dấu vết các cạnh là các học phần cần môn này
    #dot.attr('node', shape='box', color='#ff000042', style='filled', fontcolor='black')    
    dot.edge_attr.update(arrowhead='inv', arrowsize='1',)
    findCaller(myCourse["X"], dot, setHP)
    
    #Vẽ đồ thị
    try:
        # format='svg'
        dot.render(OUTPUT_FOLDER + '/' + myCourse['X'], view=False,format='png')
    except:
        print("     error to export to file with {0}".format(myCourse['X']))
        pass    
    dot.clear()