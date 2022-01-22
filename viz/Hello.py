from flask import *

app = Flask(__name__)
@app.route('/')
def message():
      return render_template('course.html')
@app.route('/test-output/<path:filename>')
def download_file(filename):
    return send_from_directory("./test-output/",
                               filename, as_attachment=True)
@app.route('/login', methods=['POST'])
def login():
    course = request.form['course']
    return download_file("courses"+str(course)+".png")
if __name__ == '__main__':
    app.run(debug=True)