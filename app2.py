from flask import Flask, request, render_template
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

app = Flask(__name__)


# Hàm mã hóa Caesar
def caesar_encrypt(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result


# Hàm mã hóa Affine
def affine_encrypt(text, a, b):
    result = ""
    for char in text:
        if char.isupper():
            result += chr(((a * (ord(char) - 65) + b) % 26) + 65)
        elif char.islower():
            result += chr(((a * (ord(char) - 97) + b) % 26) + 97)
        else:
            result += char
    return result


# Hàm mã hóa AES sử dụng thư viện cryptography
def aes_encrypt(text, key):
    backend = default_backend()
    iv = os.urandom(16)  # Khởi tạo IV ngẫu nhiên
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()


def triple_des_encrypt(text, key):
    backend = default_backend()
    iv = os.urandom(8)  # Khởi tạo IV ngẫu nhiên cho 3DES (8 byte)
    cipher = Cipher(algorithms.TripleDES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(iv + ciphertext).decode()



# Trang chủ hiển thị form mã hóa
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        method = request.form['method']

        # Caesar Encryption
        if method == 'caesar':
            shift = int(request.form['shift'])
            result = caesar_encrypt(text, shift)

        # Affine Encryption
        elif method == 'affine':
            a = int(request.form['a'])
            b = int(request.form['b'])
            result = affine_encrypt(text, a, b)

        # AES Encryption
        elif method == 'aes':
            key = os.urandom(32)  # Khóa AES 256-bit
            result = aes_encrypt(text, key)

        # DES Encryption
        elif method == 'des':
            key = os.urandom(8)  # Khóa DES 64-bit
            result = triple_des_encrypt(text, key)

        return render_template('index.html', result=result, method=method)

    return render_template('index.html', result=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
