class Node:
    def __init__(self, request):
        self.data = request
        self.next = None


class LinkedRequestList:
    def __init__(self):
        self.head = None

    def push(self, request):
        #duplicate check
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")

        newNode = Node(request)
        newNode.next = self.head
        self.head = newNode

    def append(self, request):
        #duplciate check 
        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")

        newNode = Node(request)

        if self.head is None:
            self.head = newNode
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = newNode

    def count(self):
        total = 0
        current = self.head

        while current is not None:
            total += 1
            current = current.next

        return total

    def findById(self, request_id):
        current = self.head

        while current is not None:
            if current.data.request_id == request_id:
                return current.data
            current = current.next

        return None

    def getAt(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")

        if index < 0:
            raise IndexError("Index out of range")

        current = self.head
        i = 0

        while current is not None:
            if i == index:
                return current.data

            current = current.next
            i += 1

        raise IndexError("Index out of range")

    def insertAt(self, index, request):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")

        if index < 0 or index > self.count():
            raise IndexError("Index out of range")

        if self.findById(request.request_id) is not None:
            raise ValueError("Duplicate ID")

        if index == 0:
            self.push(request)
            return

        newNode = Node(request)
        current = self.head
        i = 0

        while i < index - 1:
            current = current.next
            i += 1

        newNode.next = current.next
        current.next = newNode

    def removeAt(self, index):
        if not isinstance(index, int) or isinstance(index, bool):
            raise TypeError("Index must be an integer")

        if index < 0:
            raise IndexError("Index out of range")

        if index == 0:
            if self.head is None:
                raise IndexError("Index out of range")

            removed = self.head.data
            self.head = self.head.next
            return removed

        current = self.head
        i = 0

        while current is not None and i < index - 1:
            current = current.next
            i += 1

        if current is None or current.next is None:
            raise IndexError("Index out of range")

        removed = current.next.data
        current.next = current.next.next

        return removed

    def __str__(self):
        result = ""
        current = self.head

        while current is not None:
            result += str(current.data) + " -> "
            current = current.next

        result += "None"
        return result
