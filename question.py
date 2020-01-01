from typing import List # import List duck-typing functionality from Python 3.5 lib
from database import DB
from adapter import Adapter

# multiple-choice questions have an entire List with however many answers they have
# questions with only one element in the list are treated as open-ended
# number of question will be index in list

class Question:

	def __init__(self, id: int, question: str, answers: List[str], correct_answer_index: int):
		self.id = id
		self.question = question
		self.answers = answers
		
		self.correct_answer_index = correct_answer_index
		
		if int(correct_answer_index) > len(answers): self.correct_answer = 0
		else: self.correct_answer = answers[int(correct_answer_index)] # handle if answer_index > list size
		
		self.question_type: bool = False if len(answers) == 1 else True # is multiple choice or open-ended
		
	def __len__(self):
		return len(self.answers)
	
	def set_answer(self, answer):
		if answer not in answers:
			return False
		self.user_answer = answer

	def is_answer_correct(self) -> bool:
		return self.user_answer == correct_answer

	def create(self): # will probably bug out because there is no insertion or reference to the other table apart from the for loop
		with DB() as database:		
			for ans in self.answers:
				database.execute('''INSERT INTO answers (id, answer) VALUES (?, ?)''', (self.id, ans))
		
			database.execute('''INSERT INTO questions (id, question, answers_id, correct_answer_index) VALUES (?, ?, ?, ?)''',
					(self.id, self.question, self.id, self.correct_answer_index))

			return self

	@staticmethod
	def get_all():
		with DB() as database:
			rows = Adapter.adapt_query(database.execute('''SELECT * FROM questions''').fetchall()) # convert the data into a list of lists
			rows = Adapter.adapt_question_rows(database, rows)
			
			print(rows)

			return [Question(*row) for row in rows] # instantiate questions list
			
	@staticmethod
	def get_test_questions(ids): # takes question ids and returns a list of questions for the given test
		print(ids)
		return [Question.find(id[0]) for id in ids]

	@staticmethod
	def find(id):
		with DB() as database:
			row = Adapter.adapt_query(database.execute('''SELECT * FROM questions WHERE id = ?''', (id,)).fetchall())
			
			try:
				row = tuple(Adapter.adapt_question_rows(database, row)[0])
			except IndexError as error:
				return None
				
			print(row)
			
			return Question(*row)
