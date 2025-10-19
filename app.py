from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- RUTAS PRINCIPALES ---
@app.route('/')
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/carta')
def carta():
    return render_template('carta.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/reserva', methods=['GET', 'POST'])
def reserva():
    """
    Maneja la visualización del formulario de reserva (GET) y
    el procesamiento de la reserva (POST).
    """
    if request.method == 'POST':
        # Lógica de procesamiento de la reserva (ej. validar disponibilidad, guardar datos)
        # datos_reserva = request.form
        
        # Redirige a la página de confirmación de reserva
        return redirect(url_for('reserva_confirmada'))

    return render_template('reserva.html')

@app.route('/reserva_confirmada')
def reserva_confirmada():
    """Muestra la página de confirmación después de una reserva exitosa."""
    return render_template('reserva_confirmada.html')


# --- RUTAS DE DELIVERY ---
@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    
    if request.method == 'POST':
        return redirect(url_for('carta_delivery'))
    
    return render_template('delivery.html')

@app.route('/carta_delivery')
def carta_delivery():
      return render_template('carta_delivery.html')

@app.route('/delivery_confirmado')
def delivery_confirmado():
        return render_template('delivery_confirmado.html')


# --- RUTA DE PROCESAMIENTO Y CONFIRMACIÓN DE PAGO (NUEVA LÓGICA) ---

@app.route('/carrito_pago', methods=['GET'])
def carrito_pago():
    """Muestra la página del carrito y el formulario de pago."""
    return render_template('carrito_pago.html')

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    """
    RUTA CORREGIDA: RECIBE EL FORMULARIO DE PAGO MEDIANTE POST.
    
    Aquí iría la lógica real para validar y ejecutar el cobro.
    Si el pago es exitoso, redirige a la confirmación de pago.
    """
    # 1. Recuperar los datos del formulario:
    # datos_pago = request.form
    
    # 2. Lógica de pago (simulada):
    pago_exitoso = True # Asumimos que el pago siempre es exitoso para el ejemplo
    
    if pago_exitoso:
        # Una vez procesado el POST, redirigimos con un GET a la página de confirmación.
        return redirect(url_for('confirmacion_pago'))
    else:
        # Manejar el error de pago (ej. redirigir a carrito con mensaje de error)
        return redirect(url_for('carrito_pago'))


@app.route('/confirmacion_pago', methods=['GET'])
def confirmacion_pago():
    """Muestra la página final de confirmación de pago (siempre por GET)."""
    # Si necesitas pasar el número de pedido, lo harías aquí:
    # return render_template('confirmacion_pago.html', pedido_numero=request.args.get('id'))
    return render_template('confirmacion_pago.html')


# --- OTRAS RUTAS ---
@app.route('/seguimiento')
def seguimiento():
    return render_template('seguimiento.html')


# --- RUTAS DE CATEGORÍAS ---
@app.route('/pollo')
def pollos():
    return render_template('carta_pollo.html')

@app.route('/pizza')
def pizza():
    return render_template('carta_pizza.html')

@app.route('/pastas')
def pastas():
    return render_template('carta_pastas.html')

@app.route('/bebidas')
def bebidas():
    return render_template('carta_bebidas.html')


# --- INICIO DE LA APLICACIÓN ---
if __name__ == '__main__':
    # Asegúrate de usar debug=True solo en desarrollo
    app.run(debug=True)
