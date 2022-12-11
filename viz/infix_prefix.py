import json

class ExpressionConverter:
    """
        Chuyển đổi biểu thức trung tố --> tiền tố
        Yêu cầu: mọi toán hạng đều gồm 6 kí tự số và chữ.
    """    
    precedence={'/':6,',':5,'=':4,'!':3,'(':2,')':1}
    #precedence={'^':5,'*':4,'/':4,'+':3,'-':3,'(':2,')':1}
    ''' Danh sách các toán tử'''
    def __init__(self):
        self.items=[]
        self.size=-1
    def push(self,value):
        self.items.append(value)
        self.size+=1
    def pop(self):
        if self.isempty():
            return 0
        else:
            self.size-=1
            return self.items.pop()
    def isempty(self):
        if(self.size==-1):
            return True
        else:
            return False
    def seek(self):
        if self.isempty():
            return False
        else:
            return self.items[self.size]
    def is0perand(self,i):
        if i in self.precedence:
            return False
        else:
            return True
    def reverse(self,expr):
        rev=""
        index = 0
        while index < len(expr):
            ch = expr[index]
            if ch == '(':
                ch=')'
            elif ch == ')':
                ch='('
            if self.is0perand(ch):
                rev=expr[index:index+6]+rev
                index = index + 6
            else:       
                rev=ch+rev
                index = index + 1
        return rev
    
    def infixtoprefix (self,expression, isPrefix = True):
        """_summary_
            Chuyển đổi biểu thức trung tố thành biểu thức tiền tố/hậu tố
        Args:
            expression (string): biểu thức trung tố. Ví dụ (IT1000/IT1001),(CH1000/CH1001),(BB1000/BB1001)
            isPrefix (bool): là biểu thức tiền tố (True), hoặc ngược lại là hậu tố (False)
        Returns:
            string: biểu thức tiền tố/hậu tố.
        """
                
        expr = self.reverse(expression)
        prefix=""
        index = 0
        while index < len(expr):
            ch = expr[index]
            if(self.is0perand(ch)):
                # Đưa toán hạng vào ngăn xếp
                operand = expr[index:index+6] 
                prefix +=operand
                index = index + 5 # sẽ +1 sau
            elif ch == '(':
                # Đưa ngoặc vào ngăn xếp
                self.push(ch)
            elif ch == ')':
                o=self.pop()
                while o!='(':
                    prefix +=o
                    o=self.pop()
            elif(ch in self.precedence):  # tất nhiên đã loại 2 dấu ngoặc ra rồi
                while(len(self.items)and self.precedence[ch] < self.precedence[self.seek()]):
                    prefix+=self.pop()
                self.push(ch)
            index = index + 1
        #end of while
        while len(self.items):
            if(self.seek()=='('):
                self.pop()
            else:
                prefix+=self.pop()
        if isPrefix:
            # Trả về dạng tiền tố
            return self.reverse(prefix)
        else:
            # Trả về dạng hậu tố
            return prefix
        
    def infixtodict (self,expression):
        """_summary_
            Chuyển đổi biểu thức trung tố thành cấu trúc python dictionary
        Args:
            expression (string): biểu thức trung tố. Ví dụ (IT1000/IT1001),(CH1000/CH1001),(BB1000/BB1001)
        Returns:
            dict: thể hiển biểu thức. {"operator":"/","operands":[]}. Ví dụ {'operator': ',', 'operands': [{'operator': '/', 'operands': ['IT1000', 'IT1001']}, {'operator': '/', 'operands': ['CH1000', 'CH1001']}, {'operator': '/', 'operands': ['BB1000', 'BB1001']}]}
        """
        #return {"operator":"/","operand":["CH1123",{"operator":",","operand":["ABC","CDE"]}]}
        expr = self.reverse(expression)
        index = 0
        operands=[]
        while index < len(expr):
            ch = expr[index]
            if(self.is0perand(ch)):
                # Đưa toán hạng vào ngăn xếp
                operand = expr[index:index+6] 
                operands.append(operand)
                index = index + 5 # sẽ +1 sau
            elif ch == '(':
                # Đưa ngoặc vào ngăn xếp
                self.push(ch)
            elif ch == ')':
                pre_o = ""
                o=self.pop()
                while o!='(':
                    #Sử dụng ghép một loạt phép toán hạng của các toán tử giống nhau
                    if pre_o != o:
                        # Nếu 2 toán hạng liên tiếp khác nhau thì cứ tạo biểu thức 2 toán hạng
                        littlejson = {"operator":o,"operands":[operands.pop(),operands.pop()]}
                        operands.append(littlejson)
                    else:
                        #Lấy toán hạng phức hợp trước ra khỏi hàng đợi
                        prejson = operands.pop()
                        #Mở rộng toán hạng phức hợp với toán hạng trước đó
                        prejson["operands"].append(operands.pop())
                        #Và đẩy trở lại vào danh sách toán hạng
                        operands.append(prejson)
                    pre_o = o;                        
                    o=self.pop()
            elif(ch in self.precedence):  # tất nhiên đã loại 2 dấu ngoặc ra rồi
                while(len(self.items)and self.precedence[ch] < self.precedence[self.seek()]):
                    self.pop()
                self.push(ch)
            index = index + 1
        #end of while
        
        pre_o = ""
        while len(self.items):
            if(self.seek()=='('):
                self.pop()
            else:
                #Sử dụng ghép một loạt phép toán hạng của các toán tử giống nhau
                o=self.pop()           
                if pre_o != o:
                    # Nếu 2 toán hạng liên tiếp khác nhau thì cứ tạo biểu thức 2 toán hạng
                    littlejson = {"operator":o,"operands":[operands.pop(),operands.pop()]}
                    operands.append(littlejson)
                else:
                    #Lấy toán hạng phức hợp trước ra khỏi hàng đợi
                    prejson = operands.pop()
                    #Mở rộng toán hạng phức hợp với toán hạng trước đó
                    prejson["operands"].append(operands.pop())
                    #Và đẩy trở lại vào danh sách toán hạng
                    operands.append(prejson)
                pre_o = o;
        return operands.pop()
    

