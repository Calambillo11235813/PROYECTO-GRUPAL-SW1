import random

# mi implementacion de quicksort
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)

# testing
test_list = [random.randint(1, 100) for _ in range(10)]
print("Original:", test_list)
sorted_list = quicksort(test_list)
print("Sorted:", sorted_list)

# verificar si funciona
assert sorted_list == sorted(test_list), "algo esta mal!"
print("ok!")
