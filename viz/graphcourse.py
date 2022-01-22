import pandas as pd
import graphviz
import re
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

#Danh sách các cạnh
setedge=set()
for index, row in graph.iterrows():
    # f.write(row['Y']+"\n")
    a=re.split('=|/|, |,|\)|\(|\*', row['Y'])
    for i in a:
        if i !='': setedge.add(row['X']+' '+i)
# f.close()
# print(len(setedge))

def drawall():
    dot = graphviz.Digraph(comment='Course')
    dot.format='svg'
    for edge in setedge:
        e=edge.split(' ')
        dot.edge(e[0],e[1], label='')
    dot.render('test-output/allcourse', view=False)
    dot.clear()

def findedge(HP,dot,edgeHP):
    dot.node(HP)
    arrnode=[]
    for edge in setedge:
        e = edge.split(' ')
        if e[0]==HP :
            arrnode.append(e[1])
            edgeHP.add(edge)
    if len(arrnode)>1:
        with dot.subgraph(name='cluster'+str(HP)) as c:
            for node in arrnode:
                c.node(node)
                findedge(node,c,edgeHP)
    else:
        if len(arrnode)==1 : findedge(arrnode[0],dot,edgeHP)


def drawone(HP):
    dot = graphviz.Digraph(comment='Course')
    edgeHP=set()
    dot.format = 'png'
    findedge(HP,dot,edgeHP)
    for edge in edgeHP:
        e=edge.split(' ')
        dot.edge(e[0], e[1], label='')
    dot.render('test-output/courses'+str(HP), view=False)
    print(dot.source)
    dot.clear()
    edgeHP.clear()
drawone('IT3070')