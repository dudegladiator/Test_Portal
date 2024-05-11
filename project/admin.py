from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_required, current_user
import json

admin = Blueprint('admin', __name__)

with open('questions.json', 'r') as f:
    questions = json.load(f)
    
with open('admin.json', 'r') as f:
    admin_content = json.load(f)
    
def save_files(content, filename):
    with open(filename, 'w') as f:
        json.dump(content, f)

@admin.route('/')
@login_required
def admin_page():
    if(current_user.urole != 'admin'):
        return redirect(url_for('dashboard.dashboard1'))
    return render_template('admin_dashboard.html', questions=questions, admin=admin_content)


@admin.route('/update', methods=['POST'])
@login_required
def update():
    global questions
    global admin_content
    if(current_user.urole != 'admin'):
        return redirect(url_for('dashboard.dashboard1'))
    # print(request.form)
    
    time_limit = request.form['time_limit']
    
    new_questions = request.form.getlist('question')
    new_options = request.form.getlist('options')
    new_answer = request.form.getlist('correct_answer')
    new_score = request.form.getlist('score')
    new_negative_score = request.form.getlist('negative_score')
    print(len(new_questions), len(new_options), len(new_answer), len(new_score), len(new_negative_score))
    new_dict = {}
    
    for i in range(len(new_questions)):
        options = []
        for j in new_options[i].split(','):
            options.append(j)
        if(new_answer[i] not in options or len(options) < 2):
            continue
        try:
            new_dict[i+1] = {
                "question": new_questions[i],
                "options": options,
                "correct_answer": new_answer[i],
                "score": int(new_score[i]),
                "negative_score": int(new_negative_score[i])
            }
        except:
            continue
    print(new_dict)
    try:
        admin_content["default"]["time_limit"] = int(time_limit)
        admin_content["default"]["total_questions"] = len(new_dict)
        questions = new_dict
        save_files(new_dict, 'questions.json')
        save_files(admin_content, 'admin.json')
        session['change'] = True
    except:
        pass    
    return redirect(url_for('admin.admin_page'))
