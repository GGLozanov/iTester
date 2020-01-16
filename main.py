from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from functools import wraps
from flask_httpauth import HTTPBasicAuth
from test import Test
from question import Question
from user import User
from flask import session
import json

app = Flask(__name__)  # instantiate class with name module

auth = HTTPBasicAuth()  # instantiate authentication class

app.secret_key = "OMG EPIC SUPER SECRET KEY! CHECKMATE GUITARISTS!"


def require_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect('/login')

        return func(*args, **kwargs)

    return wrapper


@app.route('/')
def hello_world():
    return redirect('/login')


@app.route('/homepage')
@require_login
def get_homepage():
    return render_template('homepage.html')


@app.route('/questions', methods=['GET'])
@require_login
def show_questions():
    return render_template('questions.html', questions=Question.get_all())


@app.route('/new/question', methods=['GET', 'POST'])
@require_login
def new_question():
    if request.method == 'GET':
        return render_template('new_question.html')
    elif request.method == 'POST':
        Question(None,
                 request.form['question'],
                 [request.form['answer_one'], request.form['answer_two'],
                     request.form['answer_three']],
                 request.form['correct_answer']).create()

        app.logger.info('Question "%s" with answers "%s", "%s", "%s" and correct answer "%s" created successfully',
                        request.form['question'],
                        request.form['answer_one'], request.form['answer_two'], request.form['answer_three'],
                        request.form['correct_answer'])

        return redirect('/questions')


@app.route('/edit/question', methods=['GET', 'POST'])
@require_login
def edit_question():
    if request.method == 'GET':
        return render_template('edit_question.html', questions=Question.get_all())
    elif request.method == 'POST':
        question = Question.find(int(request.form['questions']))

        values = (
            request.form['question'],
            request.form['correct_answer'],
        )

        answers = [
            request.form['answer_one'],
            request.form['answer_two'],
            request.form['answer_three'],
        ]

        question.update(values, answers).edit()
        app.logger.info("question %s was edited succesfully",
                        request.form['question'])
        return redirect('/homepage')


@app.route('/delete/question', methods=['GET', 'POST'])
@require_login
def delete_question():
    if request.method == 'GET':
        return render_template('delete_question.html', questions=Question.get_all())
    elif request.method == 'POST':
        # id is an int, which is why conversion is necessary
        question = Question.find(int(request.form['questions']))

        # delete tests containing the deleted question
        Test.delete_tests_w_deleted_question(question)

        question.delete()
        app.logger.info("question %s was succesfully deleted", request.form['question'])
        return redirect('/homepage')


@app.route('/tests', methods=['GET'])
@require_login
def show_tests():
    # call static method get_all(), which returns the desired list
    return render_template('tests.html', tests=Test.get_all())


@app.route('/new/test', methods=['GET', 'POST'])
@require_login
def new_test():
    if request.method == 'GET':
        return render_template('new_test.html', questions=Question.get_all())
    elif request.method == 'POST':
        # create a tuple containing all of the needed information given from new_test
        # id is none because it is autoincrement

        Test(None,
             [Question.find(int(request.form['question_one'])),  # 99% sure to bug out??
                 # request.form[] returns the value of select element (id)
                 Question.find(int(request.form['question_two'])),
                 Question.find(int(request.form['question_three']))],  # we use find() with the id to get the object we need
             request.form['title']).create()

        app.logger.info('Test "%s" with questions "%s", "%s", "%s" created successfully',
                        request.form['title'],
                        request.form['question_one'], request.form['question_two'], request.form['question_three'])

        return redirect('/tests')
        # instantiate a Test object by passing the tuple's values individually with *
        # then insert into the database with the static method create() here


@app.route('/edit/test', methods=['GET', 'POST'])
@require_login
def edit_test():
    if request.method == 'GET':
        return render_template('edit_test.html', tests=Test.get_all(), questions=Question.get_all())
    elif request.method == 'POST':
        test = Test.find(int(request.form['tests']))

        values = (
            request.form['title']
        )

        questions = [
            Question.find(request.form['question_one']),
            Question.find(request.form['question_two']),
            Question.find(request.form['question_three'])
        ]

        test.update(values, questions).edit()
        app.logger.info("test %s was succesfully edited", request.form['title'])
        return redirect('/homepage')


@app.route('/delete/test', methods=['GET', 'POST'])
@require_login
def delete_test():
    if request.method == 'GET':
        return render_template('delete_test.html', tests=Test.get_all())
    elif request.method == 'POST':
        test = Test.find(int(request.form['tests']))
        test.delete()
        app.logger.info('Test "%s" with questions "%s", "%s", "%s" deleted successfully',
                        test.title,
                        test.questions[0].question, test.questions[1].question, test.questions[2].question)
        return redirect('/homepage')


# takes the reference parameter
# define class inside html (with name message) with current instance
answers = []
@app.route('/test/<int:id>', methods=['GET', 'POST'])
@require_login
def show_test(id):
    test = Test.find(id)  # get instance dependent on id
    if request.method == 'GET':
        # implement corner case where ID is not in table -> exception
        return render_template('test.html', test=test)
    elif request.method == 'POST':
        # implement corner case where ID is not in table -> exception
        # get instance dependent on id
        for question in test.questions:
            answers.append(
                request.form[str(test.questions.index(question) + 1)])

        app.logger.info("tests successfuly rendered")
        return redirect('/test/%d/grade' % id)


@app.route('/test/<int:id>/grade', methods=['GET'])
@require_login
def grade_test(id):
    global answers
    test = Test.find(id)
    test.set_answers(answers)
    test.check_test()
    grade = test.count_correct()
    user = User.find_by_username(session['USERNAME'])
    User.insert_grade(user, grade)
    answers = []
    app.logger.info("test successfuly gradet")
    return render_template('test_grade.html', test=test)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            0
        )
        User(*values).create()
        app.logger.info("user %s successfuly registered", request.form['username'])
        return redirect('/homepage')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        user = User.find_by_username(username)

        if not user or not user.verify_password(password):
            flash("Invalid Login.")
            return redirect('/login')

        session['USERNAME'] = user.username
        session['logged_in'] = True
        app.logger.info("user %s successfuly logged", session['USERNAME'])

        return redirect('/homepage')


@app.route('/logout', methods=["POST"])
def logout():
    session['logged_in'] = False
    session['USERNAME'] = None
    app.logger.info("the current user successfuly logged out") 
    return redirect('/login')


@app.route('/users', methods=['GET'])
@require_login
def show_users():
    return render_template('users.html', users=User.get_all())


if __name__ == '__main__':
    app.run()
