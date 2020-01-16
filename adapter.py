from database import DB

class Adapter:
	@staticmethod
	def adapt_list_by_step_3(list):
		return [list[element:element+3] for element in range(0, len(list), 3)]

	@staticmethod
	def adapt_double_list_by_step_3(list):
		list = [element[0] for element in list] # convert answers into a single list
		return Adapter.adapt_list_by_step_3(list) # create list of lists spliced by 3 elements (answer = int index)

	@staticmethod	
	def adapt_question_rows(database, rows):
		answers = Adapter.adapt_double_list_by_step_3(database.execute('''SELECT answer FROM answers''').fetchall())
		for row in rows:
			row[2] = answers[row[0] - 1] 
			# set the answers to the answer element in each question (find the apt answer by id - 1 index)
		
		return rows
		
	@staticmethod
	def adapt_test_rows(database, rows, questions):
		for row in rows:
			row[1] = questions # place at second position (None)
			
		return rows
	
	@staticmethod	
	def adapt_query(query):
		return [list(tup) for tup in query]
