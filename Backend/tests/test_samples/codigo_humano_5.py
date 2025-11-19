def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

# probando diferentes valores
print(factorial(5))  # deberia dar 120
print(factorial(0))  # deberia dar 1
print(factorial(10))

# ahora vamos a hacer algo mas complicado
def permutaciones(s):
    if len(s) <= 1:
        return [s]
    
    perms = []
    for i, char in enumerate(s):
        resto = s[:i] + s[i+1:]
        for p in permutaciones(resto):
            perms.append(char + p)
    
    return perms

# test
resultado = permutaciones("abc")
print(resultado)
print(f"total: {len(resultado)}")  # deberia ser 6
