# imports
from flask import Flask

app = Flask(__name__)

# Definir uma rota raiz (pagina inicial) e a funcao que sera executada ao requisitar 
@app.route('/')
def hellow_word():
    return 'Hellow Word'

if __name__ == "__main__":
    app.run(debug=True)