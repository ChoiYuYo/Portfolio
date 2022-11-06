import flask
from flask import Flask, request, render_template
from sklearn.externals import joblib
import numpy as np
from scipy import misc

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return flask.render_template('index.html')


@app.route('/predict', methods=['POST'])
def make_prediction():
    if request.method == 'POST':
        file = request.files['image']
        if not file: return render_template('index.html', label="No Files")

        img = misc.imread(file)
        img = img[:, :, :3]
        img = img.reshape(1, -1)

        prediction = model.predict(img)

        label = str(np.squeeze(prediction))

        if label == '10' : label = '0'

        return render_template('index.html', label=label)

if __name__ == '__name__':
    model = joblib.load('./model/model.pkl')

    app.run(host='0.0.0.0', port=80000, debug=True)