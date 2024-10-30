from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='template', static_folder='static')

# Datos de ejemplo para probar el login (AQUÍ CONECTAR BD)
usuarios = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2'
}

def verificar_credenciales(usuario, contraseña):
    return usuarios.get(usuario) == contraseña

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    usuario = data.get('username')
    contraseña = data.get('password')
    
    if verificar_credenciales(usuario, contraseña):
        return jsonify({"message": f"¡Bienvenido, {usuario}!"}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
