class Node:
    def __init__(self, request):
        self.data = request
        self.next = None


class LinkedRequestList:
    def __init__(self):
        self.head = None

    def push(self, request):
        #Checks for dups
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate Id")
        #new node create and add it to front with push
        newNode = Node(request)
        newNode.next = self.head
        self.head = newNode

    def append(self, request):
        #dups?
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate id")

        newNode = Node(request)
        #cheks if empty to make sure we can move thorugh a node
        if self.head is None:
            self.head = newNode
            return
        else:
            current = self.head
        #last node
        while current.next is not None:
            current = current.next
        #adds to end
        current.next = newNode

    def count(self):
        #counts all nodes starting from 0 and loop while adding to total
        total = 0
        current = self.head

        while current is not None:
            total += 1
            current = current.next

        return total

    def findById(self, request_id):
        #start at first node
        current = self.head
        #loop while there are nodes and checks that id exists in requests to match
        while current is not None:
            if current.data.request_id == request_id:
                return current.data
            current = current.next

        return None

    def getAt(self, index):
        #typerror for index not being a number
        if type(index) != int:
            raise TypeError("Index not int")
        #starts at first node index 0 
        current = self.head
        i = 0
        #loop till the index we are looking for is matched
        while current is not None:
            if i == index:
                return current.data
            current = current.next
            #used to move by each node 
            i += 1
        #need if index doesnt exist 
        raise IndexError("Index not found")

    def insertAt(self, index, request):
        #index error required
        if type(index) != int:
            raise TypeError("Index not int")

        if index < 0 or index > self.count():
            raise IndexError("Index rnage error")

        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")

        newNode = Node(request)

        if index == 0:
            #new first node if inserted at start 
            newNode.next = self.head
            self.head = newNode
            return
        #finds first node 
        current = self.head
        #loops and stops at index beore the one we want 
        for i in range(index - 1):
            current = current.next

        newNode.next = current.next
        current.next = newNode

    def removeAt(self, index):
        if type(index) != int:
            raise TypeError("Index not int")
        #avoids negative int
        if index < 0:
            raise IndexError("Index out of range")
        #if forst index is removed removes fist node
        if index == 0:
            # if head is none the list is empty
            if self.head is None:
                raise IndexError("List empty")
            #we need to be able to return what we removed and move the node
            removed = self.head.data
            self.head = self.head.next
            return removed

        current = self.head
        
        #stops before index we want to remove so we can remove and move them
        for i in range (index - 1):
            current = current.next

        if current is None or current.next is None:
            raise IndexError("Index missing")
        #saves the removed variable 
        removed = current.next.data
        current.next = current.next.next

        return removed

    def __str__(self):
        #new list to hold string
        result = ""
        current = self.head
        # keep going while there are nodes, makes data strings and adds
        while current is not None:
            result += str(current.data) + " - "
            current = current.next

        return "Head" + result + "None"
