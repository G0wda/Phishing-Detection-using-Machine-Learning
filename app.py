from flask import Flask, render_template, request, url_for
import pickle 

vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/detect', methods=['POST'])
def detect():
    if request.method == "POST":
        url = request.form['url']
        print(url)

        result = model.predict(vector.transform([url]))
        return render_template("detect.html",result=result)
    else:
        return render_template("404.html")






if __name__ == "__main__":
    app.run(debug=True)

