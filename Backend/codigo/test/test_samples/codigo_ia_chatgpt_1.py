# Código típico de ChatGPT - sin documentación excesiva, patrones repetitivos

def process_data(data):
    result = []
    for item in data:
        if item is not None:
            processed_item = item * 2
            result.append(processed_item)
    return result

def validate_input(value):
    if value is None:
        return False
    if not isinstance(value, (int, float)):
        return False
    return True

def calculate_average(numbers):
    if not numbers:
        return 0
    total = sum(numbers)
    count = len(numbers)
    return total / count

def filter_positive(numbers):
    result = []
    for num in numbers:
        if num > 0:
            result.append(num)
    return result
