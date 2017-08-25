from bottle import route, run, template, request, response, redirect
import measure

@route('/fishfish-abunaiabunai-kikenkiken.con')
def demo(name='unknown'):
    return template('demo')

@route('/index.html')
def index():
    return template('index')

@route('/result.html')
def result():
    url = request.query.url
    persent = measure.measure(url)
    return template('result', persent=persent)
run(host='localhost', port=8080, debug=True, reloader=True)
