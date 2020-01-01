from database import DB

class Adapter:
	@staticmethod	
	def adapt_question_rows(database, rows):
		for row in rows:
			answers = database.execute('''SELECT answer FROM answers''').fetchall() # get distinct answers out of the three questions

			answers = [answer[0] for answer in answers] # convert answers into a single list
			answers = [answers[answer:answer+3] for answer in range(0, len(answers), 3)] # create list of lists spliced by 3 elements (answer = int index)

			row[2] = answers[rows.index(row)] # set the answers to the answer element in each question
		
		return rows
		
	@staticmethod
	def adapt_test_rows(database, rows, questions):
		for row in rows:
			row[1] = questions # place at second position (None)
			
		return rows
	
	@staticmethod	
	def adapt_query(query):
		return [list(tup) for tup in query]
