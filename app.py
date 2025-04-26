from flask import Flask
from tfidf.views import bp as tfidf_bp
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'LESTA'
Bootstrap(app)

app.register_blueprint(tfidf_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
