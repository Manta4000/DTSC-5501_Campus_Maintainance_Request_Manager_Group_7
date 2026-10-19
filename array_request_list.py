class ArrayRequestList:
    def __init__(self, capacity):
        self.data = [None] * capacity
        self.size = 0
        self.capacity = capacity

    def push(self, request):
        #dups?
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")
        #ran out of space, resize when size = cap
        if self.size == self.capacity:
            self.resize()
        #countbackwards to shift and overwrite/copies
        for i in range(self.size, 0, -1):
            self.data[i] = self.data[i - 1]

        self.data[0] = request
        self.size += 1

    def resize(self):
        #make new capacity 2 times more
        newCapacity = self.capacity * 2 
        newData = [None] * newCapacity
        #for loop and copies to new set
        for i in range(self.size):
            newData[i] = self.data[i]

        self.data = newData
        self.capacity = newCapacity

    def count(self):
        return self.size

    def findById(self, request_id):
        #loop to match id we are looking for to one in set
        for i in range(self.size):
            if self.data[i].request_id == request_id:
                return self.data[i]
        return None

    def append(self, request):
        #dups
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")
        #more space if needed 
        if self.size == self.capacity:
            self.resize()
        #adds more space if needed 
        self.data[self.size] = request
        self.size += 1

    def inserAt(self, index, request):
        #checks if index is not negative or too big 
        if index < 0 or index > self.size:
            #is index valid?
            raise IndexError("Index Error")
        #dups?
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate id")
        #more room if needed
        if self.size == self.capacity:
            self.resize()
        #shift to right
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        
        self.data[index] = request
        self.size += 1

    def inserAt(self, index, request):
        return self.insertAt(index, request)

    def removeAt(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")
        #what was removed to be recalled 
        removed = self.data[index]
        #left shift
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        
        # once shift removes last copy 
        self.data[self.size - 1] = None
        self.size -= 1
        return removed

        return removed

    def getAt(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index Error")
        return self.data
