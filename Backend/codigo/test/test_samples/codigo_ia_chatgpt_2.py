def main():
    numbers = [1, 2, 3, 4, 5]
    
    squared = []
    for num in numbers:
        squared.append(num ** 2)
    
    print(squared)

def process_string(s):
    result = ""
    for char in s:
        if char.isalpha():
            result += char.upper()
    return result

def find_max(arr):
    if not arr:
        return None
    max_val = arr[0]
    for val in arr:
        if val > max_val:
            max_val = val
    return max_val

def is_palindrome(s):
    cleaned = ""
    for char in s:
        if char.isalnum():
            cleaned += char.lower()
    return cleaned == cleaned[::-1]

if __name__ == "__main__":
    main()
