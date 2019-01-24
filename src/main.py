from flask import Flask, render_template
import random
import urllib2

app = Flask(__name__)

@app.route('/')
def hello_world():
    """GET endpoint to return Hello world"""
    try:
       instanceid = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id', timeout=1).read()
    except:
       return render_template('index.html'), 200
    return render_template('index.html', instanceid=instanceid), 200

@app.errorhandler(404)
def page_not_found(e):
    animals = [
        'https://rlv.zcache.com/sad_panda_square_sticker-rc8d7c3fe2f3a44d3a3912e265eb2cc17_v9wf3_8byvr_552.jpg',
        'https://media.makeameme.org/created/sad-cat-5b6c0d.jpg',
        'http://fixmyracquet.com/wp-content/uploads/2016/07/photo-Sad-Puppy-Face-in-Blanket-768x512.jpg'
    ]
    return render_template('404.html', sad_animal=random.choice(animals)), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)