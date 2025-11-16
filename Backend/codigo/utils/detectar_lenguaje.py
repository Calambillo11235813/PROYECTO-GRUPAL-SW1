# backend/codigo/utils/detectar_lenguaje.py
def detectar_lenguaje(nombre_archivo, contenido):
    nombre = nombre_archivo.lower()

    # Detectar por extensión
    if nombre.endswith(".py"):
        return "python"
    if nombre.endswith(".js"):
        return "javascript"
    if nombre.endswith(".java"):
        return "java"
    if nombre.endswith(".cpp") or nombre.endswith(".cc") or nombre.endswith(".cxx"):
        return "cpp"
    if nombre.endswith(".cs"):
        return "csharp"
    if nombre.endswith(".php"):
        return "php"
    if nombre.endswith(".ts"):
        return "typescript"
    if nombre.endswith(".rb"):
        return "ruby"
    if nombre.endswith(".go"):
        return "go"
    if nombre.endswith(".swift"):
        return "swift"

    # Si no tiene extensión → heurística básica
    contenido_lower = contenido.lower()

    if "import " in contenido_lower and "def " in contenido_lower:
        return "python"

    if "function " in contenido_lower or "console.log" in contenido_lower:
        return "javascript"

    if "public class " in contenido_lower or "static void main" in contenido_lower:
        return "java"

    if "#include" in contenido_lower:
        return "cpp"

    return "desconocido"
