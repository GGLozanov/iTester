from typing import List # import List duck-typing functionality from Python 3.5 lib
from database import DB
from adapter import Adapter

# multiple-choice questions have an entire List with however many answers they have
# number of question will be index in list

class Question:

	def __init__(self, id: int, question: str, answers: List[str], correct_answer_index: int):
		self.id = id
		self.question = question
		self.answers = answers
		
		self.correct_answer_index = 0 \
			if int(correct_answer_index) - 1 < 0 or int(correct_answer_index) > len(answers) \
			else int(correct_answer_index) - 1
		
		self.correct_answer = answers[self.correct_answer_index] 
		
		self.user_answer = None
		# default answer is None (lol fuck you students)
		# handle if answer_index > list size -> done
		
	def __len__(self):
		return len(self.answers)
	
	def set_answer(self, answer):
		self.user_answer = answer

	def is_answer_correct(self) -> bool:
		return self.user_answer == self.correct_answer

	def create(self): # will probably bug out because there is no insertion or reference to the other table apart from the for loop
		with DB() as database:
			for ans in self.answers:
				database.execute('''INSERT INTO answers (id, answer) VALUES (?, ?)''', (self.id, ans))
		
			database.execute('''INSERT INTO questions (id, question, answers_id, correct_answer_index) VALUES (?, ?, ?, ?)''',
					(self.id, self.question, self.id, self.correct_answer_index))

			return self
			
	def update(self, values, answers):
		self.question = values[0]
		self.correct_answer = values[1]
		self.answers = answers
		
		return self
			
	def edit(self):
		with DB() as database:
			len = len(self.answers)
			for ans in self.answers:
				rows = database.execute('''SELECT * from answers''')
				database.execute('''UPDATE answers
					SET answer = ? WHERE id = ?''', (ans, self.id * 3 - (len - self.answers.index(ans) - 1)))
					# set all of the answers of the questio to these (replace the 3 if more questions are needed)
				
			database.execute('''UPDATE questions 
				SET question = ?, answers_id = ?, correct_answer_index = ?
				WHERE id = ?''', (self.question, self.id, self.correct_answer_index, self.id))
			return self
			
	def delete(self):
		with DB() as database:
			database.execute('''DELETE FROM questions WHERE id = ?''', (self.id,))

	@staticmethod
	def get_all():
		with DB() as database:
			rows = Adapter.adapt_query(database.execute('''SELECT * FROM questions''').fetchall()) # convert the data into a list of lists
			rows = Adapter.adapt_question_rows(database, rows)
			

			return [Question(*row) for row in rows] # instantiate questions list
			
	@staticmethod
	def get_test_questions(ids): # takes question ids and returns a list of questions for the given test
		return [Question.find(id[0]) for id in ids]

	@staticmethod
	def find(id):
		with DB() as database:
			row = Adapter.adapt_query(database.execute('''SELECT * FROM questions WHERE id = ?''', (id,)).fetchall())
			
			try:
				row = tuple(Adapter.adapt_question_rows(database, row)[0])
			except IndexError as error:
				return None
			
			return Question(*row)
