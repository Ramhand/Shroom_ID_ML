from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
with open('../models/fun_guy.dat', 'rb') as file:
    model = pickle.load(file)
class_dict = {'0': 'probably eat this if you want to.  Seems edible.',
              '1': 'not eat this.  I\'m warning you.  This is only a one up if you believe in reincarnation.'}
columns = ['odor', 'gill-attachment', 'gill-size', 'stalk-surface-below-ring', 'stalk-color-above-ring',
           'spore-print-color', 'population']



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        values = {}
        for i in columns:
            values[i] = 0
            i += '_'
            j = request.form.get(i)
            values[i[:-1]] = j
        new = [[values[i] for i in columns]]
        prediction = str(model.predict(new)[0])
        pred_class = class_dict[prediction]
    else:
        pred_class = None
    return render_template('index.html', prediction=pred_class)
