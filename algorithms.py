### Linear Search Algorithm

### Test Data Set

test_request_ids = [1000, 1001, 1010, 1011, 1110, 1002, 1005, 4501, 1004, 3105, 1007, 4532, 1009]
test_priority = [1, 3, 4, 1, 2, 3, 4, 1, 3, 2, 4, 1, 2]
def linear_search(request_id, position):
    for i in range(len(request_id)):
        if request_id[i] == position:
            return i
    return None

### Testing the linear search function

linear_search_result = linear_search(test_request_ids, 1005)
print(linear_search_result)

###

### Binary Search Algorithm

class OrderedArray(object):
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
                hi = mid - 1
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

### Testing the binary search function

binary_search_result = Binary_search(test_request_ids, 1005)
print(binary_search_result)

###

### Insertion Sort Algorithm

def insertion_sort(priority, request_id):
    copy = priority.copy()
    for i in range(1, len(request_id)):
        key = copy[i]
        j = i - 1
        while j >= 0 and copy[j] > key:
            copy[j + 1] = copy[j]
            j -= 1
        copy[j + 1] = key
    return copy

### Merge Sort Algorithm

def merge_sort(request_id, low, high):
    if low >= high:
        return request_id

    mid = (low + high) // 2
    merge_sort(request_id, low, mid)
    merge_sort(request_id, mid + 1, high)

    left = request_id[low:mid + 1]
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

    while i < len(left):
        request_id[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        request_id[k] = right[j]
        j += 1
        k += 1

    return request_id

### Check sorting algorithms

insertion_sort_result = insertion_sort(test_priority, test_request_ids)
print(insertion_sort_result)

merge_sort_result = merge_sort(test_request_ids, 0, len(test_request_ids) - 1)
print(merge_sort_result)