import random

def totient(p, q):
    return (p - 1) * (q - 1)

def prime(n_integer):
    if n_integer <= 1:
        return False
    if(n_integer <= 3):
        return True
    if(n_integer % 2 == 0 or n_integer % 3 == 0):
        return False
    i = 5
    while(i * i <= n_integer):
        if(n_integer % i == 0 or n_integer % (i + 2) == 0):
            return False
        i = i + 6
    return True

def modulo(a, b):
    if b == 0:
        raise ValueError("Divisor não pode ser zero")
    return a % b 

def mdc(a, b):  
    while(b != 0):
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        return None
    else:
        return x % phi  

def calculate_d(e, phi):
    return mod_inverse(e, phi)

def calculate_e(phi):
    e = 3
    while e < phi:
        if mdc(e, phi) == 1:
            return e
        e += 2
    return None

def cipher_encrypt(ciphertext, e, n):
    tam = len(ciphertext)
    i = 0
    encrypted = []
    while i < tam:
        letter = ciphertext[i]
        k = ord(letter)
        d = pow(k, e, n)
        encrypted.append(d)
        i += 1
    return encrypted

def decipher_encrypt(encrypted, d, n):
    list = []
    i = 0
    tam = len(encrypted)
    while i < tam:
        result = pow(encrypted[i], d, n)
        letra = chr(result)
        list.append(letra)
        i += 1
    return list

# Os valores de p e q devem ser números primos grandes para garantir a segurança da criptografia RSA.
# Além disso, n = p * q precisa ser maior que qualquer valor ASCII do texto a ser criptografado.
# Na prática, p e q são escolhidos aleatoriamente com centenas de dígitos para dificultar a fatoração.


p = 101
q = 113
n = p * q
phi = totient(p, q)
e = calculate_e(phi)
d = calculate_d(e, phi)

texto = "InstitutoFederal"
encriptado = cipher_encrypt(texto, e, n)
print("Chaves (n, e, d):", n, e, d)
print("Texto criptografado:", encriptado)

decifrado = decipher_encrypt(encriptado, d, n)
print("Texto decifrado:", "".join(decifrado))
