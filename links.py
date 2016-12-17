import sqlite3

from flask import Flask
from flask import Response
from flask import redirect, abort, request, url_for, jsonify

from config import *

def connect_db() :
    conn = sqlite3.connect(db_location)
    return conn

http = Flask(__name__)

# @http.route('/')
# def root() :
#     return 'Hello World!'
#
# @http.route('/hijack')
# def hijack() :
#     return redirect('http://index.hu')
#
# @http.route('/hiba')
# def hiba() :
#     return abort(401)
#
# @http.route('/reverse/<chosen>')
# def reverse(chosen) :
#     return Response(chosen [::-1])

@http.route('/<id>')
def lookup(id) :
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('''SELECT url FROM links WHERE id = ?''', (id, ))
    url = cur.fetchone()[0]
    conn.close()
    return redirect(url)

@http.route('/shorten')
def shorten() :
    try :
        url = request.args['url']
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('''SELECT id FROM links WHERE url = ?''', (url, ))
        record = cur.fetchone()
        if record == None :
            cur.execute('''INSERT INTO links(url) VALUES(?)''', (url, ))
            id = cur.lastrowid
        else :
            id = record[0]
        conn.commit()
        conn.close()
        result = { 'original': url, 'shortened': url_for('lookup', id = id) }
        return jsonify(result)
    except Exception as e :
        report = { 'message': str(e) }
        return jsonify(report)

if __name__ == '__main__' :
    http.run()
