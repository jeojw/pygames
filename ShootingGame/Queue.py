class Node(object):
    def __init__(self, data):
        self.data = data
        self.link = None

class Queue(object):
    def __init__(self):
        self.tail = None
        self.length = 0
        
    def isEmpty(self):
        return self.tail is None and self.length == 0
    
    def size(self):
        return self.length
    
    def enqueue(self, data):
        newNode = Node(data)
        if (self.isEmpty()):
            newNode.link = newNode
            self.tail = newNode
        else:
            newNode.link = self.tail.link
            self.tail.link = newNode
            self.tail = newNode
            
        self.length += 1
            
    def dequeue(self):
        if (not self.isEmpty()):
            if (self.length == 1):
                deleteNode = self.tail
                deleteNode = self.tail.link
                self.tail = None
            else:
                deleteNode = self.tail.link
                self.tail.link = deleteNode.link
                
            self.length -= 1
            return deleteNode.data
        
    def peek(self):
        if (not self.isEmpty()):
            return self.tail.data
        
    def display(self):
        node = self.tail.link
        while (node != self.tail):
            print(node.data, end=' ')
            node = node.link
        print(node.data, end=' ')
        print('size:', self.length)
        