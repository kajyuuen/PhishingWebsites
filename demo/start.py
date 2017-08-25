from bottle import route, run, template, request, response, redirect

@route('/fishfish-abunaiabunai-kikenkiken.con')
def demo(name='unknown'):
    return template('demo')

run(host='localhost', port=8080, debug=True, reloader=True)
