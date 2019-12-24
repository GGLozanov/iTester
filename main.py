from flask import Flask, render_template, url_for, redirect, request
from flask_httpauth import HTTPBasicAuth
from test import Test
from question import Question

app = Flask(__name__) # instantiate class with name module

auth = HTTPBasicAuth() # instantiate authentication class

@app.route('/')
def hello_world():
    return redirect('/main')

@app.route('/hello', methods=['GET'])
def print_hello():
    return render_template('homepage.html')

@app.route('/tests', methods=['GET'])
def show_tests():
	return render_template('tests.html', tests=Tests.get_all())	# call static method get_all(), which returns the desired list

@app.route('/new/test', methods=['GET', 'POST'])
def new_test():
	if request.method == 'GET':
		return render_template('new_test.html')
	elif request.method == 'POST':
		# create a tuple containing all of the needed information given from new_test
		values = (
			request.form['title'],
			request.form['questions'],
			None,
		)
		Test(*values).create()
		# instantiate a Test object by passing the tuple's values individually with *
		# then insert into the database with the static method create() here


# takes the reference parameter
# define class inside html (witn name message) with current instance
@app.route('/test/<int:id>', methods=['GET'])
def show_test(id):
	# implement corner case where ID is not in table -> exception
	test = Test.find(id) # get instance dependent on id
	return render_template('test.html', test=test)

