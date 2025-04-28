from flask import Flask, render_template,request
import random
import string

app = Flask(__name__, template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        use_uppercase = 'uppercase' in request.form
        use_numbers = 'numbers' in request.form
        use_symbols = 'symbols' in request.form
        
        characters = list(string.ascii_lowercase)
        
        if use_uppercase:
            characters += list(string.ascii_uppercase)
        if use_numbers:
            characters += list(string.digits)
        if use_symbols:
            characters += list('!@#$%^&*()-_=+[]{};:,.<>?')
        
        password = ''.join(random.choice(characters) for _ in range(length))
    
    return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)