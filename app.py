from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',  # Dejar vacío si no has configurado una contraseña
    'database': 'restaurant_db_new'
}

# Configuración de carga de archivos
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    try:
        connection = pymysql.connect(**db_config)
        print("Connected to MySQL database")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
        return None




@app.route('/add_restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        province = request.form['province']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        phone = request.form['phone']
        website = request.form['website']
        image = None

        # Manejo de carga de imagen
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO restaurants (name, address, province, latitude, longitude, phone, website, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                               (name, address, province, latitude, longitude, phone, website, image))
                conn.commit()
                cursor.close()
            except pymysql.MySQLError as e:
                print(f"Error executing query: {e}")
            finally:
                conn.close()
            return redirect('/restaurants')
        else:
            return "Error connecting to the database"
    return render_template('add_restaurant.html')

@app.route('/edit_restaurant/<int:id>', methods=['GET', 'POST'])
def edit_restaurant(id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        province = request.form['province']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        phone = request.form['phone']
        website = request.form['website']
        image = request.form.get('existing_image')
        
        # Manejo de carga de imagen
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image = filename

        try:
            cursor = conn.cursor()
            cursor.execute('UPDATE restaurants SET name=%s, address=%s, province=%s, latitude=%s, longitude=%s, phone=%s, website=%s, image=%s WHERE id=%s',
                           (name, address, province, latitude, longitude, phone, website, image, id))
            conn.commit()
            cursor.close()
        except pymysql.MySQLError as e:
            print(f"Error executing query: {e}")
        finally:
            conn.close()
        return redirect('/restaurants')
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM restaurants WHERE id = %s', (id,))
    restaurant = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_restaurant.html', restaurant=restaurant)

@app.route('/delete_restaurant/<int:id>', methods=['POST'])
def delete_restaurant(id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM restaurants WHERE id = %s', (id,))
        conn.commit()
        cursor.close()
    except pymysql.MySQLError as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()
    return redirect('/restaurants')

@app.route('/restaurants')
def restaurants():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurants')
        restaurants = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('restaurants.html', restaurants=restaurants)
    else:
        return render_template('error.html', error_message="Error connecting to the database")

@app.route('/restaurantes')
def restaurantes():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM restaurants')
        restaurants = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('restaurantes.html', restaurants=restaurants)
    else:
        return render_template('error.html', error_message="Error connecting to the database")


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Manejador de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message="Página no encontrada"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message="Error interno del servidor"), 500

if __name__ == '__main__':
    app.run(debug=True)
