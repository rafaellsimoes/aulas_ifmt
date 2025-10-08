# -----------------------------------------------
# PARA EXECUTAR ESTE CÓDIGO É NECESSÁRIO INSTALAR A BIBLIOTECA:
# pip install pycryptodome
# 
# O 'pycryptodome' é uma implementação moderna e segura das funções
# criptográficas em Python, incluindo AES, DES, 3DES, RSA, entre outros.
# -----------------------------------------------

from Crypto.Cipher import AES
from Crypto.Cipher import DES3  
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes 

# -----------------------------
# CRIPTOGRAFIA SIMÉTRICA COM AES (Advanced Encryption Standard)
# -----------------------------

# Gera uma chave aleatória de 16 bytes (128 bits) para o AES
chave = get_random_bytes(16) 

# Texto que será criptografado (convertido em bytes)
dados = "IFMT - Campus Cel Octayde Jorge da Silva".encode()

# Define o tamanho do bloco (em bytes) utilizado pelo AES
bloco = 16

# Ajusta o tamanho dos dados para ser múltiplo do bloco (preenchimento)
dados = pad(dados, bloco)

# Cria o objeto de cifra AES no modo ECB (Electronic Codebook)
cipher = AES.new(chave, AES.MODE_ECB)

# Criptografa os dados
mensagem_cifrada = cipher.encrypt(dados)

# Exibe o texto cifrado em formato hexadecimal
print("Texto cifrado:", mensagem_cifrada.hex())

# -----------------------------
# DESCRIPTOGRAFIA COM AES
# -----------------------------

# Descriptografa os dados
dados_decifrado = cipher.decrypt(mensagem_cifrada)

# Remove o preenchimento adicionado anteriormente
dados_decifrado = unpad(dados_decifrado, bloco)

# Converte novamente os bytes para string legível
print("Texto decifrado:", dados_decifrado.decode())


# -----------------------------
# CRIPTOGRAFIA SIMÉTRICA COM 3DES (Triple DES)
# -----------------------------

# O 3DES utiliza chaves de 16 ou 24 bytes, por isso é gerada uma chave aleatória de 24 bytes
chave_3des = get_random_bytes(24)

# Texto a ser criptografado com 3DES (convertido em bytes)
mensagem = "Tempo seco com muito calor e possibilidade de mudança".encode()
print("mensagem:", mensagem)

# Define o tamanho do bloco para o 3DES (8 bytes)
bloco_3des = 8 

# Adiciona preenchimento à mensagem
mensagem_padded = pad(mensagem, bloco_3des)

# Cria o objeto de cifra 3DES no modo ECB
cipher = DES3.new(chave_3des, DES3.MODE_ECB)

# Criptografa os dados
mensagem_cifrada_3des = cipher.encrypt(mensagem_padded)

# Exibe o texto cifrado em formato hexadecimal
print("Texto cifrado 3DES:", mensagem_cifrada_3des.hex())

# -----------------------------
# DESCRIPTOGRAFIA COM 3DES
# -----------------------------

# Descriptografa os dados cifrados
mensagem_decifrada = cipher.decrypt(mensagem_cifrada_3des)

# Remove o preenchimento corretamente (agora sobre a variável descriptografada)
mensagem_decifrada = unpad(mensagem_decifrada, bloco_3des)

# Converte novamente os bytes para string legível
print("Texto decifrado:", mensagem_decifrada.decode())
