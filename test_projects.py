"""Reproducible operation tests for the campus maintenance request lists.
"""


import unittest
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
