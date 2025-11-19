# Código típicamente escrito por humano
# Tiene bugs, comentarios informales, y estilo inconsistente

def calc(x, y):
    # TODO: fix this later
    result = x + y
    print(result)  # debug
    return result

# probando...
nums = [1,2,3, 4,5]
total=0
for n in nums:
    total+=n
    
print(total)

class Usuario:
    def __init__(self, nombre):
        self.nombre=nombre
        
    def saludar(self):
        print(f"hola {self.nombre}!")

u = Usuario("Juan")
u.saludar()
