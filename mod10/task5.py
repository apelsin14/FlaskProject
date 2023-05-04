def find_insert_position(arr, x):
    left = 0
    right = len(arr)

    while left < right:
        middle = (left + right) // 2
        if arr[middle] < x:
            left = middle + 1
        else:
            right = middle
    return left