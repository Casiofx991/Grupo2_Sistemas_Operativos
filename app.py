from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="########",
        user="########",
        password="########",
        database="########",
    )

@app.route('/')
def index():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM canciones")
    songs = cursor.fetchall()
    connection.close()
    return render_template('index.html', songs=songs)

@app.route('/add_song', methods=['POST'])
def add_song():
    titulo = request.form['titulo']
    compositor = request.form['compositor']
    interprete = request.form['interprete']
    periodo = request.form['periodo']
    duracion = request.form['duracion']
    
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO canciones (titulo, compositor, interprete, periodo, duracion) VALUES (%s, %s, %s, %s, %s)", (titulo, compositor, interprete, periodo, duracion))
    connection.commit()
    connection.close()
    
    return redirect(url_for('index'))

@app.route('/modify_song/<int:song_id>', methods=['POST'])
def modify_song(song_id):
    titulo = request.form['titulo']
    compositor = request.form['compositor']
    interprete = request.form['interprete']
    periodo = request.form['periodo']
    duracion = request.form['duracion']

    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("UPDATE canciones SET titulo = %s, compositor = %s, interprete = %s, periodo = %s, duracion = %s WHERE id = %s", (titulo, compositor, interprete, periodo, duracion, song_id))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))

@app.route('/delete_song/<int:song_id>')
def delete_song(song_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM canciones WHERE id = %s", (song_id,))
    connection.commit()
    connection.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
