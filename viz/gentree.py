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
import graphviz
import csv
import argparse                     # module phân tích tham số dòng lệnh. Ví dụ. python ./gentree.py -s IT1110
from infix_prefix import ExpressionConverter  
''' Hàm chuyển đổi biểu thức trung tố --> hậu tố'''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# create a url variable that is the website link that needs to crawl
BASE_URL = 'http://sinno.soict.ai:37080/course'   

#Thư mục chứa file đâu vào
COURSE_COLLECTION_FOLDER = "assets" 
'''Thư mục chứa file đâu vào'''

#Cơ sở dữ liệu của các học phần, được thu thập từ trang ctt-sis
COURSE_LIST_FILE = 'CourseListdata.csv'
'''Cơ sở dữ liệu của các học phần, được thu thập từ trang ctt-sis'''

#Thư mục chứa file ảnh đầu ra
OUTPUT_FOLDER = COURSE_COLLECTION_FOLDER + "/graph0"
'''Thư mục chứa file ảnh đầu ra'''

#Màu của các đường nối quan hệ giữa các học phần
lineColors=["blue","orange","red","green","#34084D","#00539B","#183b0b","#23585e"];
'''Màu của các đường nối quan hệ giữa các học phần. Nên bổ sung thêm các màu sẫm cho đa dạng.'''

MAX_DEPENDANCY = 100
COMMON_NAME = "so many"

#Danh sách các học phần thuộc một chương trình đào tạo nào đó, được nhập vào bởi tham số dòng lệnh -p
Education_Programme_Courses=[]
'''Danh sách các học phần thuộc một chương trình đào tạo nào đó, được nhập vào bởi tham số dòng lệnh -p'''
# Tham số dòng lệnh: -p IT2030,IT4991,IT3020,IT3011,IT3180,IT3070,IT3080,IT3160,IT4015,IT3150,IT3930,IT3120,IT3940,IT4409,IT4785,IT4490,IT4501,IT4611,IT4441,IT3170,IT4930,IT3190,IT1110,IT2000,IT3030,IT3040,IT3090,IT3100,IT4653,IT4663,IT4613,IT4480,IT4350,IT4341,IT4931,IT4244,IT4863,IT4906,IT4788,IT4488
#EDUCATION_PROGRAMME_NAME="CNKHMT"
#EDUCATION_PROGRAMME_COURSES = ['IT2030','IT4991','IT3020','IT3011','IT3180','IT3070','IT3080','IT3160','IT4015','IT3150','IT3930','IT3120','IT3940','IT4409','IT4785','IT4490','IT4501','IT4611','IT4441','IT3170','IT4930','IT3190','IT1110','IT2000','IT3030','IT3040','IT3090','IT3100','IT4653','IT4663','IT4613','IT4480','IT4350','IT4341','IT4931','IT4244','IT4863','IT4906','IT4788','IT4488']

# Tham số dòng lệnh: -p IT2030,IT4991,IT3420,IT3020,IT4172,IT4593,IT3011,IT3180,IT3070,IT3080,IT4015,IT3150,IT3120,IT4409,IT4785,IT4611,IT3170,IT4210,IT4735,IT4651,IT1110,IT2000,IT3030,IT3040,IT3090,IT3100,IT4060,IT3943,IT4931,IT4681,IT4263,IT4025,IT3931,IT4831,IT4489
#EDUCATION_PROGRAMME_NAME="CNKTMT"
#EDUCATION_PROGRAMME_COURSES =["IT2030","IT4991","IT3420","IT3020","IT4172","IT4593","IT3011","IT3180","IT3070","IT3080","IT4015","IT3150","IT3120","IT4409","IT4785","IT4611","IT3170","IT4210","IT4735","IT4651","IT1110","IT2000","IT3030","IT3040","IT3090","IT3100","IT4060","IT3943","IT4931","IT4681","IT4263","IT4025","IT3931","IT4831","IT4489"]

# Tham số dòng lệnh: -p IT2030,IT4991,IT3020,IT4172,IT4593,IT3011,IT3180,IT3070,IT3080,IT3160,IT4015,IT3150,IT3930,IT3120,IT3940,IT4931,IT4490,IT3170,IT3190,IT4210,IT4735,IT1110,IT2000,IT3030,IT3040,IT3090,IT3100,IT4653,IT4663,IT4995
#EDUCATION_PROGRAMME_NAME="TNKHMT"
#EDUCATION_PROGRAMME_COURSES =["IT2030","IT4991","IT3020","IT4172","IT4593","IT3011","IT3180","IT3070","IT3080","IT3160","IT4015","IT3150","IT3930","IT3120","IT3940","IT4931","IT4490","IT3170","IT3190","IT4210","IT4735","IT1110","IT2000","IT3030","IT3040","IT3090","IT3100","IT4653","IT4663","IT4995"]

#Tham số dòng lệnh: -p IT3100E,IT4785E,IT3070E,IT3080E,IT2030,IT3160E,IT4142E,IT3020E,IT2110,IT2120,IT3210,IT3220,IT4948,IT3420E,IT2140E,IT4110E,IT4172E,IT4593E,IT3312E,IT3230E,IT3170E,IT4082E,IT3292E,IT3290E,IT3283E,IT3280E,IT4015E,IT5023E,IT5024E,IT4549E,IT4062E,IT3323E,IT4409E,IT4542E,IT3191E,IT4441E,IT4210E,IT4735E,IT4651E,IT4125E
EDUCATION_PROGRAMME_NAME="ICT"
EDUCATION_PROGRAMME_COURSES =["IT3100E","IT4785E","IT3070E","IT3080E","IT2030","IT3160E","IT4142E","IT3020E","IT2110","IT2120","IT3210","IT3220","IT4948","IT3420E","IT2140E","IT4110E","IT4172E","IT4593E","IT3312E","IT3230E","IT3170E","IT4082E","IT3292E","IT3290E","IT3283E","IT3280E","IT4015E","IT5023E","IT5024E","IT4549E","IT4062E","IT3323E","IT4409E","IT4542E","IT3191E","IT4441E","IT4210E","IT4735E","IT4651E","IT4125E"]


def FindFullCourse(courseId):
    ''' Tìm cấu trúc chứa thông tin đầy đủ về một mã học phần nào đó'''
    global standardizedCourses; 
    for x in standardizedCourses:
        if x['X']==courseId:
            return x  
    return 0 

def getDependent(courseId):
    """_summary_
        Lấy danh sách các học phần phụ thuộc
    Args:
        courseId (_type_): học phần muốn tìm kiếm
    Returns:
        _type_: danh sách các học phần phụ thuộc
    """
    for myCourse in standardizedCourses:
        if courseId == myCourse['X']:
            return myCourse['Y']
    return ""

def Operator2NodeStyle(operator):
    if operator == ",":
        return NodeStyle.And
    elif operator == "/":
        return NodeStyle.Or

def Operator2EdgeStyle(operator):
    if operator == ",":
        return "solid"
    elif operator == "/":
        return "dotted"
    else:
        return "solid"

def Operator2EdgeLabel(operator):
    if operator == "=":
        return "song hành"
    elif operator == "!":
        return "tiên quyết"
    else:
        return ""

#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
def findDependant(HP, dot, rootStyle):
    """_summary_
        Tìm kiếm các môn học bị phụ thuộc vào môn hiện thời.
        Thuật giải quét chiều rộng, không đệ qui.
    Args:
        HP (_type_): Mã học phần cần tìm. Ví dụ IT3030
        dot (_type_): handler điều khiển graphviz
        rootStyle (NodeStyle): nút gốc có chuỗi học phần điều kiện là giả định hay thật
    """    


    # Hàng đợi cần tìm kiếm phụ thuộc
    dependant_queue = []
    # Danh sách các học phần đã xử lý xong. Loại bỏ khỏi dependant_queue thì tống vào đây
    scaned_queue = []
    
    # Đưa học phần đầu tiên vào danh sách cần tìm kiếm
    dependant_queue.append(HP)
    RegisterAndRenderNode(dot, HP, rootStyle)

    '''Phụ trách phân tích biểu thức phụ thuộc'''
    EC = ExpressionConverter(); '''Phụ trách phân tích biểu thức phụ thuộc'''
    '''Phụ trách phân tích biểu thức phụ thuộc'''

    #Giới hạn số lượt quét học phần phụ thuộc
    limited = 0;

    #Quét toàn bộ danh sách các học phần cần tìm phụ thuộc
    while len(dependant_queue)>0 :
        #Lấy ra học phần gốc để tìm kiếm phụ thuộc
        victim = dependant_queue.pop();
        if victim in scaned_queue:
            continue
        scaned_queue.append(victim)
        
        #text mô tả sự phụ thuộc của sis
        dependentText = getDependent(victim)
        if (dependentText == ''): continue
        
        #Phân tích text chứa thông tin học phần theo kiểu của sis
        dependentTopo = EC.infixtodict(dependentText)
        
        #Top của cấu trúc phụ thuộc đương nhiên là học phần gốc rồi.
        parent_queue = []
        parent_queue.append(victim)
        parent_queue.append(dependentTopo)
        
        while (len(parent_queue)>0):       
            childrenTopo = parent_queue.pop()
            parent = parent_queue.pop()
            operator = ""
            #Nếu có toán tử 2 toán hạng, thì ngay lập tức tạo node trung gian
            if (childrenTopo.__contains__("operator") and not EC.Has1Operand(childrenTopo["operator"])):
                operator = childrenTopo['operator']
                # Tạo node trung chuyển 
                switch_name, isDuplicate = RegisterAndRenderNode(dot, 
                      str(childrenTopo).__hash__(), Operator2NodeStyle(operator))
                # Lựa chọn 1 màu để tô cho các cạnh
                edge_color = random.choice(lineColors)
                # Tạo 1 cạnh liền duy nhất, nối trực tiếp giữa học phần đang xử lý và điểm trung chuyển
                if HP == parent:
                    width= "5.0"
                else:
                    width = "1.0"
                dot.edge(parent, switch_name, style="solid", penwidth=width, color=edge_color, label="")
                # chuyển parent thành điểm trung gian toán tư luôn
                parent = switch_name
                # Nếu node trung gian đã được vẽ rồi, thì do bản chất của đặt tên bằng hash, chứng tỏ 
                # rằng các node con cũng giống hệt, nên không cần vẽ nữa để tránh tạo nhiều mũi tên
                if isDuplicate:
                    continue
                
            #Kết nối với các toán hạng đang có với 3 trường hợp:
            #   {"operands":[{},{}]}
            #   "IT1110"
            #   ["IT1110", "IT3030"] ????????
            if (childrenTopo.__contains__("operands") and not EC.Has1Operand(childrenTopo["operator"])):
                children = childrenTopo["operands"]
            elif type(childrenTopo) == str or (EC.Has1Operand(childrenTopo["operator"])):
                # Áp dụng cho loại biểu thức điều kiện là "IT1110", hoặc "IT1110="
                children = [childrenTopo]
            else:
                children = childrenTopo
            for operand in children:
                if type(operand) == dict:
                    # Đăng kí ngay để quét tiếp nếu là dạng 2 toán tử                    
                    if not EC.Has1Operand(operand["operator"]):
                        parent_queue.append(parent);
                        parent_queue.append(operand);
                    else:
                        # Nếu là dạng 1 toán tử thì hiển thị luôn
                        RegisterAndRenderNode(dot, operand["operands"][0], NodeStyle.Dependency)
                        # Và tạo 1 cạnh liền duy nhất, nối trực tiếp giữa học phần đang xử lý và học phần phụ thuộc duy nhất
                        dot.edge(parent, operand["operands"][0], style=Operator2EdgeStyle(operator), penwidth="1.0", color=random.choice(lineColors), label=Operator2EdgeLabel(operand['operator']))
                        dependant_queue.append(operand["operands"][0]);                    
                else:
                    # Nếu là dạng toán hạng nút lá, thì hiển thị ngay
                    RegisterAndRenderNode(dot, operand, NodeStyle.Dependency)
                    # Và tạo 1 cạnh liền duy nhất, nối trực tiếp giữa học phần đang xử lý và học phần phụ thuộc duy nhất
                    dot.edge(parent, operand, style=Operator2EdgeStyle(operator), penwidth="1.0", color=random.choice(lineColors))
                    dependant_queue.append(operand);   
        # Hết lệnh if
    # Kết thúc vòng lặp duyệt tất cả các phần tử dependant_queue
    return
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
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
    
    # Đưa học phần đầu tiên vào danh sách cần tìm kiếm
    caller_queue.append(HP)

    #Giới hạn số lượt quét học phần phụ thuộc
    limited = 0;
    
    #Quét toàn bộ danh sách các học phần cần tìm phụ thuộc
    while len(caller_queue)>0 :
        #Lấy ra học phần gốc để tìm kiếm học phần triệu gọi
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
            
            # Vẽ đậm nếu là liên kết trực tiếp với học phần hiện tại    
            if HP == victim:
                width= "5.0"
            else:
                width = "1.0"   
                
            # .. và vẽ thêm cạnh nối vào đồ thị.
            # Vẽ nét đứt nếu bị lệ thuộc một phần (do điều kiện hoặc), và nét liền nếu lệ thuộc hoàn toàn (điều kiện and)
            if halfCaller:
                edge_style="dotted"
                
            else: 
                edge_style="solid"
            
            # Vẽ cạnh
            dot.edge(Caller, victim, style=edge_style, penwidth = width)
            
             
            
            # Mở rộng danh sách cần đệ qui 
            if (limited <= MAX_DEPENDANCY):
                limited = limited + 1
                caller_queue.append(Caller);
        # Kết thúc vòng lặp tìm xem có môn học nào phụ thuộc vào myCourse không?           
    return
    

class NodeStyle(Enum):
    ''' Các loại node để vẽ đồ thị'''
    Root = 0
    Caller =1
    CallerCluster =2
    Dependency = -1
    DependencyCluster = -2
    RootTrial = -3        #Biểu tượng cho thấy học phần điều kiện là giả định.
    And = 9000          #Mã 9xxx dành cho các node tượng trưng/node switch phân cạnh, không phải học phần
    Or =  9001


ScannedNodes = []
''' Danh sách các node đã tồn tại'''

def RegisterAndRenderNode(dot, courseId, style : NodeStyle):
    """_summary_
        Vẽ thông tin node lên đồ thị 
    Args:
        dot (Graphviz):   Đối tượng quản lý đồ thị Graphviz. Do tính đệ qui của đồ thị nên dot có thể là một vùng con.
        courseId (string): Mã học phần, duy nhất. Ví dụ IT1110, hoặc hash(học phần điều kiện)
        style (NodeStyle): kiểu hiển thị. 
    """   
    if (style == NodeStyle.CallerCluster or style == NodeStyle.DependencyCluster):
        myCourse = 0
    else:
        myCourse = FindFullCourse(courseId)
        
    graphNodeId = str(courseId)
    '''Tên định danh của node trong cấu trúc đồ thị Graphviz'''
    
    #Cờ báo hiệu node đã từng tồn tại
    isDuplicate = (graphNodeId in ScannedNodes)
    print (str(style) + " " + graphNodeId)
    if (style == NodeStyle.Root):
        # Trường hợp là node của học phần gốc cần tính toán        
        dot.attr('node', shape='record', color='red:orange', style='filled', gradientangle='270', fontcolor='white', fontsize="18", fontname="Tahoma")
    elif (style == NodeStyle.RootTrial):
        # Trường hợp là node của học phần gốc cần tính toán        
        dot.attr('node', shape='record', color='lightgray:gray', style='filled', gradientangle='0', fontcolor='black', fontsize="15", fontname="Tahoma")
        pass
    elif (style == NodeStyle.Caller):
        # Trường hợp là node của học phần bị phụ thuộc vào học phần hiện tại        
        dot.attr('node', shape='record', color='#ff000042', style='filled', fontcolor='black', fontsize="14", fontname="Tahoma")
        pass
    elif (style == NodeStyle.Dependency):
        # Trường hợp là node của học phần điều kiện
        dot.attr('node', shape='record', color='lightblue', style='filled', fontcolor='black', fontsize="14", fontname="Tahoma")
        pass
    elif (style == NodeStyle.And or style == NodeStyle.Or):
        # Trường hợp là node của học phần điều kiện
        dot.attr('node', shape='circle', color='gray', style='', fontcolor='darkgreen', fontsize="10", fontname="Tahoma")
        pass
    #-------------------------------------------------------------
    if style == NodeStyle.And:
        if not isDuplicate:
            dot.node(graphNodeId, label="và")
        ScannedNodes.append(graphNodeId)
    elif style == NodeStyle.Or:
        if not isDuplicate:
            dot.node(graphNodeId, label="hoặc")
        ScannedNodes.append(graphNodeId)
    else:
        TrialNote = ""
        if (style == NodeStyle.RootTrial):
            TrialNote = "Giả định: " + myCourse['Y'] + "| Hiện tại: "
            pass
        try: 
            graphNodeId = myCourse['Mã học phần']
            dot.node(graphNodeId, label="{" + "{id} | {name}  | {condition} | {credit}".format(
            id = myCourse['Mã học phần'],
            name=myCourse['Tên học phần'],
            condition = (str(TrialNote) + myCourse['Học phần điều kiện']) ,
            credit=myCourse['Thời lượng'] + " / " + str(myCourse['TC học phí']) + "đ / " + str(myCourse['Trọng số'])  ,
            ) + "}",
            # Bug:  nếu viết như bên dưới thì kí tự & sẽ được chuyển đổi encoding. Chưa tìm được hàm để nó đừng có encoding nua
            #     dot.node(graphNodeId, label="và", URL=BASE_URL + '?type=svg&id=' + graphNodeId)                     
            URL=BASE_URL + "?id=" + graphNodeId)       
            ScannedNodes.append(graphNodeId)
        except:
            # Ghi nhận lỗi với node có tên là "so many"
            print ("Không vẽ được với " + str(courseId))                    
    return graphNodeId, isDuplicate

def ExportDotToGraph(dot, filename):
    """
        Xuất dữ liệu trong cấu trúc dot Graphviz ra file
    """    
    try:
        # format='svg'
        dot.render(filename, view=False,format='png')
        dot.render(filename, view=False,format='svg')
    except:
        print("     error to export to file with {0}".format(myCourse['X']))
        pass    

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Khai báo thông tin phần mềm cho bộ phân tích tham số dòng lệnh
cmd_parser = argparse.ArgumentParser(
                    prog = 'Vẽ đồ thị quan hệ giữa các mã học phần',
                    description = 'Vẽ và ghép đồ thị các học phần phụ thuộc và bị phụ thuộc vào một mã học phần, dựa trên nguồn dữ liệu trong file ' + COURSE_COLLECTION_FOLDER + '/' + COURSE_LIST_FILE + '. Thư mục ảnh đầu ra là ' + OUTPUT_FOLDER,
                    epilog = 'Dữ liệu nguồn từ Đại học Bách khoa Hà Nội')
'''Bộ phân tích tham số dòng lệnh'''

# Khai báo các tham số dòng lệnh
cmd_parser.add_argument('-s','--subject', dest="hocphan", type=str.upper, help='Vẽ đồ thị cho duy nhất học phần chỉ định. Nếu bỏ qua, mặc định sinh đồ thị cho tất cả các mã học phần trong nguồn dữ liệu ' + str(COURSE_LIST_FILE),)  # Luôn tự động uppercase chuỗi kí tự nhập vào
cmd_parser.add_argument('-c','--condition', dest="dieukienthu", type=str.upper, help='Điều kiện học phần giả định. Nếu được chỉ định, sẽ thay thế cho học phần điều kiện trong cơ sở dữ liệu. Phải dùng với tham số -s kèm theo.',)  # Luôn tự động uppercase chuỗi kí tự nhập vào

cmd_parser.add_argument('-p','--programme', dest="chuongtrinh", type=str.upper, help='Vẽ đồ thị cho 1 chương trình đào tạo, gồm nhiều mã học phần trên cùng 1 đồ thị. Danh sách học phần ở dạng CSV, không có kí tự trống. Phải có tham số -n kèm theo. Ví dụ -n programme_name -p it1110,it3030,it4251')  # Luôn tự động uppercase chuỗi kí tự nhập vào
cmd_parser.add_argument('-n','--name', dest="tenchuongtrinh", type=str, help='Tên file xuất của chương trình đào tạo . Ví dụ -n sie -p it1110,it3030,it4251') 

# Phân tích tham số dòng lệnh hiện có
cmd_params = cmd_parser.parse_args()  
'''dict chứa các tham số dòng lệnh. Lấy tham số là cmd_params.thamso'''

# Kiểm tra quan hệ giữa các tham số dòng lệnh
if (cmd_params.chuongtrinh != None and cmd_params.tenchuongtrinh == None) or (cmd_params.chuongtrinh == None and cmd_params.tenchuongtrinh != None):
    print("Tham số -p và -n phải cùng xuất hiện.")
    exit(-1)
if (cmd_params.dieukienthu != None and cmd_params.hocphan == None):
    print("Tham số -c phải xuất hiện cùng tham số -s.")
    exit(-2)

# Kiểm tra luôn tham số về chương trình đào tạo nếu có
if cmd_params.chuongtrinh != None:
    Education_Programme_Courses = cmd_params.chuongtrinh.split(',')
    print("Các học phần của chương trình đào tạo: ")
    print(Education_Programme_Courses)



#Chuyển đổi đường dẫn tương đối thành tuyệt đối
COURSE_COLLECTION_FOLDER = os.getcwd() + '/../' + COURSE_COLLECTION_FOLDER
OUTPUT_FOLDER = os.getcwd() + '/../' +  OUTPUT_FOLDER

csvfile = open(COURSE_COLLECTION_FOLDER + '/' + COURSE_LIST_FILE, 'r',encoding="utf-8-sig")
'''File dữ liệu đầu vào, kết quả của quá trình crawl dữ liệu trang sis'''

reader = csv.DictReader(csvfile)
'''handler điều khiển đọc file csv'''

standardizedCourses = []; 
''' Danh sách đầy đủ các course với thông tin đã được chuẩn hoá.'''

#Bố trí lại thông tin phụ thuộc
for myCourse in reader:
    dk=str(myCourse['Học phần điều kiện']);
    dependency=dk.replace("*", "").replace(" ", "")
    
    myCourse['X']= myCourse['Mã học phần'] #Mã học phần chính, trùng lặp dữ liệu để tiện cho thuật toán tìm quan hệ
    myCourse['Y']= dependency       #Mã học phần điều kiện, trùng lặp dữ liệu để tiện cho thuật toán tìm quan hệ
    #if len(dependency) > 60:
    #    print(myCourse)
    standardizedCourses.append(myCourse)
#print(standardizedCourses[12]['HP']);

#EC = ExpressionConverter()
#print (EC.infixtodict("IT1000/CH1000/CH1001"))
#print (EC.infixtodict("(IT1000/IT1001),(CH1000/CH1001),(BB1000/BB1001)"))
#exit(0)

setHP = set()
setHP.clear();
courseIndex = 0

dot = graphviz.Digraph('G', 
                        node_attr={'shape': 'record',}, 
                        edge_attr={'len': '2.0'}
                        )
for myCourse in standardizedCourses:
    courseIndex  = courseIndex + 1;

    #Nếu có chỉ định tham số dòng lệnh vẽ đồ thị cho 1 chương trình đào tạo nào đó, thì chỉ vẽ cho duy nhất các học phần trong danh sách
    if  (cmd_params.chuongtrinh != None) and (not myCourse['X'] in Education_Programme_Courses):
        continue

    #Nếu có chỉ định tham số dòng lệnh vẽ đồ thị cho 1 học phần nào đó, thì chỉ vẽ cho duy nhất 1 học phần
    if (cmd_params.hocphan != None):
        if (myCourse['X'] != cmd_params.hocphan):
            continue
        if cmd_params.dieukienthu != None:
            # Ép buộc điều kiện thử từ tham số dòng lệnh
            myCourse['Y'] = cmd_params.dieukienthu  
             
    # Nén: các node cluster sẽ lồng vào nhau
    dot.attr(compound='true')
    
    # Đưa nút gốc, mã học phần gốc vào, với màu sắc chỉ định. Riêng trường hợp thử nghiệm học phần điều kiện giả định thì phải vẽ khác một tí để phân biệt
    # Tham khảo: https://graphviz.org/doc/info/shapes.html
    # Bỏ qua vì việc vẽ nút gốc đã nằm trong hàm findDependant rồi
    #RegisterAndRenderNode(dot, myCourse['X'], style=NodeStyle.Root)   
                

    # Chuẩn hóa dữ liệu từ file csv
    print("Vẽ đồ thị: HP " + myCourse['X']+ " --dk--> " + myCourse['Y'])
    
    # Lần theo dấu vết các cạnh là các học phần phụ thuộc
    dot.attr('node', shape='box', color='white', style='filled', fontcolor='black')     # Không hiểu sao phải thiết lập thuộc tính ở đây, nếu không thì node đại diện cho cluster sẽ kông đổi atrribute được
    dot.edge_attr.update(arrowhead='none', arrowsize='1')
    ScannedNodes.clear()
    if cmd_params.dieukienthu != None:
        rootStyle = NodeStyle.RootTrial
    else:
        rootStyle = NodeStyle.Root    
    findDependant(myCourse["X"], dot, rootStyle)
    
    # Lần theo dấu vết các cạnh là các học phần cần môn này
    #dot.attr('node', shape='box', color='#ff000042', style='filled', fontcolor='black')    
    dot.edge_attr.update(arrowhead='inv', arrowsize='1',)
    findCaller(myCourse["X"], dot, setHP)
    
    if cmd_params.chuongtrinh == None:
        #Vẽ đồ thị và làm mới đồ thị khi chỉ vẽ cây phụ thuộc cho 1 học phần riêng rẽ
        if cmd_params.dieukienthu == None:
            filename = OUTPUT_FOLDER + '/' + myCourse['X']
        else:
            filename = COURSE_COLLECTION_FOLDER + '/trial/' + myCourse['X'] + "."+ cmd_params.dieukienthu.replace("/","+").replace("\\","+")
            print(filename)
        ExportDotToGraph(dot, filename)
        dot.clear()
        setHP.clear()
    
    #Nếu có chỉ định tham số dòng lệnh vẽ đồ thị cho 1 học phần nào đó, thì vẽ xong là kết thúc luôn
    if (cmd_params.hocphan != None) and (myCourse['X'] != cmd_params.hocphan):
       break

if cmd_params.chuongtrinh != None:
    #Vẽ đồ thị cho toàn bộ chương trình đào tạo nếu có tham số dòng lệnh
    ExportDotToGraph(dot, OUTPUT_FOLDER + '/' + cmd_params.tenchuongtrinh)
    dot.clear()