from flask import Flask, render_template
from tiktok_app.routes import tiktok_blueprint
from google_app.routes import google_blueprint

app = Flask(__name__)

app.register_blueprint(tiktok_blueprint, url_prefix='/tiktok')
app.register_blueprint(google_blueprint, url_prefix='/google')

@app.route('/')
def home():
    return render_template('index.html')  # Giao diện chọn nguồn dữ liệu

if __name__ == '__main__':
    app.run(debug=True)