from database import DB
from question import Question
from typing import List
from adapter import Adapter

class Test:
	def __init__(self, id = None, questions = [Question() for _ in range(3)], title = "TestTest"):
		self.title = title
		self.questions = questions
		self.prev_questions = None
		self.id = id
		self.correct_answers = [None] * len(questions) # create a list with size answers
		
	def __eq__(self, other):
		if not isinstance(other, Test):
			return NotImplemented
		
		return self.title == other.title
	
	def check_test(self):
		for idx, question in enumerate(self.questions):
			self.correct_answers[idx] = "Correct" if question.is_answer_correct() else "Incorrect"
			# set whether current question is correct
	
	def set_answers(self, answers: List[str]): # answer amount should be identical to question amount
		if len(answers) != len(self.questions):
			return False
			
		for idx, question in enumerate(self.questions):
			question.set_answer(answers[idx]) 
			# set answer of question to one given (will be garnered through requests and made into list)
			
	def count_correct(self):
		return (self.correct_answers.count("Correct") / len(self.correct_answers)) * 100
		
	def count_incorrect(self):
		return (self.correct_answers.count("Incorrect") / len(self.correct_answers)) * 100

	def create(self):
		with DB() as database:
			database.execute('''
				INSERT INTO tests (id, questions_id, title)
				VALUES (?, ?, ?)''', (self.id, self.id, self.title))
					
			for question in self.questions: # int array of question ids to categorise test questions by
				database.execute('''
				INSERT INTO test_questions (id, question_id) VALUES (?, ?)
				''', (self.id, question.id))
				
				database.execute('''UPDATE test_questions
					SET test_id = id WHERE question_id = ?''', (question.id,))
				
			return self
			
	def update(self, values, questions):
		self.title = values
		self.prev_questions = self.questions
		self.questions = questions
	
		return self
		
	def edit(self):
		with DB() as database:
			database.execute('''UPDATE tests
				SET title = ?''', (self.title,))
			
			lens = len(self.questions)
			for idx, question in enumerate(self.questions):
				database.execute('''UPDATE test_questions
				SET test_id = id, question_id = ? WHERE id = ?''', (question.id, self.prev_questions[idx].id))
			
			
			return self
			
	def delete(self):
		with DB() as database:
			database.execute('''DELETE FROM tests WHERE id = ?''', (self.id,))
			
			for question in self.questions:
				database.execute('''DELETE FROM test_questions WHERE test_id = ?''', (self.id,))
			
	@staticmethod
	def delete_tests_w_deleted_question(question):
		for test in Test.get_all():
			if question in test.questions:
				test.delete()
	@staticmethod
	def get_all():
		with DB() as database:
			rows = database.execute('''SELECT * FROM tests''').fetchall() # fetches all rows which correspond to the query (i.e. every row)

			rows = Adapter.adapt_test_rows(database, Adapter.adapt_query(rows), Question.get_test_questions(
				database.execute('''
				SELECT question_id FROM test_questions
				''').fetchall())) 
			# new rows is result of adapted method return value 
			# adapt query converts list of tuples into list of lists
			
			return [Test(*row) for row in rows] 
			# for each row in the data, instantiate a class with the values from the table
			# and return them all as a list

	@staticmethod
	def find(id):
		with DB() as database:
			row = Adapter.adapt_query(database.execute('''SELECT * FROM tests WHERE id = ?''', (id,)).fetchall())
			# rather banal back-and-forth type conversion from list of tuples to list of lists
			
			question_order = database.execute('''
				SELECT question_id FROM test_questions
				''').fetchall()
				
			try:			
				question_order = Adapter.adapt_list_by_step_3(question_order) # create list of lists spliced by 3
				row = tuple(Adapter.adapt_test_rows(database, row, Question.get_test_questions(question_order[id - 1]))[0])
			except IndexError as error:
				return None
			
			# fetch a single row where id is given id
			# sql queries take tuples, which is why we pass arguments in such a manner
			
			return Test(*row) # return new instance of Test() where we pass the elements of the container as args
