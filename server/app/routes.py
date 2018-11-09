from app import app

@app.route('/index', methods=['GET', 'POST'])  
@app.route('/', methods=['GET', 'POST'])
def index():
    return "Yo"

