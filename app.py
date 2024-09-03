from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Veritabanı modellerimiz
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    options = db.Column(db.PickleType, nullable=False)  
    answer = db.Column(db.String(100), nullable=False)

# Veritabanını oluşturduk ve gerekli verilerle doldurduk
def initialize_db():
    with app.app_context():
        db.create_all()
        if Question.query.count() == 0:
            questions = [
                {'question': 'Python dilinde AI geliştirme hangi kütüphane ile yapılır?', 'options': ['TensorFlow', 'OpenCV', 'NLTK'], 'answer': 'TensorFlow'},
                {'question': 'Bilgisayar görüşü hangi kütüphane ile yapılır?', 'options': ['Scikit-learn', 'OpenCV', 'Pandas'], 'answer': 'OpenCV'},
                {'question': 'NLP hangi kütüphane ile yapılır?', 'options': ['NumPy', 'NLTK', 'Matplotlib'], 'answer': 'NLTK'}
            ]
            for q in questions:
                question = Question(question=q['question'], options=q['options'], answer=q['answer'])
                db.session.add(question)
            db.session.commit()

# Uygulama başlatıldığında veritabanını başlatmak için tekrardan çağrılmasına gerek kalmamasını sağladık
with app.app_context():
    initialize_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    questions = Question.query.all()
    total_questions = len(questions)
    score = 0
    percentage_score = None

    if request.method == 'POST':
        for i, question in enumerate(questions):
            user_answer = request.form.get(f'question_{i}')
            if user_answer == question.answer:
                score += 1
        
        if total_questions > 0:
            percentage_score = int(round((score / total_questions) * 100))

    return render_template('index.html', questions=questions, score=score, percentage_score=percentage_score, total_questions=total_questions)

if __name__ == '__main__':
    app.run(debug=True)
