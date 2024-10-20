class InventoryItem:
    def __init__(self, name, price, quantity, weight, value):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.weight = weight
        self.value = value

def merge_sort(items, key='name'):
    if len(items) > 1:
        mid = len(items) // 2
        left_half = items[:mid]
        right_half = items[mid:]

        merge_sort(left_half, key)
        merge_sort(right_half, key)

        i, j, k = 0, 0, 0

        while i < len(left_half) and j < len(right_half):
            if getattr(left_half[i], key) < getattr(right_half[j], key):
                items[k] = left_half[i]
                i += 1
            else:
                items[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            items[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            items[k] = right_half[j]
            j += 1
            k += 1

def binary_search(items, target_name, key='name'):
    merge_sort(items, key)
    low, high = 0, len(items) - 1

    while low <= high:
        mid = (low + high) // 2
        if getattr(items[mid], key) == target_name:
            return items[mid]
        elif getattr(items[mid], key) < target_name:
            low = mid + 1
        else:
            high = mid - 1

    return None

def knapsack(items, capacity):
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if items[i - 1].weight <= w:
                dp[i][w] = max(dp[i - 1][w], items[i - 1].value + dp[i - 1][w - items[i - 1].weight])
            else:
                dp[i][w] = dp[i - 1][w]

    selected_items = []
    i, j = n, capacity
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            selected_items.append(items[i - 1])
            j -= items[i - 1].weight
        i -= 1

    return dp[n][capacity], selected_items

def bellman_ford_shortest_paths(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node].items():
                if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight

    # Check for negative-weight cycles
    for node in graph:
        for neighbor, weight in graph[node].items():
            if distances[node] != float('inf') and distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    return distances

# Example usage:
item1 = InventoryItem("Item1", 10, 50, 5, 100)
item2 = InventoryItem("Item2", 5, 30, 3, 50)
item3 = InventoryItem("Item3", 20, 20, 8, 150)

inventory = [item1, item2, item3]

# Binary search using merge sort
search_item_name = input("Enter the name of the item to search: ")
target_item = binary_search(inventory, search_item_name, key='name')
print("Binary Search Result:", target_item.__dict__ if target_item else "Item not found")

# Merge sort
sort_key = input("Enter the sorting key (name/price/quantity/weight/value): ")
merge_sort(inventory, key=sort_key)
print(f"Merge Sort Result (by {sort_key.capitalize()}):")
for item in inventory:
    print(item.__dict__)

# Knapsack problem after sorting and searching
knapsack_capacity = int(input("Enter the knapsack capacity: "))
knapsack_value, selected_items = knapsack(inventory, knapsack_capacity)
print(f"Knapsack Value for Capacity {knapsack_capacity}:", knapsack_value)
print("Selected Items:")
for item in selected_items:
    print(item.__dict__)

# Bellman-Ford algorithm
graph = {
    'Warehouse': {'LocationA': 2, 'LocationB': 4, 'LocationC': 6},
    'LocationA': {'LocationB': -1},
    'LocationB': {'LocationC': 1},
    'LocationC': {}
}
try:
    shortest_paths = bellman_ford_shortest_paths(graph, start='Warehouse')
    print("Bellman-Ford Shortest Paths:", shortest_paths)
except ValueError as e:
    print(e)
