from typing import List # import List duck-typing functionality from Python 3.5 lib
from database import DB

# multiple-choice questions have an entire List with however many answers they have
# questions with only one element in the list are treated as open-ended
# number of question will be index in list

class Question:
	user_answer = None
	correct_answer = None

	def __init__(self, id: int, question: str, answers: List[str], correct_answer_index: int):
		self.id = id
		self.question = question
		self.answers = answers
		
		self.correct_answer_index = correct_answer_index
		
		if int(correct_answer_index) > len(answers): self.correct_answer = 0
		else: self.correct_answer = answers[int(correct_answer_index)] # handle if answer_index > list size
		
		self.question_type: bool = False if len(answers) == 1 else True # is multiple choice or open-ended
	
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
			data = [list(tup) for tup in database.execute('''SELECT * FROM questions''').fetchall()]
	
			print(data)
	
			for row in data:
				answers = database.execute('''SELECT answer FROM answers''').fetchall() # get answers
				print(answers)
				answers = [answer[0] for answer in answers]
				answers = [answers[answer:answer+3] for answer in range(0, len(answers), 3)]
				print(answers)
				row[2] = answers[data.index(row)]
				
			questions = [Question(*row) for row in data]

			
#			for question in questions:
#				answers = database.execute('''SELECT answer FROM answers WHERE id = ?''', question.id)
#				question.answers = answers
#							
#			print(questions)

			return questions


	@staticmethod
	def find(id):
		with DB() as database:
			row = database.execute('''SELECT * FROM questions WHERE id = ?''', (id,)).fetchone()
			
			return Question(*row)
