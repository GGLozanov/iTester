from database import DB
from question import Question
from typing import List 

class Test:	

	def __init__(self, title, questions: List[Question], test_id):
		self.title = title
		self.questions = questions
		self.test_id = test_id
		self.correct_answers: List[bool] = [ans < 0 for ans in questions] # create a boolean list w/list comprehension
	
	def check_test(self):
		for q in questions:
			correct_answers[q] = q.is_answer_correct() # set whether current question is correct
	
	def set_answers(self, answers: List[str]): # answer amount should be identical to question amount
		if answers.size() != questions.size():
			return False
		for q in questions:
			q.set_answer(answers[q]) # set answer of question to one given (will be garnered through requests and made into list)

	@staticmethod # decorator declaring this as a static method
	def create(self):
		values = (self.title, self.questions, self.test_id)
		with DB() as database:
			database.execute('''
				INSERT INTO tests (title, questions, test_id)
				VALUES (?, ?, ?)''', values)
			return self

	@staticmethod
	def get_all(self):
		with DB() as database:
			data = database.execute('''SELECT * FROM tests''').fetchall() # fetches all rows which correspond to the query (i.e. every row)
			return [Test(*row) for row in data] 
			# for each row in the data, instantiate a class with the values from the table
			# and return them all as a list

	@staticmethod
	def find(id):
		with DB() as database:
			row = database.exectute('''SELECT * FROM tests WHERE test_id = ?''', (id,)).fetchone()
			# fetch a single row where id is given id
			# sql queries take tuples, which is why we pass arguments in such a manner
			return Test(*row) # return new instance of Test() where we pass the elements of the container as args
