class ArrayRequestList:
    def __init__(self, capacity):
        #capacity management
        self.data = [None] * capacity
        self.size = 0 
        self.capacity = capacity
    def push(self, request):
        #checks for duplicates before pushing a new request
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")
        if self.size == self.capacity:
            self.resize()
        i = self.size
        while i > 0:
            self.data[i] = self.data[i - 1]
            i -=1
        self.data[0] = request
        self.size += 1


    def resize(self):
        #make new capacity 2 times more
        newCapacity = self.capacity * 2 
        newData = [None] * newCapacity
        #loop for everything in array and copy over data when resizeing 
        for i in range(self.size):
            newData[i] = self.data[i]
        #set the new data
        self.data = newData
        self.capacity = newCapacity
    def count(self):
        return self.size
    
    def findById(self, request_id):
        #makes the code go through entire set
        for i in range(self.size):
            #using the current array and its index pull and match the id from request_id
            if self.data[i].request_id == request_id:
                return self.data[i]
        return None
    
    def append(self, request):
        if self.findById(request.request_id) is not None:
            raise ValueError("Value Error")

        if self.size == self.capacity:
            self.resize()

        self.data[self.size] = request
        self.size += 1

    def inserAt(self, index, request):

    def removeAt(self):

    def getAt(self):
