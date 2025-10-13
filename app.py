from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# 🧩 Conexión a tu base de datos en AWS RDS
try:
    conexion = pymysql.connect(
        host='angello.c1jh3g8aqs0w.us-east-1.rds.amazonaws.com',  # endpoint correcto
        user='admin',
        password='angello1234',
        database='dbangello',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✅ Conexión exitosa con la base de datos dbangello")
except Exception as e:
    print("❌ Error al conectar con la base de datos:", e)

# 🔹 Ruta raíz
@app.route('/')
def index():
    return redirect(url_for('inicio'))

# 🔹 Página de inicio
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# 🔹 Página de carta
@app.route('/nuestra-carta')
def cartas():
    return render_template('cartas.html')

# 🔹 Página de historia
@app.route('/nuestra-historia')
def historia():
    return render_template('historia.html')

# 🔹 Página del formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            dni = request.form['dni']
            correo = request.form['correo']
            telefono = request.form['telefono']

            print(f"📨 Datos recibidos del formulario: {nombre}, {apellidos}, {dni}, {correo}, {telefono}")

            with conexion.cursor() as cursor:
                sql = """
                INSERT INTO Suscriptores (nombre, apellidos, dni, correo, telefono)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre, apellidos, dni, correo, telefono))
                conexion.commit()

            print("✅ Registro insertado correctamente en la base de datos")
            return redirect(url_for('confirmar_suscripcion'))

        except Exception as e:
            print("❌ Error al guardar los datos:", e)
            return "Error al guardar en la base de datos. Revisa la consola."
    else:
        return render_template('formulario.html')

# 🔹 Página de confirmación
@app.route('/suscripcion-exitosa')
def confirmar_suscripcion():
    return render_template('confirmacion_suscripcion.html')

# 🔹 Test de conexión directa desde Flask
@app.route('/test-db')
def test_db():
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS total FROM Suscriptores;")
            resultado = cursor.fetchone()
        return f"✅ Conexión exitosa. Registros actuales: {resultado['total']}"
    except Exception as e:
        return f"❌ Error al conectar con la base: {e}"

# 🚀 Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)
