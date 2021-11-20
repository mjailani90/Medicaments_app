from flask import Flask


app = Flask(__name__)


app.config['SECRET_KEY'] = '123456'


# database.db.init_app(app)




# app.run(port=8080, host="0.0.0.0", debug=True)

# app.run() 