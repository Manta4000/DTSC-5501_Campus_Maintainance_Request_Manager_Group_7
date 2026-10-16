### Linear Search Algorithm

def linear_search(request_id, position):
    for i in range(len(request_id)):
        if request_id[i] == position:
            return i
        else:
            return None
    return None

### Binary Search Algorithm

class OrderedArray(request_id):
    def __init__(self, initialSize):
        self.__a = [None] * initialSize
        self.__nItems = 0

    def find(self, item):
        lo = 0
        hi = self.__nItems - 1

        while lo <= hi:
            mid = (lo + hi) // 2
            if self.__a[mid] == item:
                return mid
            elif self.__a[mid] < item:
                lo = mid + 1
            else:
                hi = mid -1
        return lo

def Binary_search(request_id, position):
    lo = 0
    hi = len(request_id) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if request_id[mid] == position:
            return mid
        elif request_id[mid] < position:
            lo = mid + 1
        else:
            hi = mid - 1
    return None



### Insertion Sort Algorithm

def insertion_sort(self, priority, request_id):
    self.copy = request_id.copy(), priority.copy()
    for i in range(1, len(request_id)):
        key = self.copy[i]
        j = i - 1
        while j >= 0 and self.copy[j] > key:
            self.copy[j + 1] = self.copy[j]
            j -= 1
        self.copy[j + 1] = key
    return self.copy

### Merge Sort Algorithm

def mrge_sort(self, request_id, low, mid, high):
    left = request_id[low:mid +1]
    right = request_id[mid + 1:high + 1]
    i = 0
    j = 0
    k = low
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            request_id[k] = left[i]
            i += 1
        else:
            request_id[k] = right[j]
            j += 1
        k += 1
