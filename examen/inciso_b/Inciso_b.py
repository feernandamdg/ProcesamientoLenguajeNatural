import re
import string

# Leer .txt en utf-8 y mostrar su contenido en pantalla
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    return contenido

def tokenizador(texto):

  token = ""
  tokens = []
  
  withes = string.whitespace
  delimitadores = string.whitespace + string.punctuation
  numbers = string.digits
  not_letters = delimitadores + numbers

  if texto[-1] not in delimitadores:
    texto = texto + '.'
    #print("Texto ingresado:", texto)
    
  is_number = None

  for i in range(0, len(texto)):
    char = texto[i]
    if texto[i] == '.' or texto[i] in withes:
      if token != "":
        tokens = tokens + [token]
      token = ""
      is_number = None
    elif token == "" and texto[i] not in delimitadores:
        if texto[i] in numbers:
            is_number = True
        if texto[i] not in not_letters:
            is_number = False
        token += texto[i]
    elif texto[i] not in not_letters and is_number: # Si comenzó como digito y encontró letra.
          token = texto[i]
          is_number = False
    elif (texto[i] in numbers and is_number) or (texto[i] not in not_letters and not is_number): #Si texto[i] corresponde a la bandera
          token += texto[i]

  return tokens

def A_minusculas(texto):
    letras = ""
    
    for letra in texto:
        if ord(letra) >= 65 and ord(letra) <=90:
            letra = chr(ord(letra) +32)
        letras += letra
    return letras

def detectar_instituciones(tokens):

    patrones = ['Secretaría', 'Ministerio', 'Instituto', 'Universidad', 'Escuela', 'Facultad', 'Departamento', 'Dirección', 'Agencia', 'Organización', 'Comisión', 'Policía']
    instituciones = []
    flag = False

    for token in tokens:
        if flag:
            if token[0].isupper() or token in ['de', 'del', 'la', 'y', 'en']:
                instituciones[-1] += ' ' + token
            else:
                flag = False
        if token in patrones:
            flag = True
            instituciones.append(token)

    return instituciones

def detectar_telefonos(tokens):
    telefonos = []
    for token in tokens:
        if token.isdigit() and len(token) == 10:
            telefonos.append(token)
    return telefonos

def es_codigo_postal(token):
    return token.isdigit() and len(token) == 5

def detectar_direcciones(tokens):
    patrones = ['Calle', 'Avenida', 'Boulevard', 'Av']
    direcciones = []
    flag_direccion = False
# Si encontramos codigo postal, ya somo verificamos que las siguientes tres letras no sean Ciudad de México, si no, agregamos eso a la dirección

    for token in tokens:
        if flag_direccion:
            direcciones[-1] += ' ' + token
            if es_codigo_postal(token):
                direcciones[-1] += ' ' + token
                flag_direccion = False
            
        if token in patrones:
            flag_direccion = True
            direcciones.append(token)

    return direcciones

# pruebas

texto = leer_archivo('texto.txt')
tokens = tokenizador(texto)
print("Tokens:")
print(tokens)
instituciones = detectar_instituciones(tokens)
print("\nInstituciones detectadas:\n")
for institucion in instituciones:
    print(institucion)
telefonos = detectar_telefonos(tokens)
print("\nTeléfonos detectados:\n")
for telefono in telefonos:
    print(telefono)

direcciones = detectar_direcciones(tokens)
print("\nDirecciones detectadas:\n")
for direccion in direcciones:
    print(direccion)
    
