### Linear Search Algorithm

### Test Data Set

test_request_ids = [1000, 1001, 1010, 1011, 1110, 1002, 1005, 4501, 1004, 3105, 1007, 4532, 1009]
test_priority = [1, 3, 4, 1, 2, 3, 4, 1, 3, 2, 4, 1, 2]

# Check each value in order because this search also works on unsorted data.
def linear_search(request_id, position):
    # Visit every valid list index until the target is found.
    for i in range(len(request_id)):
        if request_id[i] == position:
            # Return the matching index, not the stored value.
            return i
    # Use None consistently when no match exists.
    return None

### Testing the linear search function

linear_search_result = linear_search(test_request_ids, 1005)
print(linear_search_result)

###

### Binary Search Algorithm

# Store ordered values in a fixed-capacity array.
class OrderedArray(object):
    def __init__(self, initialSize):
        # Reserve storage and begin with no inserted values.
        self.__a = [None] * initialSize
        self.__nItems = 0

    # Find an item or its sorted insertion position.
    def find(self, item):
        # Search only the occupied range.
        lo = 0
        hi = self.__nItems - 1

        # Halve the remaining search range each iteration.
        while lo <= hi:
            mid = (lo + hi) // 2
            if self.__a[mid] == item:
                return mid
            elif self.__a[mid] < item:
                # The target can only be in the upper half.
                lo = mid + 1
            else:
                # The target can only be in the lower half.
                hi = mid - 1
        # lo marks where the item belongs to keep values ordered.
        return lo

# Binary search returns an index, and requires sorted input.
def Binary_search(request_id, position):
    # Start with the full list as the candidate range.
    lo = 0
    hi = len(request_id) - 1

    # Discard half the range after each comparison.
    while lo <= hi:
        mid = (lo + hi) // 2
        if request_id[mid] == position:
            return mid
        elif request_id[mid] < position:
            # Search the portion above the midpoint.
            lo = mid + 1
        else:
            # Search the portion below the midpoint.
            hi = mid - 1
    # Return None when the target is absent.
    return None

### Testing the binary search function

binary_search_result = Binary_search(test_request_ids, 1005)
print(binary_search_result)

###

### Insertion Sort Algorithm

# Sort a copy so the original priority list remains unchanged.
def insertion_sort(priority, request_id):
    copy = priority.copy()
    # Grow a sorted prefix from left to right.
    for i in range(1, len(request_id)):
        key = copy[i]
        j = i - 1
        # Shift larger values right to make room for the current value.
        while j >= 0 and copy[j] > key:
            copy[j + 1] = copy[j]
            j -= 1
        # Place the current value at its sorted position.
        copy[j + 1] = key
    # Return the sorted copy to the caller.
    return copy

### Merge Sort Algorithm

# Sort request_id in place by recursively sorting and merging halves.
def merge_sort(request_id, low, high):
    # A range of zero or one item is already sorted.
    if low >= high:
        return request_id

    # Divide the current range into two smaller ranges.
    mid = (low + high) // 2
    # Sort each half before merging them.
    merge_sort(request_id, low, mid)
    merge_sort(request_id, mid + 1, high)

    # Copy each half so values can be merged safely in place.
    left = request_id[low:mid + 1]
    right = request_id[mid + 1:high + 1]
    # Track positions in the left half, right half, and output.
    i = 0
    j = 0
    k = low
    # Repeatedly copy the smaller next value into the original list.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            request_id[k] = left[i]
            i += 1
        else:
            request_id[k] = right[j]
            j += 1
        k += 1

    # Copy any values remaining in the left half.
    while i < len(left):
        request_id[k] = left[i]
        i += 1
        k += 1

    # Copy any values remaining in the right half.
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