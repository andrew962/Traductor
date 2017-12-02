from flask import Flask,render_template,redirect,request
from translate_api.translate_api import api

app = Flask(__name__)
"""

"""
@app.route('/',methods = ['GET'])
def init():
    if request.args.get('text') is None:
        pass
    else:
        text = request.args.get('text')
        siglas = request.args.get('siglas')
        siglas1 = request.args.get('siglas1')
        traductor = api(text,siglas,siglas1)
        print(api(text,siglas,siglas1))
        return render_template('translate.html', traductor=traductor,text = text)
    return render_template('translate.html')

if __name__ == '__main__':
    app.run(debug=True)