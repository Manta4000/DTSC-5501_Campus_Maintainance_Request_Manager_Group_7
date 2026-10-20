"""Reproducible operation tests for the campus maintenance request lists.
"""

### Prediction
### At n=25,000 vs. 5,000: constant-time operations should be about 1x; linear about 5x; quadratic about 25x.
### Arrays should win middle reads/search; linked lists should win front edits. Part K is append-heavy, so predict array wins.
### More front insertions/removals could shift the workload toward linked lists.

import unittest
import time
from types import SimpleNamespace

from array_request_list import ArrayRequestList
from linked_request_list import LinkedRequestList


BUILDINGS = ("CASE", "ECNW", "ECCR", "AERO", "ATLAS", "NORLIN")


def make_request(request_id, building_index=0):
    """Return a deterministic maintenance-request-shaped object."""
    return SimpleNamespace(
        request_id=request_id,
        building=BUILDINGS[building_index % len(BUILDINGS)],
        category="HVAC",
        priority=3,
        reported_time="2026-10-19T09:00:00",
        status="Open",
    )


class RequestListContractTests:
    list_factory = None

    def make_list(self):
        return self.list_factory()

    def assert_ids(self, request_list, expected_ids):
        self.assertEqual(request_list.count(), len(expected_ids))
        self.assertEqual(
            [request_list.getAt(index).request_id for index in range(len(expected_ids))],
            expected_ids,
        )

    def test_empty_and_single_and_two_requests(self):
        requests = self.make_list()
        self.assertEqual(requests.count(), 0)
        self.assertIsNone(requests.findById(999))
        with self.assertRaises(IndexError):
            requests.getAt(0)
        with self.assertRaises(IndexError):
            requests.removeAt(0)

        first = make_request(100, 0)
        requests.append(first)
        self.assertEqual(requests.count(), 1)
        self.assertIs(requests.getAt(0), first)

        second = make_request(101, 1)
        requests.append(second)
        self.assertEqual(requests.count(), 2)
        self.assertIs(requests.getAt(1), second)
        self.assertIs(requests.findById(100), first)
        self.assertIsNone(requests.findById(404))

    def test_push_adds_at_the_beginning(self):
        requests = self.make_list()
        existing = make_request(150, 1)
        pushed = make_request(149, 0)
        requests.append(existing)

        requests.push(pushed)
        self.assert_ids(requests, [149, 150])
        self.assertIs(requests.getAt(0), pushed)

    def test_insert_at_beginning_middle_and_end(self):
        requests = self.make_list()
        middle = make_request(201, 1)
        end = make_request(202, 2)
        beginning = make_request(200, 0)
        requests.append(middle)
        requests.append(end)

        requests.insertAt(0, beginning)
        requests.insertAt(2, make_request(203, 3))
        requests.insertAt(requests.count(), make_request(204, 4))
        self.assert_ids(requests, [200, 201, 203, 202, 204])

    def test_remove_at_beginning_middle_and_end_returns_removed_item(self):
        requests = self.make_list()
        for request_id in (300, 301, 302, 303, 304):
            requests.append(make_request(request_id, request_id))

        self.assertEqual(requests.removeAt(0).request_id, 300)
        self.assertEqual(requests.removeAt(1).request_id, 302)
        self.assertEqual(requests.removeAt(requests.count() - 1).request_id, 304)
        self.assert_ids(requests, [301, 303])

    def test_duplicate_request_id_is_rejected(self):
        requests = self.make_list()
        requests.append(make_request(400))
        for operation in (
            lambda: requests.push(make_request(400, 1)),
            lambda: requests.append(make_request(400, 2)),
            lambda: requests.insertAt(0, make_request(400, 3)),
        ):
            with self.assertRaises(ValueError):
                operation()
        self.assert_ids(requests, [400])

    def test_invalid_indexes_are_rejected(self):
        requests = self.make_list()
        requests.append(make_request(500))

        for index in (-1, 1):
            with self.subTest(index=index):
                with self.assertRaises(IndexError):
                    requests.getAt(index)
                with self.assertRaises(IndexError):
                    requests.removeAt(index)
        for index in (-1, 2):
            with self.subTest(insert_index=index):
                with self.assertRaises(IndexError):
                    requests.insertAt(index, make_request(501))

        for index in (1.5, "0", True):
            with self.subTest(noninteger_index=index):
                with self.assertRaises(TypeError):
                    requests.getAt(index)
                with self.assertRaises(TypeError):
                    requests.removeAt(index)
                with self.assertRaises(TypeError):
                    requests.insertAt(index, make_request(502))


class ArrayRequestListTests(RequestListContractTests, unittest.TestCase):
    list_factory = staticmethod(lambda: ArrayRequestList(2))

    def test_array_resizes_and_preserves_order(self):
        requests = self.make_list()
        for request_id in range(600, 605):
            requests.append(make_request(request_id, request_id))

        self.assertGreaterEqual(requests.capacity, 5)
        self.assert_ids(requests, [600, 601, 602, 603, 604])

    def test_zero_capacity_array_grows_on_first_insert(self):
        requests = ArrayRequestList(0)
        first = make_request(650)

        requests.append(first)
        self.assertGreaterEqual(requests.capacity, 1)
        self.assertIs(requests.getAt(0), first)


class LinkedRequestListTests(RequestListContractTests, unittest.TestCase):
    list_factory = staticmethod(LinkedRequestList)


### Part G -- Performance Testing

PART_G_SIZES = (1000, 5000, 10000, 25000)

def request_id_for(order, index, size, multiplier):
    if order == "sorted":
        return index
    if order == "reverse sorted":
        return size - index
    return 100000 + ((index * multiplier + 17) % size)


def coprime_multiplier(size):
    candidate = size - 1
    while candidate > 1:
        left = candidate
        right = size
        while right:
            left, right = right, left % right
        if left == 1:
            return candidate
        candidate -= 1
    return 1

def make_benchmark_collection(collection_type, size, order="sorted"):
    multiplier = coprime_multiplier(size)
    if collection_type is ArrayRequestList:
        collection = ArrayRequestList(size + 1)
        for index in range(size):
            request_id = request_id_for(order, index, size, multiplier)
            collection.data[index] = make_request(request_id, index)
        collection.size = size
        return collection

    collection = LinkedRequestList()
    node_type = None
    tail = None
    for index in range(size):
        request_id = request_id_for(order, index, size, multiplier)
        request = make_request(request_id, index)
        if node_type is None:
            collection.push(request)
            node_type = type(collection.head)
            tail = collection.head
        else:
            tail.next = node_type(request)
            tail = tail.next
    return collection

def measured_seconds(operation):
    start = time.perf_counter()
    operation()
    return time.perf_counter() - start


def linear_search(collection, target):
    if isinstance(collection, ArrayRequestList):
        for index in range(collection.size):
            request = collection.data[index]
            if request.request_id == target:
                return request
        return None

    current = collection.head
    while current is not None:
        if current.data.request_id == target:
            return current.data
        current = current.next
    return None


def binary_search(collection, target):
    low = 0
    high = collection.count() - 1
    while low <= high:
        middle = (low + high) // 2
        request = collection.getAt(middle)
        if request.request_id == target:
            return request
        if request.request_id < target:
            low = middle + 1
        else:
            high = middle - 1
    return None


def insertion_sort_array(collection):
    for index in range(1, collection.size):
        request = collection.data[index]
        position = index - 1
        while position >= 0 and collection.data[position].request_id > request.request_id:
            collection.data[position + 1] = collection.data[position]
            position -= 1
        collection.data[position + 1] = request


def insertion_sort_linked(collection):
    current = collection.head
    sorted_head = None
    while current is not None:
        following = current.next
        if sorted_head is None or sorted_head.data.request_id >= current.data.request_id:
            current.next = sorted_head
            sorted_head = current
        else:
            position = sorted_head
            while position.next is not None and position.next.data.request_id < current.data.request_id:
                position = position.next
            current.next = position.next
            position.next = current
        current = following
    collection.head = sorted_head


def report_operation(size, collection_name, operation_name, operation):
    elapsed = measured_seconds(operation)
    print(f"{size:>6} | {collection_name:<7} | {operation_name:<34} | {elapsed:.9f} s")


def benchmark_collection_operations(size, collection_type, collection_name):
    middle = size // 2
    missing_id = -1
    operation_cases = (
        ("read middle element", lambda collection: collection.getAt(middle)),
        ("insert at beginning", lambda collection: collection.insertAt(0, make_request(size + 1))),
        ("append", lambda collection: collection.append(make_request(size + 2))),
        ("insert in middle", lambda collection: collection.insertAt(middle, make_request(size + 3))),
        ("remove from beginning", lambda collection: collection.removeAt(0)),
        ("remove from middle", lambda collection: collection.removeAt(middle)),
        ("search for missing ID", lambda collection: collection.findById(missing_id)),
        ("linear search for missing ID", lambda collection: linear_search(collection, missing_id)),
        ("binary search for missing ID", lambda collection: binary_search(collection, missing_id)),
    )
    for operation_name, operation in operation_cases:
        collection = make_benchmark_collection(collection_type, size)
        report_operation(size, collection_name, operation_name, lambda: operation(collection))


def benchmark_insertion_sorts(size, collection_type, collection_name):
    for order in ("sorted", "reverse sorted", "random"):
        collection = make_benchmark_collection(collection_type, size, order)
        sorter = insertion_sort_array if collection_type is ArrayRequestList else insertion_sort_linked
        report_operation(
            size,
            collection_name,
            f"insertion sort ({order})",
            lambda: sorter(collection),
        )


def run_part_g():
    print("Part G performance results (single timed operation; setup excluded)")
    print("Array mutation tests reserve one free slot to avoid timing a resize.")
    print("     n | list    | operation                          | elapsed")
    print("-------+---------+------------------------------------+----------------")
    for size in PART_G_SIZES:
        for collection_type, collection_name in (
            (ArrayRequestList, "array"),
            (LinkedRequestList, "linked"),
        ):
            benchmark_collection_operations(size, collection_type, collection_name)
            benchmark_insertion_sorts(size, collection_type, collection_name)


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
    run_part_g()
