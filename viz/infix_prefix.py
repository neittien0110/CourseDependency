class infix_to_prefix:
    """
        Chuyển đổi biểu thức trung tố --> tiền tố
        Yêu cầu: mọi toán hạng đều gồm 6 kí tự số và chữ.
    """    
    precedence={'/':6,',':5,'=':4,'!':3,'(':2,')':1}
    precedence={'^':5,'*':4,'/':4,'+':3,'-':3,'(':2,')':1}
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
    
    def infixtoprefix (self,expression):
        expr = self.reverse(expression)
        prefix=""
        index = 0
        while index < len(expr):
            ch = expr[index]
            if(self.is0perand(ch)):
                # Đưa toán hạng vào ngăn xếp
                prefix +=expr[index:index+6]
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
        backup_items = self.items
        while len(self.items):
            if(self.seek()=='('):
                self.pop()
            else:
                prefix+=self.pop()
        return self.reverse(prefix), backup_items