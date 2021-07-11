class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack(object):
    def __init__(self):
        self.top = None
        self.size = 0
        
    def isEmpty(self):
        return self.top == None
    
    def GetSize(self):
        return self.size
    
    def push(self, data):
        new = Node(data)
        if (self.isEmpty()):
            self.top = new
        else:
            new.next = self.top
            self.top = new
            
        self.size += 1
        
    def pop(self):
        if (not self.isEmpty()):
            delete = self.top
            if (self.size == 1):
                self.top = None
            else:
                self.top = delete.next
            self.size -= 1
            return delete.data
        
        return -1
    
    def peek(self):
        if (not self.isEmpty()):
            return self.top.data
        
        return None