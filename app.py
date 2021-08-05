from flask import Flask,flash,redirect,render_template,request, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_HOST="localhost"
DB_PORT='5433'
DB_NAME='sampledb'
DB_USER='postgres'
DB_PASS='dba'

conn = psycopg2.connect(dbname=DB_NAME,user=DB_USER,password=DB_PASS,host=DB_HOST,port=DB_PORT)

app.secret_key = 'SkillChen_Secret_Key'

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if 'file' not in request.files:
        flash("No File Psrt")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No Image Selected for unloading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename )

        cursor.execute("Insert into upload(title) values(%s)",(filename,))
        conn.commit()

        flash('Image successfully uploaded and displayed below')
        return render_template('index.html', filename=filename)
    else:
        flash("Allowed image types are - png|jpg|jpeg|gif")
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename )
    return redirect(url_for('static',filename='uploads/' + filename), code=301)


if __name__ == '__main__':
    app.run(debug=True)
