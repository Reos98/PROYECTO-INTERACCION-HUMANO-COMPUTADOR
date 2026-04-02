from flask import Flask, render_template, request, session, redirect, url_for, flash
import json
import os
import tempfile

app = Flask(__name__)
# HCI: Usamos secret_key para manejar la sesión del usuario de forma segura y poder dar feedback con 'flash'
app.secret_key = 'super_secret_key_hci' 

USERS_FILE = os.path.join(tempfile.gettempdir(), 'users.json')

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'admin': '1234'}

def save_users(users_dict):
    with open(USERS_FILE, 'w') as f:
        json.dump(users_dict, f)

# Cargamos base de datos de usuarios
USERS = load_users()

# Datos simulados de cascos ampliados con descripciones
# HCI: Estructurar bien los datos permite mostrar información clara y consistente al usuario en distintas vistas.
PRODUCTS = [
    {
        "id": 1, "nombre": "Casco Moto Integral Edge", "tipo": "Moto", "precio": 120.00, 
        "imagen": "/static/img/casco_moto_integral_1775081139333.png", 
        "descripcion": "Casco integral de alta resistencia con diseño aerodinámico.", 
        "material": "Policarbonato", "peso": "1.45 kg"
    },
    {
        "id": 2, "nombre": "Casco Bici MTB Fox", "tipo": "Bicicleta", "precio": 85.50, 
        "imagen": "/static/img/casco_bici_mtb_1775081153734.png", 
        "descripcion": "Ideal para Cross Country y Trail con excelente ventilación.", 
        "material": "EPS y Policarbonato In-Mold", "peso": "320 g"
    },
    {
        "id": 3, "nombre": "Casco Skate Pro Triple 8", "tipo": "Deportes", "precio": 45.00, 
        "imagen": "/static/img/casco_skate_pro_1775081166674.png", 
        "descripcion": "Protección clásica para deportes extremos. Interior de espuma EVA.", 
        "material": "Plástico ABS", "peso": "450 g"
    },
    {
        "id": 4, "nombre": "Casco Moto Modular HJC", "tipo": "Moto", "precio": 150.00, 
        "imagen": "/static/img/casco_moto_modular_1775081182778.png", 
        "descripcion": "Versatilidad abatible para viajes largos y ciudad.", 
        "material": "Fibra de vidrio", "peso": "1.65 kg"
    },
    {
        "id": 5, "nombre": "Casco Enduro MX-9", "tipo": "Moto", "precio": 180.00, 
        "imagen": "/static/img/casco_enduro_mx9_1775081195766.png", 
        "descripcion": "Alto rendimiento para off-road con visera ajustable y sistema MIPS.", 
        "material": "Policarbonato reforzado", "peso": "1.5 kg"
    },
    {
        "id": 6, "nombre": "Casco Urbano Thousand", "tipo": "Bicicleta", "precio": 95.00, 
        "imagen": "/static/img/casco_urbano_thousand_1775081208167.png", 
        "descripcion": "Estilo vintage para la ciudad. Incluye sistema PopLock para candado.", 
        "material": "Carcasa ABS, interior EPS", "peso": "410 g"
    },
    {
        "id": 7, "nombre": "Casco Integral Arai XS", "tipo": "Moto", "precio": 450.00, 
        "imagen": "/static/img/casco_integral_arai_1775081222175.png", 
        "descripcion": "El pináculo de la seguridad. Supera las certificaciones más estrictas.", 
        "material": "Super Fibra Laminada (SFC)", "peso": "1.6 kg"
    },
    {
        "id": 8, "nombre": "Casco POC Octal", "tipo": "Bicicleta", "precio": 220.00, 
        "imagen": "/static/img/casco_poc_octal_1775081236289.png", 
        "descripcion": "Innovación en seguridad y ligereza para ciclismo de ruta profesional.", 
        "material": "Núcleo EPS optimizado", "peso": "195 g"
    },
    {
        "id": 9, "nombre": "Casco Jet Retro Clásico", "tipo": "Moto", "precio": 110.00, 
        "imagen": "/static/img/casco_jet_retro_1775081252387.png", 
        "descripcion": "Diseño abierto retro con acabados en cuero premium.", 
        "material": "Fibra de vidrio y Cuero", "peso": "1.1 kg"
    },
    {
        "id": 10, "nombre": "Casco BMX Calavera", "tipo": "Deportes", "precio": 35.00, 
        "imagen": "/static/img/casco_bmx_calavera_1775081265051.png", 
        "descripcion": "Diseño agresivo y gran resistencia para saltos y trucos en bici.", 
        "material": "Plástico de inyección termoplástica", "peso": "480 g"
    }
]

@app.before_request
def make_session_permanent():
    # HCI: Mantener al usuario conectado evita la fricción de tener que loguearse constantemente.
    session.permanent = True

@app.context_processor
def inject_cart_count():
    # HCI: Feedback visual constante.
    cart = session.get('cart', [])
    return dict(cart_count=sum(item['cantidad'] for item in cart))

@app.route('/')
def index():
    return render_template('index.html', cascos=PRODUCTS)

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html', cascos=PRODUCTS)

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/soporte')
def soporte():
    return render_template('soporte.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Refresh to ensure latest from file if modified externally
        global USERS
        USERS = load_users()
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        # HCI: Manejo de errores instructivo.
        if not username or not password:
            flash('Por favor, completa tanto tu usuario como tu contraseña.', 'error')
        elif username in USERS and USERS[username] == password:
            session['user'] = username
            flash('¡Inicio de sesión exitoso! Bienvenido de nuevo.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'error')
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        global USERS
        USERS = load_users()
        
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not username or not email or not password:
            flash('Todos los campos son obligatorios para crear una cuenta.', 'error')
        elif username in USERS:
            flash('Este usuario ya existe. Intenta con otro nombre de usuario.', 'error')
        else:
            USERS[username] = password
            save_users(USERS)
            flash('¡Cuenta creada con éxito! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
            
    return render_template('registro.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Has cerrado sesión correctamente. ¡Vuelve pronto!', 'info')
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    cart = session.get('cart', [])
    subtotal = sum(item['precio'] * item['cantidad'] for item in cart)
    return render_template('carrito.html', cart=cart, subtotal=subtotal)

@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    casco = next((c for c in PRODUCTS if c['id'] == id), None)
    if casco:
        if 'cart' not in session:
            session['cart'] = []
        
        cart = session['cart']
        encontrado = False
        
        for item in cart:
            if item['id'] == id:
                item['cantidad'] += 1
                encontrado = True
                break
                
        if not encontrado:
            cart.append({
                'id': casco['id'],
                'nombre': casco['nombre'],
                'precio': casco['precio'],
                'imagen': casco['imagen'],
                'cantidad': 1
            })
            
        session.modified = True
        flash(f"Se ha añadido '{casco['nombre']}' a tu carrito.", 'success')
        
    return redirect(request.referrer or url_for('index'))

@app.route('/remove_from_cart/<int:id>')
def remove_from_cart(id):
    if 'cart' in session:
        # Filtramos dejando todos los que NO son el id solicitado
        session['cart'] = [item for item in session['cart'] if item['id'] != id]
        session.modified = True
        flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('carrito'))

@app.route('/increase_quantity/<int:id>')
def increase_quantity(id):
    if 'cart' in session:
        for item in session['cart']:
            if item['id'] == id:
                item['cantidad'] += 1
                session.modified = True
                break
    return redirect(url_for('carrito'))

@app.route('/decrease_quantity/<int:id>')
def decrease_quantity(id):
    if 'cart' in session:
        for item in session['cart']:
            if item['id'] == id:
                if item['cantidad'] > 1:
                    item['cantidad'] -= 1
                    session.modified = True
                else:
                    # Si la cantidad baja a 0, se elimina del todo
                    return redirect(url_for('remove_from_cart', id=id))
                break
    return redirect(url_for('carrito'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not session.get('cart'):
        flash('Tu carrito está vacío. Agrega productos antes de pagar.', 'warning')
        return redirect(url_for('carrito'))
        
    if request.method == 'POST':
        # Simular pago y vaciar carrito
        session.pop('cart', None)
        flash('¡Pago procesado con éxito! Gracias por tu compra en MotoSafe.', 'success')
        return redirect(url_for('index'))
        
    cart = session.get('cart', [])
    total = sum(item['precio'] * item['cantidad'] for item in cart)
    return render_template('checkout.html', total=total)

# ---- Páginas Rápidas de Footer ----
@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/tallas')
def tallas():
    return render_template('tallas.html')

@app.route('/envios')
def envios():
    return render_template('envios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)
