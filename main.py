from flask import Flask, render_template, url_for, redirect, request
from flask_httpauth import HTTPBasicAuth
from test import Test
from question import Question

app = Flask(__name__) # instantiate class with name module

auth = HTTPBasicAuth() # instantiate authentication class

@app.route('/')
def hello_world():
    return redirect('/homepage')

@app.route('/homepage')
def get_homepage():
    return render_template('homepage.html')

@app.route('/questions', methods=['GET'])
def show_questions():
	return render_template('questions.html', questions=Question.get_all())

@app.route('/new/question', methods=['GET', 'POST'])
def new_question():
	if request.method == 'GET':
		return render_template('new_question.html')
	elif request.method == 'POST':
		Question(None,
			request.form['question'],
			[request.form['answer_one'], request.form['answer_two'], request.form['answer_three']],
			request.form['correct_answer']).create()
			
		return redirect('/questions')
		

@app.route('/tests', methods=['GET'])
def show_tests():
	return render_template('tests.html', tests=Test.get_all())	# call static method get_all(), which returns the desired list

@app.route('/new/test', methods=['GET', 'POST'])
def new_test():
	if request.method == 'GET':
		return render_template('new_test.html', questions=Question.get_all())
	elif request.method == 'POST':
		# create a tuple containing all of the needed information given from new_test
		# id is none because it is autoincrement
		values = (
			request.form['title'],
			[Question.find(request.form['question_one']), # 99% sure to bug out??
				Question.find(request.form['question_two']), # request.form[] returns the value of select element (id)
				Question.find(request.form['question_three'])], # we use find() with the id to get the object we need
			None,
		)

		Test(*values).create()
		return redirect('/tests')
		# instantiate a Test object by passing the tuple's values individually with *
		# then insert into the database with the static method create() here


# takes the reference parameter
# define class inside html (with name message) with current instance
@app.route('/test/<int:id>', methods=['GET'])
def show_test(id):
	# implement corner case where ID is not in table -> exception
	test = Test.find(id) # get instance dependent on id
	return render_template('test.html', test=test)

if __name__ == '__main__':
	app.run()

