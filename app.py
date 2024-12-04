from flask import Flask, request, render_template, jsonify, Request
from conexionBD import obtener_conexion

app = Flask(__name__)

# Ruta principal (Inicio)
@app.route('/')
def inicio():
    return render_template('index.html')

# Crear un nuevo lugar (INSERTAR)
@app.route('/insertar', methods=['GET', 'POST'])
def insertar_lugar():
    if request.method == 'POST':
        tipoLugar = request.form['tipoLugar']
        nombreLugar = request.form['nombreLugar']
        calificacionLugar = int(request.form['calificacionLugar'])
        resenaLugar = request.form['resenaLugar']
        ubicacionLugar = request.form['ubicacionLugar']

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO lugar (tipoLugar, nombreLugar, calificacionLugar, resenaLugar, ubicacionLugar)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (tipoLugar, nombreLugar, calificacionLugar, resenaLugar, ubicacionLugar))
        conexion.commit()
        conexion.close()

        # Mensaje de éxito
        mensaje = "Lugar insertado correctamente."
        return render_template('insertar.html', mensaje=mensaje)

    return render_template('insertar.html')

# Consultar lugares (LECTURA)
@app.route('/consultar', methods=['GET'])
def consultar_lugar():
    idResena = request.args.get('idResena', '')
    tipoLugar = request.args.get('tipoLugar', '')
    calificacionLugar = request.args.get('calificacionLugar', '')
    resenaLugar = request.args.get('resenaLugar', '')
    ubicacionLugar = request.args.get('ubicacionLugar', '')

    query = "SELECT * FROM lugar WHERE 1=1"
    params = []

    if tipoLugar:
        query += " AND tipoLugar LIKE %s"
        params.append('%' + tipoLugar + '%')
    if calificacionLugar:
        query += " AND calificacionLugar = %s"
        params.append(calificacionLugar)
    if idResena:
        query += " AND idResena = %s"
        params.append(idResena)
    if resenaLugar:
        query += " AND resenaLugar = %s"
        params.append(resenaLugar)
    if ubicacionLugar:
        query += " AND ubicacionLugar = %s"
        params.append(ubicacionLugar)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(query, params)
    lugares = cursor.fetchall()
    conexion.close()

    #print(lugares)  # Verifica qué datos se están obteniendo
    return render_template('consultar.html', lugares=lugares)

# Borrar lugar (DELETE)
@app.route('/borrar', methods=['GET', 'POST'])
def borrar_lugar():
    if request.method == 'POST':
        idResena = request.form['idResena']

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = "DELETE FROM lugar WHERE idResena = %s"
        cursor.execute(consulta, (idResena,))
        conexion.commit()
        conexion.close()

    return render_template('borrar.html')

# Actualizar lugar (UPDATE)
@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar_lugar():
    if request.method == 'POST':
        idResena = request.form['idResena']
        tipoLugar = request.form['tipoLugar']
        nombreLugar = request.form['nombreLugar']
        calificacionLugar = int(request.form['calificacionLugar'])
        resenaLugar = request.form['resenaLugar']
        ubicacionLugar = request.form['ubicacionLugar']

        conexion = obtener_conexion()
        cursor = conexion.cursor()
        consulta = """
            UPDATE lugar
            SET tipoLugar = %s, nombreLugar = %s, calificacionLugar = %s,
                resenaLugar = %s, ubicacionLugar = %s
            WHERE idResena = %s
        """
        cursor.execute(consulta, (tipoLugar, nombreLugar, calificacionLugar, resenaLugar, ubicacionLugar, idResena))
        conexion.commit()
        conexion.close()

    return render_template('actualizar.html')

# Consultar lugares (JSON)
@app.route('/resena', methods=['GET'])
def resena_lugar():
    idResena = request.args.get('idResena', '')
    tipoLugar = request.args.get('tipoLugar', '')
    calificacionLugar = request.args.get('calificacionLugar', '')
    resenaLugar = request.args.get('resenaLugar', '')
    ubicacionLugar = request.args.get('ubicacionLugar', '')

    query = "SELECT * FROM lugar WHERE 1=1"
    params = []

    if tipoLugar:
        query += " AND tipoLugar LIKE %s"
        params.append('%' + tipoLugar + '%')
    if calificacionLugar:
        query += " AND calificacionLugar = %s"
        params.append(calificacionLugar)
    if idResena:
        query += " AND idResena = %s"
        params.append(idResena)
    if resenaLugar:
        query += " AND resenaLugar = %s"
        params.append(resenaLugar)
    if ubicacionLugar:
        query += " AND ubicacionLugar = %s"
        params.append(ubicacionLugar)

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(query, params)
    lugares = cursor.fetchall()
    conexion.close()

    # Excluir el campo 'idResena' de los resultados
    for lugar in lugares:
        lugar.pop('idResena', None)

    # Retornar los resultados como JSON
    return jsonify(lugares)

# Consultar lugares por tipo
@app.route('/resena/tipo', methods=['GET'])
def resena_por_tipo():
    tipoLugar = request.args.get('tipoLugar', '')

    if not tipoLugar:
        return jsonify({"error": "Debes proporcionar un tipo de lugar."}), 400

    query = "SELECT * FROM lugar WHERE tipoLugar LIKE %s"
    params = ['%' + tipoLugar + '%']

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(query, params)
    lugares = cursor.fetchall()
    conexion.close()

    # Excluir el campo 'idResena' de los resultados
    for lugar in lugares:
        lugar.pop('idResena', None)

    return jsonify(lugares)

# Consultar lugares por calificación
@app.route('/resena/calificacion', methods=['GET'])
def resena_por_calificacion():
    calificacionLugar = request.args.get('calificacionLugar', '')

    if not calificacionLugar.isdigit() or not (0 <= int(calificacionLugar) <= 5):
        return jsonify({"error": "Debes proporcionar una calificación válida (entre 0 y 5)."}), 400

    query = "SELECT * FROM lugar WHERE calificacionLugar = %s"
    params = [calificacionLugar]

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(query, params)
    lugares = cursor.fetchall()
    conexion.close()

    # Excluir el campo 'idResena' de los resultados
    for lugar in lugares:
        lugar.pop('idResena', None)

    return jsonify(lugares)

@app.route('/reseno/<string:nombreLugar>')
def getProduct(nombreLugar):
    print(nombreLugar)
    print(request.json)
    return "recived"

if __name__ == '__main__':
    app.run(port=4000, debug=True)
