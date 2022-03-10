from turtle import color
import pandas as pd
import graphviz
import re
from time import sleep
import os


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'http://sis.hust.edu.vn/ModuleProgram/CourseLists.aspx'   

#Thư mục chứa kết quả
#COURSE_COLLECTION_FOLDER = "/../assets"
COURSE_COLLECTION_FOLDER = "/assets"


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
                c.attr(label='cluster' + str(i),color='red')
                handlesubchildnode(c, a[i], c.name,setHP,HP,dot)
            if i > 0: dot.edge(clustername + str(i), clustername + str(i - 1), arrowhead='none')

    else:
        if subchildnode.find("OR") == -1 and subchildnode.find("AND") == -1 and subchildnode.find(
                ",") == -1 and subchildnode.find("/") == -1:
            if spliit(subchildnode) in setHP:
                dota.edge(HP, spliit(subchildnode), label='')
            else:
                dot.node(spliit(subchildnode))
            setHP.add(spliit(subchildnode))
        else:
            b = spliit(subchildnode).split("/")
            if len(b) > 1:
                for j in b:
                    if j in setHP:
                        dota.edge(HP, j, label='')
                    else:
                        dot.node(j)
                        f = finddependent(j)
                        findedge(j, dot, setHP, f)


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
        
    #Phân tích text chứa thông tin học phần theo kiểu của sis        
    a = spliit(dependentHP).split(",")
    j = 0
    pre = ""
    nex = ""
    for i in range(len(a)):
        if a[i].find("OR") == -1 and a[i].find("AND") == -1 and a[i].find(",") == -1 and a[i].find("/") == -1:
            # Nếu chuỗi text (mã học phần đang xét) là đơn độc
            dot.edge(HP, spliit(a[i]), label='')
            f = finddependent(a[i])
            findedge(a[i], dot, setHP, f)
            if i == 0:
                pre = a[i]
            else:
                nex = a[i]
                dot.edge(pre, nex, arrowhead='none')
                pre = nex
        else:
            # Nếu kí tự đang xét là kí tự thường
            with dot.subgraph(name='cluster'  + str(j)) as c:
                c.attr(label='cluster'  + str(j),color='red')
                dot.edge(HP, 'cluster'  + str(j))
                subchildnodes = a[i].split("/")
                for subchildnode in subchildnodes:
                    handlesubchildnode(c, subchildnode, c.name, setHP, HP, dot)
            if i == 0:
                pre = 'cluster'  + str(j)
            else:
                nex = 'cluster'  + str(j)
                dot.edge(pre, nex, arrowhead='none')
                pre = nex
            j = j + 1


#     for edge in setedge:
#         e = edge.split(' ')
#         if e[0]==HP :
#             arrnode.append(e[1])
#             edgeHP.add(edge)
#     if len(arrnode)>1:
#         with dot.subgraph(name='cluster'+str(HP)) as c:
#             for node in arrnode:
#                 c.node(node)
#                 findedge(node,c,edgeHP)
#     else:
#         if len(arrnode)==1 : findedge(arrnode[0],dot,edgeHP)
def finddependent(HP):
    a = ""
    for index, row in course_relationship.iterrows():
        if HP == row['X']:
            a = row['Y'].replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    return a


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import graphviz

#Load dữ liệu học phần
course = pd.read_csv(os.getcwd() + COURSE_COLLECTION_FOLDER + '/CourseListdata.csv')
# data[['id', 'Mã học phần']]

# Lấy thành phần để xây dựng đồ thị
course_relationship=course[['Mã học phần','Học phần điều kiện']].rename({'Mã học phần': 'X', 'Học phần điều kiện': 'Y'}, axis=1)
course_relationship=course_relationship[~course_relationship.Y.isnull()]
print(course_relationship)


setHP = set()
for index, row in course_relationship.iterrows():
    if not( (index == 917) or (index ==918) or (index == 6923)):
        continue;
    dot = graphviz.Digraph('G', 
                           node_attr={'shape': 'record',}, 
                           edge_attr={'len': '2.0'}
                           )
    # Nén: các node cluster sẽ lồng vào nhau
    dot.attr(compound='true')
    
    # Đưa nút gốc, mã học phần gốc vào, với màu sắc chỉ định
    dot.attr('node', shape='box', color='red:orange', style='filled', gradientangle='270', fontcolor='white')
    dot.node(row['X'], label=row['X'])
    
    # Thuộc tính cho các môn phụ thuộc
    dot.attr('node', shape='box', color='lightblue', style='filled', fontcolor='black')

    # Chuẩn hóa dữ liệu từ file csv
    #   - bỏ kí tự "*= !"
    b=row['Y'].replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    print("Vẽ đồ thị: HP " + row['X']+ " --dk--> " + b)
    
    # Lần theo dấu vết các cạnh là các học phần phụ thuộc
    findedge(row["X"], dot, setHP, b)
    
    #Vẽ đồ thị
    dot.render('dotsourcemoredetail/' + row['X'], view=False,format='png')
    dot.clear()