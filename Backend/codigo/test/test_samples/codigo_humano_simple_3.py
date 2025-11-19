# Grade calculator

def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

# Test with different scores
scores = [95, 82, 78, 65, 55]
for score in scores:
    grade = calculate_grade(score)
    print(f"Score {score} = Grade {grade}")
