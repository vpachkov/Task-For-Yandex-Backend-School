from manage import db

@app.route('/imports', methods=['POST'])
def imports():
    citizens = request.json
