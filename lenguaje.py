import re
from flask import Flask, render_template, request, jsonify

gramatica = {
    "Tipo": r"(X|Y|A|B)",
    "Nombre": r"[a-z][a-z0-9]*",
    "Asignacion": r"=",
    "Entero": r"\d+",
    "Cadena": r'"[^"]*"',
    "Double": r"\d+\.\d+",
    "Booleano": r"(True|False)",

    "PalabraFuncion": r"LT",
    "Parametros": r"<>",
    "DosPuntos": r":",
    "Contenido": r".+$",
   
    "SaltoLinea": r"\n +",

    "PalabraCiclo": r"RT",
    "Operador": r"(>|<|>=|<=|==|!=)",

    "PalabraCondicion": r"RB",
    "PalabraMain": r"Start",
}

def validar_var(cadena):
    tipos_permitidos = {
        "X": gramatica["Entero"],
        "Y": gramatica["Cadena"],
        "A": gramatica["Double"],
        "B": gramatica["Booleano"]
    }

    tipo_match = re.match(gramatica["Tipo"], cadena)
    if tipo_match:
        tipo = tipo_match.group()
        if tipo in tipos_permitidos:
            tipo_re = tipos_permitidos[tipo]
            gramatica_pattern = re.compile(f"^{gramatica['Tipo']} {gramatica['Nombre']} {gramatica['Asignacion']} {tipo_re}$")
            print(gramatica_pattern)
            if gramatica_pattern.match(cadena):
                return True
    return False


def validar_func(cadena):
    gramatica_pattern = re.compile(f"^{gramatica['PalabraFuncion']} {gramatica['Nombre']}{gramatica['Parametros']}{gramatica['DosPuntos']}({gramatica['SaltoLinea']}| {gramatica['Contenido']})+$")
    print(gramatica_pattern)

    if gramatica_pattern.match(cadena):
        return True
    return False


def validar_cic(cadena):
    gramatica_pattern = re.compile(f"^{gramatica['PalabraCiclo']} ({gramatica['Nombre']}|{gramatica['Entero']}|{gramatica['Booleano']}) {gramatica['Operador']} ({gramatica['Nombre']}|{gramatica['Entero']}|{gramatica['Booleano']}){gramatica['DosPuntos']}({gramatica['SaltoLinea']}| {gramatica['Contenido']})+$")
    print(gramatica_pattern)

    if gramatica_pattern.match(cadena):
        return True
    return False


def validar_cond(cadena):
    gramatica_pattern = re.compile(f"^{gramatica['PalabraCondicion']} ({gramatica['Nombre']}|{gramatica['Entero']}|{gramatica['Booleano']}) {gramatica['Operador']} ({gramatica['Nombre']}|{gramatica['Entero']}|{gramatica['Booleano']}){gramatica['DosPuntos']}({gramatica['SaltoLinea']}| {gramatica['Contenido']})+$")
    print(gramatica_pattern)

    if gramatica_pattern.match(cadena):
        return True
    return False


def validar_main(cadena):
    gramatica_pattern = re.compile(f"^{gramatica['PalabraMain']}{gramatica['DosPuntos']}({gramatica['SaltoLinea']}| {gramatica['Contenido']})+$")
    print(gramatica_pattern)

    if gramatica_pattern.match(cadena):
        return True
    return False

def validar_construccion(cadena):
    if validar_var(cadena):
        return "La cadena es una variable"
    elif validar_func(cadena):
        return "La cadena es una función"
    elif validar_cic(cadena):
        return "La cadena es un ciclo"
    elif validar_cond(cadena):
        return "La cadena es una condición"
    elif validar_main(cadena):
        return "La cadena es el main"
    else:
        return "ERROR: La cadena no es válida"
    
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validar', methods=['POST'])
def validar_cadena():
    data = request.get_json()
    codigo = data['codigo']
    resultado = validar_construccion(codigo)
    return jsonify({"resultado": resultado})

if __name__ == '__main__':
    app.run(debug=True)