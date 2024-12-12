import random

def generate_passwords(num_passwords, password_length):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*().,?0123456789'
    passwords = []

    for _ in range(num_passwords):
        password = ''.join(random.choice(chars) for _ in range(password_length))
        passwords.append(password)
    
    return passwords

print('Welcome To Your Password Generator')

# Input for number of passwords to generate
number = int(input('Amount of passwords to generate: '))

# Input for length of each password
length = int(input('Input your password length: '))

print('\nHere are your passwords:')

# Generate and print passwords
passwords = generate_passwords(number, length)
for pwd in passwords:
    print(pwd)