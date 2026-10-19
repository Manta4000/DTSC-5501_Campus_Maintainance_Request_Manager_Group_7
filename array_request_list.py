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
        newCapacity = max(1, self.capacity * 2)
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

    def insertAt(self, index, request):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")
        #checks if index is not negative or too big 
        if index < 0 or index > self.size:
            raise IndexError("Index Error")
        #check for duplicates 
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate Id")
        #will check and resize if used storgae is equal to capacity
        if self.size == self.capacity:
            self.resize()

        i = self.size
        #shifting to the right by one when inserting 
        while i > index:
            self.data[i] = self.data[i - 1]
            i-=1
        self.data[index] = request
        self.size += 1

    def inserAt(self, index, request):
        return self.insertAt(index, request)

    def removeAt(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")
        removed = self.data[index]

        i = index

        while i < self.size - 1:
            self.data[i] = self.data[i+1]
            i += 1
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

    def getAt(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")
        return self.data[index]
