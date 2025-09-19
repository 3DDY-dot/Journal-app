from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<JournalEntry {self.title}>'

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = JournalEntry.query.order_by(JournalEntry.date_created.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        entry_title = request.form['title']
        entry_content = request.form['content']
        new_entry = JournalEntry(title=entry_title, content=entry_content)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your entry.'
    else:
        return render_template('add_entry.html')

if __name__ == '__main__':
    app.run(debug=True)
