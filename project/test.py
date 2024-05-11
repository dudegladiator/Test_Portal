from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
import json
import random

with open('questions.json', 'r') as f:
    questions = json.load(f)
    questions_copy = questions.copy()
    
with open('admin.json', 'r') as f:
    admin = json.load(f)    

test = Blueprint('test', __name__)

current_index = random.choice(list(questions.keys()))
result = {}
total_score = 0


@test.route('/test')
@login_required
def test_page():
    global questions, questions_copy, admin
    print(session.get('change'))
    if(session.get('change') == True):
        session['startTime'] = None
        session['total_time'] = None
        session['change'] = False
        with open('questions.json', 'r') as f:
            questions = json.load(f)
            questions_copy = questions.copy()
        
        with open('admin.json', 'r') as f:
            admin = json.load(f)    
    
    time_limit = admin["default"]["time_limit"]
    
    if session.get("total_time") is None:
        session['total_time'] = admin["default"]["time_limit"]*admin["default"]["total_questions"]
    else:
        time_limit = time_limit if session['total_time'] >= 60 else session['total_time']
    
    questions[current_index]['options'] = random.sample(questions[current_index]['options'], len(questions[current_index]['options']))  
    
    return render_template('test.html', question=questions[current_index], time_limit = time_limit)

@test.route('/answer', methods=['POST'])
@login_required
def answer():
    global current_index, total_score, questions, questions_copy, result
    
    print(request.form)
    
    if(request.form.get('answer')):
        answer = request.form.get('answer')
    else:
        answer = ''
    
    if (request.form.get('timeLeft') != ''):
        session['total_time'] = int(session['total_time']) + int(request.form.get('timeLeft')) - int(admin["default"]["time_limit"])
    print(session['total_time'])
    
    
    if(questions[current_index]['correct_answer'] == answer):
        result[current_index] = {
            'question': questions[current_index]['question'],
            'your_answer': answer,
            'correct_answer': questions[current_index]['correct_answer'],
            'score' : questions[current_index]['score']
        }
        total_score = total_score + questions[current_index]['score']
        print('Correct!')
    else:
        result[current_index] = {
            'question': questions[current_index]['question'],
            'your_answer': answer,
            'correct_answer': questions[current_index]['correct_answer'],
            'score' : questions[current_index]['negative_score']
        }
        total_score = total_score - questions[current_index]['negative_score']
        print('Incorrect!')
    
    if(session['total_time'] <= 0):
        return redirect(url_for('test.submit'))
    
    del questions[current_index]
    
    if len(questions) == 0:
        return redirect(url_for('test.submit'))
    
    current_index = random.choice(list(questions.keys()))
    
    return redirect(url_for('test.test_page'))


@test.route('/submit')
@login_required
def submit():
    global total_score
    global questions
    global current_index
    global questions_copy
    global result
    
    session['total_time'] = None
    questions = questions_copy.copy()
    
    current_index = random.choice(list(questions.keys()))
    score_copy = total_score
    total_score = 0
    result_copy = result
    result = {}
    return render_template('submit.html', total_score=score_copy, result=result_copy)