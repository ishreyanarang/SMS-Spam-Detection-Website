from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import pickle

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session management

# Load the pre-trained model and vectorizer
model = pickle.load(open('spam_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

@app.route('/')
def home():
    # Check if the user is logged in
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple validation (replace with a database in production)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        message = data.get('message', '')

        # Vectorize the message
        vectorized_message = vectorizer.transform([message])

        # Predict using the model
        prediction = model.predict(vectorized_message)[0]
        confidence = max(model.predict_proba(vectorized_message)[0]) * 100

        result = 'Spam' if prediction == 1 else 'Ham'

        return jsonify({'result': result, 'confidence': round(confidence, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login')
def login():
    return render_template('login.html')

