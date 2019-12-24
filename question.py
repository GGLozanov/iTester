from typing import List # import List duck-typing functionality from Python 3.5 lib

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
		self.correct_answer = answers[correct_answer_index] # handle if answer_index > list size
		self.question_type: bool = False if answers.size() == 1 else True # is multiple choice or open-ended
	
	def set_answer(self, answer):
		if answer not in answers:
			return False
		self.user_answer = answer

	def is_answer_correct(self) -> bool:
		return self.user_answer == correct_answer
