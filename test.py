from database import DB
from question import Question
from typing import List
from adapter import Adapter

class Test:
	def __init__(self, id: int, questions: List[Question], title: str):
		self.title = title
		self.questions = questions
		self.id = id
		self.correct_answers: List[bool] = [False for _ in range(len(questions))] # create a 'False' boolean list w/list comprehension
	
	def check_test(self):
		for question in questions:
			correct_answers[question] = question.is_answer_correct() # set whether current question is correct
	
	def set_answers(self, answers: List[str]): # answer amount should be identical to question amount
		if answers.size() != questions.size():
			return False
			
		for question in questions:
			question.set_answer(answers[question]) 
			# set answer of question to one given (will be garnered through requests and made into list)

	def create(self):
		with DB() as database:
			database.execute('''
				INSERT INTO tests (id, questions_id, title)
				VALUES (?, ?, ?)''', (self.id, self.id, self.title))
				
			print(self.questions)
			for question in self.questions:
			
				if not isinstance(question.find(question.id), Question): 
					question.create()
					
					
			return self

	@staticmethod
	def get_all():
		with DB() as database:
			rows = database.execute('''SELECT * FROM tests''').fetchall() # fetches all rows which correspond to the query (i.e. every row)
			
			print(Question.get_all())

			rows = Adapter.adapt_test_rows(database, Adapter.adapt_query(rows), Question.get_all()) 
			# new rows is result of adapted method return value 
			# adapt query converts list of tuples into list of lists
			print(rows)			
			
			return [Test(*row) for row in rows] 
			# for each row in the data, instantiate a class with the values from the table
			# and return them all as a list

	@staticmethod
	def find(id):
		with DB() as database:
			row = Adapter.adapt_query(database.execute('''SELECT * FROM tests WHERE id = ?''', (id,)).fetchall())
			# rather banal back-and-forth type conversion from list of tuples to list of lists
			
			row = tuple(Adapter.adapt_test_rows(database, row, Question.get_all())[0])
			
			# fetch a single row where id is given id
			# sql queries take tuples, which is why we pass arguments in such a manner
			
			print(row)
			
			return Test(*row) # return new instance of Test() where we pass the elements of the container as args
