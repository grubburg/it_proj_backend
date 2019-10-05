from objectify import create_app

app = create_app()


################ ROUTES ###############
"""
Base route. TODO: replace with something meaniful
"""
@app.route('/')
def hello_world():
    return "compu-global-hyper-mega-net was here!"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
