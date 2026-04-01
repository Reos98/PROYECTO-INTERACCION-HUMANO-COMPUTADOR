from flask import Flask, render_template, request, session, redirect, url_for, flash

app = Flask(__name__)
# HCI: Usamos secret_key para manejar la sesión del usuario de forma segura y poder dar feedback con 'flash'
app.secret_key = 'super_secret_key_hci' 

# Datos simulados de cascos
# HCI: Estructurar bien los datos permite mostrar información clara y consistente al usuario en distintas vistas.
PRODUCTS = [
    {"id": 1, "nombre": "Casco Moto Integral Edge", "tipo": "Moto", "precio": 120.00, "imagen": "/static/img/casco_moto_integral_1775081139333.png"},
    {"id": 2, "nombre": "Casco Bici MTB Fox", "tipo": "Bicicleta", "precio": 85.50, "imagen": "/static/img/casco_bici_mtb_1775081153734.png"},
    {"id": 3, "nombre": "Casco Skate Pro Triple 8", "tipo": "Deportes", "precio": 45.00, "imagen": "/static/img/casco_skate_pro_1775081166674.png"},
    {"id": 4, "nombre": "Casco Moto Modular HJC", "tipo": "Moto", "precio": 150.00, "imagen": "/static/img/casco_moto_modular_1775081182778.png"},
    {"id": 5, "nombre": "Casco Enduro MX-9", "tipo": "Moto", "precio": 180.00, "imagen": "/static/img/casco_enduro_mx9_1775081195766.png"},
    {"id": 6, "nombre": "Casco Urbano Thousand", "tipo": "Bicicleta", "precio": 95.00, "imagen": "/static/img/casco_urbano_thousand_1775081208167.png"},
    {"id": 7, "nombre": "Casco Integral Arai XS", "tipo": "Moto", "precio": 450.00, "imagen": "/static/img/casco_integral_arai_1775081222175.png"},
    {"id": 8, "nombre": "Casco POC Octal", "tipo": "Bicicleta", "precio": 220.00, "imagen": "/static/img/casco_poc_octal_1775081236289.png"},
    {"id": 9, "nombre": "Casco Jet Retro Clásico", "tipo": "Moto", "precio": 110.00, "imagen": "/static/img/casco_jet_retro_1775081252387.png"},
    {"id": 10, "nombre": "Casco BMX Calavera", "tipo": "Deportes", "precio": 35.00, "imagen": "/static/img/casco_bmx_calavera_1775081265051.png"}
]

@app.before_request
def make_session_permanent():
    # HCI: Mantener al usuario conectado evita la fricción de tener que loguearse constantemente.
    session.permanent = True

@app.context_processor
def inject_cart_count():
    # HCI: Feedback visual constante. El usuario siempre debe saber cuántos items tiene en el carrito sin tener que realizar interacciones extra.
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
        # Simulación de Auth
        username = request.form.get('username')
        password = request.form.get('password')
        
        # HCI: Manejo de errores claro e instructivo. Informar al usuario el problema exacto.
        if not username or not password:
            flash('Por favor, completa tanto tu usuario como tu contraseña.', 'error')
        elif username == 'admin' and password == '1234':
            session['user'] = username
            flash('¡Inicio de sesión exitoso! Bienvenido de nuevo.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.', 'error')
            
    return render_template('login.html')

@app.route('/registro')
def registro():
    return "<h1>Página de Registro</h1>" # A implementar luego

@app.route('/logout')
def logout():
    session.pop('user', None)
    # HCI: Confirmación del estado del sistema ante una acción destructiva/salida.
    flash('Has cerrado sesión correctamente. ¡Vuelve pronto!', 'info')
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    cart = session.get('cart', [])
    # HCI: Total calculado automáticamente e instantáneo, reduciendo la carga cognitiva del usuario
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
        
        # Agrupa la cantidad de un mismo producto en vez de agregarlo x veces a la lista
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
        # HCI: Feedback positivo inmediato confirmando la acción que acaba de realizar.
        flash(f"Se ha añadido '{casco['nombre']}' a tu carrito.", 'success')
        
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
