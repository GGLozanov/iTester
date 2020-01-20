import unittest
from database import DB
from test import Test
from question import Question

class TestTests(unittest.TestCase):
	def test_create_is_working(self):
		with DB() as database:
			test = Test().create()
			test.id = database.execute('''SELECT id FROM tests WHERE title = ?''', \
				(test.title,)).fetchone()[0]
		self.assertEqual(Test.find(test.id), test)
		
	def test_delete_is_working(self):
		with DB() as database:
			test = Test().create()
			test.id = database.execute('''SELECT id FROM tests WHERE title = ?''', \
				(test.title,)).fetchone()[0]
		with DB() as database:
			test.delete()
		self.assertEqual(Test.find(test.id), None)
	
	def test_update_is_working(self): # might not work with different test titles (which is why DISTINCT exists!)
		with DB() as database:
			test = Test().create()
			test.id = database.execute('''SELECT id FROM tests WHERE title = ?''', \
				(test.title,)).fetchone()[0]
		with DB() as database:
			test.update("NewTest", test.questions).edit()
		self.assertEqual(Test.find(test.id), test)
	
	def test_grader_is_working(self):
		test = Test().create()
		test.set_answers([question.correct_answer for question in test.questions])
		test.check_test()
		self.assertEqual(test.count_correct(), 100.0)
		
class QuestionTests(unittest.TestCase):
	def test_create_is_working(self):
		with DB() as database:
			question = Question().create()
			question.id = database.execute('''SELECT id FROM questions WHERE question = ?''', \
				(question.question,)).fetchone()[0]
		self.assertEqual(Question.find(question.id), question)
		
	def test_delete_is_working(self):
		with DB() as database:
			question = Question().create()
			question.id = database.execute('''SELECT id FROM questions WHERE question = ?''', \
				(question.question,)).fetchone()[0]
		with DB() as database:
			question.delete()
		self.assertEqual(Question.find(question.id), None)
	
	def test_update_is_working(self):
		with DB() as database:
			question = Question().create()
			question.id = database.execute('''SELECT id FROM questions WHERE question = ?''', \
				(question.question,)).fetchone()[0]
		with DB() as database:
			question.update(["NewQuestion", question.correct_answer], question.answers).edit()
		self.assertEqual(Question.find(question.id), question) # find Question with id question id

if __name__ == "__main__":
	unittest.main()
