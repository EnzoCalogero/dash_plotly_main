import os
import subprocess
from flask import Flask, request, redirect, url_for,render_template
from werkzeug import secure_filename
from external_functions import dictDB

UPLOAD_FOLDER = '/home/enzo/enzo-main/testing/database/tech_view/'
#UPLOAD_FOLDER = '/tmp/enzo/'

LOCAL_FOLDER='/home/enzo/dashboard-analytics/TechoutDockerBuilder/'

ALLOWED_EXTENSIONS = set(['sql'])



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=['get'])
def index():
    return render_template('home.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':
        file = request.files['file']
        tags_name = request.form['tags_name']
        print(tags_name)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            subprocess.Popen(["{}do_IT.sh {}".format(LOCAL_FOLDER,tags_name)], shell=True)
            return redirect(url_for('index'))

    return """
    <!doctype html>
    <title>Upload new Database</title>
    <h1>Upload New DB</h1>
    <a href="list_db">list Databases</a>
    <form action="" method=post enctype=multipart/form-data>
      <p>Database to be uploaded<br> <input type=file name=file>
      <p>Tag for the Docker Techout:<br> <input type=text name=tags_name>
      <p><input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


################################################
## Build interface for the customer databases  #
################################################
@app.route("/list_db", methods=['GET'])
def list_db():
    df=dictDB()
    df.set_index(['DB'],inplace=True)
    df.index.name=None

    return render_template('listDB.html', tables=[df.to_html(classes='Databases',escape=False)],titles=['DB'])


@app.route("/builder", methods=['POST'])
def builder():
    if request.method == 'POST':
        result = request.form
        file = result['file']
        tag=result['tag']
        subprocess.Popen(["{}pre_do_it.sh {} {} > {}log.txt 2>{}err.txt ".format(LOCAL_FOLDER,file, tag,LOCAL_FOLDER,LOCAL_FOLDER)], shell=True)
    return redirect(url_for('index'))


@app.route("/dockertemplate", methods=['get'])
def docker_template():
    text = open('/home/enzo/dashboard-analytics/TechoutDockerBuilder/static/docker-compose.yml', 'r+')
    content = text.read()
    text.close()
    return render_template('content.html', text=content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)


