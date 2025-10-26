from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)

# ----------------------------------------------------------------------
# 🔐 CLAVE SECRETA Y CONFIG BD
# ----------------------------------------------------------------------
app.secret_key = 'TU_CLAVE_SECRETA_SUPER_LARGA_Y_COMPLEJA'

DB_HOST = 'angello.c1jh3g8aqs0w.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'angello1234'
DB_NAME = 'dbangello'

# ----------------------------------------------------------------------
# 🔹 FUNCIÓN DE CONEXIÓN A BD
# ----------------------------------------------------------------------
def get_db_connection():
    try:
        conexion = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conexion
    except Exception as e:
        print("❌ Error al conectar con la base de datos:", e)
        return None

# ----------------------------------------------------------------------
# 🔹 RUTAS DE AUTENTICACIÓN
# ----------------------------------------------------------------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    success_message = request.args.get('success') or request.args.get('message')
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        hashed_password = generate_password_hash(contrasena)

        conn = get_db_connection()
        if conn is None:
            return render_template('registro.html', error='Error de conexión a la base de datos.', loggedin=False)

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id FROM Usuarios WHERE correo = %s", (correo,))
                if cursor.fetchone():
                    return render_template('registro.html', error='Este correo ya está registrado.', loggedin=False)
                sql = "INSERT INTO Usuarios (nombre, correo, contrasena_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (nombre, correo, hashed_password))
                conn.commit()

            with conn.cursor() as cursor:
                cursor.execute("SELECT id, nombre FROM Usuarios WHERE correo = %s", (correo,))
                user = cursor.fetchone()

            if user:
                session['loggedin'] = True
                session['id'] = user['id']
                session['nombre'] = user['nombre']
                return redirect(url_for('inicio_premium', success='¡Cuenta creada! Bienvenido a la experiencia Premium.'))
            else:
                return redirect(url_for('inicio_secion', success='Cuenta creada. Inicia sesión.'))

        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")
            return render_template('registro.html', error='Error interno al registrar.', loggedin=False)
        finally:
            conn.close()

    return render_template('registro.html', loggedin=session.get('loggedin', False),
                           nombre=session.get('nombre'), success=success_message)


@app.route('/inicio_secion', methods=['GET', 'POST'])
def inicio_secion():
    success_message = request.args.get('success')

    if session.get('loggedin'):
        return redirect(url_for('inicio_premium'))

    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        conn = get_db_connection()
        if conn is None:
            flash('Error de conexión a la base de datos.', 'error')
            return render_template('inicio_secion.html', loggedin=False)

        try:
            with conn.cursor() as cursor:
                sql = "SELECT id, nombre, correo, contrasena_hash FROM Usuarios WHERE correo = %s"
                cursor.execute(sql, (correo,))
                user = cursor.fetchone()

            if user and check_password_hash(user['contrasena_hash'], contrasena):
                session['loggedin'] = True
                session['id'] = user['id']
                session['nombre'] = user['nombre']
                return redirect(url_for('inicio_premium'))
            else:
                flash('Correo o contraseña incorrectos.', 'error')
                return render_template('inicio_secion.html', loggedin=False)

        except Exception as e:
            print(f"❌ Error al iniciar sesión: {e}")
            flash('Error interno del servidor.', 'error')
            return render_template('inicio_secion.html', loggedin=False)
        finally:
            conn.close()

    return render_template('inicio_secion.html', success=success_message,
                           loggedin=session.get('loggedin', False), nombre=session.get('nombre'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('inicio'))

# ----------------------------------------------------------------------
# 🔹 RUTAS PRINCIPALES
# ----------------------------------------------------------------------
@app.route('/')
@app.route('/inicio')
def inicio():
    if session.get('loggedin'):
        return redirect(url_for('inicio_premium'))
    return render_template('inicio.html', loggedin=False, nombre=None)


@app.route('/inicio-premium')
def inicio_premium():
    if not session.get('loggedin'):
        flash('Debes iniciar sesión para acceder al contenido Premium.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('inicio_premium.html', loggedin=True,
                           nombre=session.get('nombre'), success=request.args.get('success'))


@app.route('/promociones')
def promociones():
    if not session.get('loggedin'):
        flash('Esta sección es exclusiva para miembros.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('promociones.html', loggedin=True, nombre=session.get('nombre'))


@app.route('/nuestra-historia')
def historia():
    return render_template('historia.html',
                           loggedin=session.get('loggedin', False),
                           nombre=session.get('nombre'))

# ----------------------------------------------------------------------
# 🔹 RUTAS DE CARTAS
# ----------------------------------------------------------------------
@app.route('/nuestra-carta')
def cartas():
    loggedin = session.get('loggedin', False)
    nombre = session.get('nombre') if loggedin else None
    return render_template('cartas.html', loggedin=loggedin, nombre=nombre)

@app.route('/carta/pollos')
def carta_pollo():
    if not session.get('loggedin'):
        flash('Debes iniciar sesión para ver el menú de Pollos.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('carta_pollo.html', loggedin=True, nombre=session.get('nombre'))

@app.route('/carta/pizzas')
def carta_pizza():
    if not session.get('loggedin'):
        flash('Debes iniciar sesión para ver el menú de Pizzas.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('carta_pizza.html', loggedin=True, nombre=session.get('nombre'))

@app.route('/carta/pastas')
def carta_pasta():
    if not session.get('loggedin'):
        flash('Debes iniciar sesión para ver el menú de Pastas.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('carta_pasta.html', loggedin=True, nombre=session.get('nombre'))

@app.route('/carta/bebidas')
def carta_bebidas():
    if not session.get('loggedin'):
        flash('Debes iniciar sesión para ver el menú de Bebidas.', 'error')
        return redirect(url_for('inicio_secion'))
    return render_template('carta_bebidas.html', loggedin=True, nombre=session.get('nombre'))

# ----------------------------------------------------------------------
# 🔹 RUTA DELIVERY (NUEVA Y CORRECTA)
# ----------------------------------------------------------------------
@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    loggedin = session.get('loggedin', False)
    nombre = session.get('nombre') if loggedin else None

    if request.method == 'POST':
        nombre_cliente = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        pedido = request.form['pedido']

        conn = get_db_connection()
        if conn is None:
            flash('Error al conectar con la base de datos.', 'error')
            return render_template('delivery.html', loggedin=loggedin, nombre=nombre)

        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO Pedidos (nombre_cliente, telefono, direccion, detalle_pedido)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre_cliente, telefono, direccion, pedido))
                conn.commit()
                flash('✅ Pedido enviado con éxito. Te llamaremos pronto.', 'success')
        except Exception as e:
            print(f"❌ Error al guardar pedido: {e}")
            flash('❌ Error interno al procesar tu pedido.', 'error')
        finally:
            conn.close()

    return render_template('delivery.html', loggedin=loggedin, nombre=nombre)

# ----------------------------------------------------------------------
# 🔹 RUTA DE RESERVAS
# ----------------------------------------------------------------------
@app.route('/reservadf', methods=['GET', 'POST'])
def reserva():
    loggedin = session.get('loggedin', False)
    nombre_usuario = session.get('nombre')

    message = None
    success = False

    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        nombre = request.form.get('nombre')
        celular = request.form.get('celular')
        cantidad_personas = request.form.get('cantidad_personas')
        mensaje = request.form.get('mensaje')

        conn = get_db_connection()
        if conn is None:
            message = 'Error de conexión a la base de datos. Inténtalo más tarde.'
        else:
            try:
                with conn.cursor() as cursor:
                    sql = """
                    INSERT INTO Reservas (fecha, hora, nombre, celular, cantidad_personas, mensaje, usuario_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    usuario_id = session.get('id', None)
                    cursor.execute(sql, (fecha, hora, nombre, celular, cantidad_personas, mensaje, usuario_id))
                    conn.commit()
                    message = '✅ ¡Reserva confirmada con éxito! Te esperamos.'
                    success = True
            except Exception as e:
                print(f"❌ Error al registrar la reserva: {e}")
                message = '❌ Error interno al procesar la reserva.'
            finally:
                conn.close()

    return render_template('reservadf.html',
                           message=message,
                           success=success,
                           loggedin=loggedin,
                           nombre=nombre_usuario)

# ----------------------------------------------------------------------
# 🔹 FORMULARIO DE SUSCRIPCIÓN
# ----------------------------------------------------------------------
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn is None:
            return "Error de conexión a la base de datos."

        try:
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            dni = request.form['dni']
            correo = request.form['correo']
            telefono = request.form['telefono']

            with conn.cursor() as cursor:
                sql = """
                INSERT INTO Suscriptores (nombre, apellidos, dni, correo, telefono)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre, apellidos, dni, correo, telefono))
                conn.commit()

            return redirect(url_for('registro', message='¡Suscripción exitosa! Crea tu cuenta para acceder a la experiencia completa.'))

        except Exception as e:
            print("❌ Error al guardar los datos:", e)
            return "Error al guardar en la base de datos."
        finally:
            conn.close()

    return render_template('formulario.html',
                           loggedin=session.get('loggedin', False),
                           nombre=session.get('nombre'))

# ----------------------------------------------------------------------
# 🔹 TEST DE CONEXIÓN A BD
# ----------------------------------------------------------------------
@app.route('/test-db')
def test_db():
    conn = get_db_connection()
    if conn is None:
        return "❌ Error al conectar con la base: Revisa los logs."
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM Usuarios;")
            resultado = cursor.fetchone()
        return f"✅ Conexión exitosa. Usuarios registrados: {resultado['total']}"
    except Exception as e:
        return f"❌ Error al consultar la base: {e}"
    finally:
        conn.close()

# ----------------------------------------------------------------------
# 🚀 EJECUTAR SERVIDOR
# ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)