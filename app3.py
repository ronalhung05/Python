from flask import Flask, jsonify, request

app = Flask(__name__)

def fibonacci(n):
    seq = [0, 1]
    for i in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

def prime_numbers(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def perfect_numbers(n):
    numbers = []
    i = 1
    while len(numbers) < n:
        if is_perfect(i):
            numbers.append(i)
        i += 1
    return numbers


def armstrong_numbers(n):
    numbers = []
    i = 1
    while len(numbers) < n:
        if is_armstrong(i):
            numbers.append(i)
        i += 1
    return numbers

def harshad_numbers(n):
    numbers = []
    i = 1
    while len(numbers) < n:
        if is_harshad(i):
            numbers.append(i)
        i += 1
    return numbers


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

@app.route('/fibonacci/<int:n>')
def get_fibonacci(n):
    return jsonify(fibonacci(n))

@app.route('/primes/<int:n>')
def get_primes(n):
    return jsonify(prime_numbers(n))

@app.route('/perfect/<int:n>')
def get_perfect(n):
    return jsonify(perfect_numbers(n))

@app.route('/armstrong/<int:n>')
def get_armstrong(n):
    return jsonify(armstrong_numbers(n))


@app.route('/harshad/<int:n>')
def get_harshad(n):
    return jsonify(harshad_numbers(n))

@app.route('/gcd')
def get_gcd():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return jsonify(gcd(a, b))

@app.route('/lcm')
def get_lcm():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return jsonify(lcm(a, b))
# Check perfect number
def is_perfect(n):
    return n == sum(i for i in range(1, n) if n % i == 0)

# Check prime number
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to check Armstrong number
def is_armstrong(n):
    digits = [int(x) for x in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def is_harshad(n):
    return n % sum(int(d) for d in str(n)) == 0


def are_coprime(a, b):
    return gcd(a, b) == 1

@app.route('/is_perfect/<int:n>')
def check_perfect(n):
    result = "a perfect number" if is_perfect(n) else "not a perfect number"
    return jsonify(f"{n} is {result}")


@app.route('/is_prime/<int:n>')
def check_prime(n):
    result = "a prime number" if is_prime(n) else "not a prime number"
    return jsonify(f"{n} is {result}")

@app.route('/is_armstrong/<int:n>')
def check_armstrong(n):
    result = "an Armstrong number" if is_armstrong(n) else "not an Armstrong number"
    return jsonify(f"{n} is {result}")


@app.route('/is_harshad/<int:n>')
def check_harshad(n):
    result = "a Harshad number" if is_harshad(n) else "not a Harshad number"
    return jsonify(f"{n} is {result}")


@app.route('/are_coprime')
def check_coprime():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = "coprime" if are_coprime(a, b) else "not coprime"
    return jsonify(f"{a} and {b} are {result}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
