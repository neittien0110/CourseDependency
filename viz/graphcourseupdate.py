import pandas as pd
import graphviz
import re
from time import sleep
#Load dữ liệu học phần
data = pd.read_csv('CourseListdata.csv')
# data[['id', 'Mã học phần']]

#Load dữ liệu mở rộng
dataex = pd.read_csv('CourseListdataextend.csv')
# dataex[['id','Học phần điều kiện']]

# join 2 bảng dữ liệu
course=data.merge(dataex, on="id")

# Lấy thành phần để xây dựng đồ thị
course_relationship=course[['Mã học phần','Học phần điều kiện']].rename({'Mã học phần': 'X', 'Học phần điều kiện': 'Y'}, axis=1)
graph=course_relationship[~course_relationship.Y.isnull()]
# f= open("DK.txt","w")
def spliit(HP, ss):
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


def handlesubchildnode(dot, subchildnode, clustername):
    a = spliit(HP, subchildnode).split(",")
    if len(a) > 1:
        for i in range(len(a)):
            with dot.subgraph(name=clustername + str(i)) as c:
                handlesubchildnode(c, a[i], c.name)
            if i > 0: dot.edge(clustername + str(i), clustername + str(i - 1), arrowhead='none')

    else:
        if subchildnode.find("OR") == -1 and subchildnode.find("AND") == -1 and subchildnode.find(
                ",") == -1 and subchildnode.find("/") == -1:
            dot.node(spliit(HP, subchildnode))
        else:
            b = spliit(HP, subchildnode).split("/")
            if len(b) > 1:
                for j in b:
                    dot.node(j)


def findedge(HP, dot, setHP, dependentHP):
    arrnode = []
    a = spliit(HP, b).split(",")
    j = 0
    pre = ""
    nex = ""
    print(len(a))
    for i in range(len(a)):
        if a[i].find("OR") == -1 and a[i].find("AND") == -1 and a[i].find(",") == -1 and a[i].find("/") == -1:
            print(a[i])
            dot.edge(HP, spliit(HP, a[i]), label='')
            if i == 0:
                pre = a[i]
            else:
                nex = a[i]
                dot.edge(pre, nex, arrowhead='none')
                pre = nex
        else:
            with dot.subgraph(name='cluster' + str(HP) + str(j)) as c:
                dot.edge(HP, 'cluster' + str(HP) + str(j))
                subchildnodes = a[i].split("/")
                for subchildnode in subchildnodes:
                    handlesubchildnode(c, subchildnode, c.name)
            if i == 0:
                pre = 'cluster' + str(HP) + str(j)
            else:
                nex = 'cluster' + str(HP) + str(j)
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
import graphviz
setHP = set()
HP =""
for index, row in graph.iterrows():
    dot = graphviz.Digraph('G', filename='cluster_edge.gv', node_attr={'shape': 'record'}, edge_attr={'len': '2.0'},
                           engine='fdp')
    dot.attr(compound='true')
    a=re.split('=|/|, |,|\)|\(|\*', row['Y'])
    b=row['Y'].replace("*", "").replace("=", "").replace(" ", "").replace("!", "")
    print(row['X']+" "+b)
    findedge(row["X"], dot, setHP, b)
    print(dot.source)
    dot.render('outputdotsourcemoredetail/courses' + row['X'], view=False,format='png')
    sleep(1)
    dot.clear()


