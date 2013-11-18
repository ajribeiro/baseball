from flask import Flask, render_template, jsonify,  \
            request, make_response
from mongokit import Connection
import json

# configuration
MONGODB_HOST = 'sd-work2.ece.vt.edu'
MONGODB_PORT = 27017


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/_noop')
def _noop():
    return jsonify(result=1)


@app.route('/_read_db_proj')
def _read_db_proj():
    a = request.args.get('name', 0, type=str)
    # connect to the database
    connection = Connection(app.config['MONGODB_HOST'],
                            app.config['MONGODB_PORT'])
    collection = connection['baseball'].player_proj
    qry = collection.find({'name':a})
    qry = [{'name':q['name'], \
            'projs':q['projs']} for q in qry]
    return jsonify(result=qry)


@app.route('/_read_db_sim')
def _read_db_sim():
    a = request.args.get('name', 0, type=str)
    # connect to the database
    connection = Connection(app.config['MONGODB_HOST'],
                            app.config['MONGODB_PORT'])
    collection = connection['baseball'].player_dists_car
    qry = collection.find({'player1':a}).sort('dist')[:50]
    qry = [{'player1':q['player1'], \
            'player2':q['player2'], \
            'dist':q['dist']} for q in qry]
    return jsonify(result=qry)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.debug=True
    app.run()
    