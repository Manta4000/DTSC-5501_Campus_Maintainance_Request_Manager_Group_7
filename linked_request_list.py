class Node:
    def __init__(self, request):
        self.data = request
        self.next = None

class LinkedRequestList:
    def __init__(self):
        self.head = None

    def append(self, request)
