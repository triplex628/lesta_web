import re
from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for
from .tfidf_utils import compute_tfidf

bp = Blueprint('tfidf', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or not f.filename.lower().endswith('.txt'):
            return render_template('index.html', error="Пожалуйста, загрузите .txt файл")
        text = f.read().decode('utf-8', errors='ignore')
        session['raw_text'] = text
        session['filename'] = f.filename
        return redirect(url_for('tfidf.result'))
    return render_template('index.html')

@bp.route('/result')
def result():
    text = session.get('raw_text')
    if not text:
        return redirect(url_for('tfidf.index'))
    filename = session.get('filename', '—')

    page     = max(int(request.args.get('page', 1)), 1)
    per_page = int(request.args.get('per_page', 20))

    tf, idf = compute_tfidf(text)
    sorted_words = sorted(tf.keys(), key=lambda w: idf[w], reverse=True)
    total = len(sorted_words)

    start = (page - 1) * per_page
    end   = start + per_page
    page_words = sorted_words[start:end]

    table = [
        {"word": w, "tf": tf[w], "idf": round(idf[w], 4)}
        for w in page_words
    ]

    return render_template('result.html',
                           table=table,
                           page=page,
                           per_page=per_page,
                           total=total,
                           filename=filename)
