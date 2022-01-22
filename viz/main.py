import os
import sys
from crawldata import Crawl
import graphcourse as draw
from flask import *

# if sys.argv[1] == '-d': drawlgraph()
# if sys.argv[1] == '-c': crawldata()
# os.system('dot -Tpng input.dot -o output.png')
def drawlgraph():
    for i in range(len(sys.argv)-2):
        try:
            draw.drawone(sys.argv[i+2])
        except:
            print("can't draw " + sys.argv[i+2])
def crawldata():
    Crawl.crawldata()
# if sys.argv[1] == '-d': drawlgraph()
# if sys.argv[1] == '-c': crawldata()
# os.system('dot -Tpng input.dot -o output.png')
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
    draw.drawone(course)
    # picture = "./test-output/course"+str(course)+".png"
    # return render_template("picture.html",user_image=picture)
    return download_file("courses"+str(course)+".png")
if __name__ == '__main__':
    app.run(debug=True)

