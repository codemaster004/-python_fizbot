import sqlite3
from datetime import datetime, timedelta


class ChatDB:
	
	def __init__(self):
		self.connection = sqlite3.connect('data/chat_data.db')
		self.cursor = self.connection.cursor()
	
	def create_table(self):
		self.cursor.execute("""CREATE TABLE chats_data
			(id INTEGER PRIMARY KEY, 
			date text,
			chat text,
			author text, 
			message text, 
			answer text)""")
	
	def write_chat(self, chat, author, message, answer):
		now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
		self.cursor.execute(f"INSERT INTO chats_data(date, chat, author, message, answer) VALUES ('{now}', {chat}, {author}, '{message}', '{answer}')")
		
		self.connection.commit()
	
	def get_data(self, n):
		day = datetime.now() - timedelta(days=n)
		
		query = self.cursor.execute(f"SELECT * FROM chats_data WHERE date LIKE '{day.strftime('%d-%m-%Y')}%'")
		
		for data in query:
			print(data)
		
		return query
	
	def my_func(self):
		day = datetime.now() - timedelta(days=1)
		self.cursor.execute(f"DELETE FROM chats_data WHERE chat_date LIKE '{day.strftime('%d-%m-%Y')}%'")
		# self.connection.commit()


if __name__ == '__main__':
	db = ChatDB()
	
	# db.create_table()
	# db.write_chat(0, 0, 'test', 'test a')
	db.get_data(0)
	# db.my_func()
