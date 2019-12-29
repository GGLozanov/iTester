from database import DB
from question import Question
from typing import List 

class Test:	

	def __init__(self, title, questions: List[Question], test_id):
		self.title = title
		self.questions = questions
		self.test_id = test_id
		self.correct_answers: List[bool] = [ans < 0 for ans in questions] # create a 'False' boolean list w/list comprehension
	
	def check_test(self):
		for q in questions:
			correct_answers[q] = q.is_answer_correct() # set whether current question is correct
	
	def set_answers(self, answers: List[str]): # answer amount should be identical to question amount
		if answers.size() != questions.size():
			return False
		for q in questions:
			q.set_answer(answers[q]) # set answer of question to one given (will be garnered through requests and made into list)

	def create(self):
		with DB() as database:
			database.execute('''
				INSERT INTO tests (title, test_id)
				VALUES (?, ?)''', (self.title, self.test_id))

			# might have to delete these insertions since they are done by question create method (?)
			# have to find question by id here?
#			for q in self.questions:
#				database.execute('''
#					INSERT INTO questions (id, question, correct_answer_index)
#					VALUES(?, ?, ?)''',  (q.id, q.question, q.correct_answer))
#				for ans in self.questions.answers:
#					database.execute('''
#					INSERT INTO answers (id, answer)
#					VALUES(?, ?)''', (self.questions.answers.index(ans), ans)) # index + answer tuple (index = id)
#			return self

	@staticmethod
	def get_all():
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
