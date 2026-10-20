
# DTSC-5501_Campus_Maintainance_Request_Manager_Group_7

Members: Joseph Gentile (joge13030) and Timothy Williams (tiwi6506)

Instructions: To use this package you must run commands via a directory attached to the project or directly create run the project.

### Run the following commands:

``` python  -m unitest -v test_projects ```

``` python algorithms.py ```

In order to use the requests directly you can also use the following:

```python
from maintainence_request import MaintainenceRequest
from array_request_list import ArrayRequestList
from linked_request_list import LinkedRequestList

request = MaintainenceRequest(
    ### value data
)
requests = ArrayRequestList(10)  # Or LinkedRequestList()
requests.append(request)

### here you can print the operations you want to have conducted

removed = requests.removeAt(0)
```

### Design choices

By defining our own `ArrayList` and `LinkedList` classes we used tuple records instead of `MaintainenceRequest` objects which made it easier to append metadata into our `LinkedRequestList` but sacrificed the better time complexity from $O(1)$ to $O(n)$. We did this because we figured that the complexity change does _not_ reflect a significant real time change.

Our array list used direct indexing for a fast `getAt` method which can help make appending faster and more efficient.

The linked lists, naturally, store data within nodes. We attempted to make all operations which could be used in our linked list have similar time complexity, which resulted in relying heavily on traversal methods.

### Package documents

1) `maintainence_request.py`
2) `design_review.md`
3) `workload.py`
4) `array_request_list.py`
5) `linked_request_list.py`
6) `algorithms.py`
7) `test_projects.py`
8) `analysis.ipynb`
9) `README.md`