### Seeded workload replay for comparing the campus request-list structures.
### Profile A: 80% append, 10% find, 5% indexed read, 5% indexed removal.
### Append dominates. The array is expected to win because both lists scan to
### reject duplicate IDs, while linked append also traverses to the tail. A mix
### with frequent front removals/insertions could favor linked storage instead.

import random
import time

from array_request_list import ArrayRequestList
from linked_request_list import LinkedRequestList, Node


n_0 = 10_000
OPERATION_COUNT = 20_000
RUN_COUNT = 5
buildings = ("CASE", "ECNW", "ECCR", "AERO", "ATLAS", "NORLIN")


class WorkloadRequest:
	def __init__(self, request_id):
		self.request_id = request_id
		self.building = buildings[request_id % len(buildings)]
		self.category = "HVAC"
		self.priority = 3
		self.reported_time = "2026-10-19 09:00"
		self.status = "Open"


def generate_operations(seed, initial_size=n_0, count=OPERATION_COUNT):
	### Generate a fixed operation sequence and simulate its IDs for valid indexes.
	rng = random.Random(seed)
	active_ids = list(range(initial_size))
	next_id = initial_size
	operations = []

	for _ in range(count):
		choice = rng.random()
		if choice < 0.80: ### pretty much always append, but sometimes remove to keep the list from growing too large
			operations.append(("append", next_id))
			active_ids.append(next_id)
			next_id += 1
		elif choice < 0.90:
			if rng.random() < 0.80:
				operations.append(("find", active_ids[rng.randrange(len(active_ids))]))
			else:
				operations.append(("find", -1 - rng.randrange(count)))
		elif choice < 0.95:
			operations.append(("get", rng.randrange(len(active_ids))))
		else:
			index = rng.randrange(len(active_ids))
			operations.append(("remove", index))
			active_ids.pop(index)

	return operations


def build_collection(kind, initial_size):
	### Build the same initial IDs without timing setup or duplicate checks.
	if kind == "array":
		collection = ArrayRequestList(initial_size)
		collection.data = [WorkloadRequest(i) for i in range(initial_size)]
		collection.size = initial_size
		return collection

	collection = LinkedRequestList()
	tail = None
	for request_id in range(initial_size): ### this is to avoid the duplicate check in push/append
		node = Node(WorkloadRequest(request_id))
		if tail is None:
			collection.head = node
		else:
			tail.next = node
		tail = node
	return collection

def replay_operations(collection, operations):
	### Apply a generated sequence using either list's public operations.
	for operation, value in operations:
		if operation == "append":
			collection.append(WorkloadRequest(value))
		elif operation == "find":
			collection.findById(value)
		elif operation == "get":
			collection.getAt(value)
		else:
			collection.removeAt(value)

	return collection.count()


def median(values):
	ordered = sorted(values)
	middle = len(ordered) // 2
	if len(ordered) % 2:
		return ordered[middle]
	return (ordered[middle - 1] + ordered[middle]) / 2


def run_benchmark(seed=20261019):
	operations = generate_operations(seed)
	print(f"Seed={seed}; initial size={n_0}; operations={len(operations)}")
	print("Expected mix: append 80%, find 10% (80% hits), getAt 5%, removeAt 5%")

	for kind, list_type in (("array", ArrayRequestList), ("linked", LinkedRequestList)):
		durations = []
		final_size = None
		for _ in range(RUN_COUNT):
			collection = build_collection(kind, n_0)
			start = time.perf_counter()
			final_size = replay_operations(collection, operations)
			durations.append(time.perf_counter() - start)

		print(
			f"{kind:6} median={median(durations):.6f}s "
			f"runs={RUN_COUNT} final_size={final_size}"
		)

	# The generated operations have about 16,000 appends and 1,000 removals.
	expected_size = n_0 + sum(op == "append" for op, _ in operations) \
		- sum(op == "remove" for op, _ in operations)
	print(f"Expected final size for both structures: {expected_size}")


if __name__ == "__main__":
	run_benchmark()



