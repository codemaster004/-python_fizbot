from chat_ai import BotAI
from answers import AnswerGen
from chat_database import ChatDB
from fbchat import Client
from fbchat.models import *
import json


my_bot = BotAI()
my_bot.load_model()

answ_gen = AnswerGen()

chat_db = ChatDB()

with open('config/config.json') as file:
	config = json.load(file)
	username = config['FB_USERNAME']
	password = config['FB_PASSWORD']
with open('config/chats.json') as file:
	chats = json.load(file)


class MyBot(Client):
	
	is_off = False
	
	admin_id = "100029716773691"
	
	def user_commands(self, current_chat, message_text):
		text = ''
		if 'status' in message_text and 'bot' in message_text:
			text = f'Chat: {current_chat["name"]}\nIs banned: {current_chat["ban"]}'
		
		if not (self.is_off or current_chat['ban']):
			if 'index' in message_text and 'bot' in message_text:
				text = f'Fiz:\n- Energia kinetyczna\n- Energia potencjalna\n- Okres drgań\n- Wychylenie\n- Siła bezwładności\n- Wahadło matematyczne (definicja)\n- Ruch harmoniczny (definicja)\n- Częstotliwość\n- Faza ruchu\n- Omega\n- Amplituda\n- Sprężystość siła i współczynnik\n- Prędkość w ruchu harmonicznym\n- Przyspieszenie w ruchu harmonicznym\n- Siła w ruchu harmonicznym\n- Energia w ruchu harmonicznym\n- Zasada dynamiki (1, 2, 3)\n- Wahadlo sprężynowe\n- sin, cos jako tabela'
			if 'help' in message_text and 'bot' in message_text:
				text = f'Dostępne komendy:\n"bot status": status chatu\n\n"bot index": spis wiedzy z fiz\n'
		
		if text != '':
			self.send(
				Message(text=text),
				thread_id=current_chat['thread_id'],
				thread_type=ThreadType.USER if current_chat['thread_type'] == 'User' else ThreadType.GROUP
			)
	
	def admin_commands(self, current_chat, message_text):
		global chats
		
		if message_text == 'bot start':
			self.is_off = False
		if message_text == 'bot stop':
			self.is_off = True
		
		if self.is_off:
			return

		if message_text == 'bot ban':
			chats[f'{current_chat["thread_id"]}']['ban'] = True
		if message_text == 'bot unban':
			chats[f'{current_chat["thread_id"]}']['ban'] = False

		with open('config/chats.json', 'w') as file:
			json.dump(chats, file)
	
	def bot_active(self, mes_text, author_id, chat):
		activations = ['bot', 'bocie', 'boot', 'robbie', 'robot', '@robbie fizbot', '@robbie']
		
		if mes_text in activations:
			
			user = client.fetchUserInfo(author_id)[author_id]
			name = user.name.split(' ')[0]
			
			self.send(
				Message(text=f'Hej, {name}!'),
				thread_id=chat['thread_id'],
				thread_type=ThreadType.USER if chat['thread_type'] == 'User' else ThreadType.GROUP
			)
			
			return False
		
		if chat['thread_type'] == 'Group':
			if any([a in mes_text for a in activations]):
				return True
		else:
			return True
		
		return False
	
	def user_exists(self, thread_id):
		global chats
		
		if thread_id in chats:
			chat = chats[f'{thread_id}']
		else:
			thread = self.fetchThreadInfo(f'{thread_id}')[f'{thread_id}']
			chats[f'{thread_id}'] = {
				"name": str(thread.name).split(' ')[0],
				"thread_type": 'Group' if thread.type == ThreadType.GROUP else 'User',
				"thread_id": thread_id,
				"ban": False,
			}
			chat = chats[f'{thread_id}']
			
			with open('config/chats.json', 'w') as file:
				json.dump(chats, file)
		
		return chat
	
	def interaction(self, message_obj, chat):
		
		message_text = message_obj.text.lower()
		prediction = my_bot.predict_label(message_text)
		
		answ = answ_gen.generate_answer(prediction, message_text)
		
		chat_db.write_chat(chat['thread_id'], message_obj.author, message_text, answ)
		
		if answ != "":
			if 'img:' in answ:
				client.sendLocalImage(
					answ.replace('img:', ''),
					thread_id=chat['thread_id'],
					thread_type=ThreadType.USER if chat['thread_type'] == 'User' else ThreadType.GROUP,
				)
			else:
				self.send(
					Message(text=answ),
					thread_id=chat['thread_id'],
					thread_type=ThreadType.USER if chat['thread_type'] == 'User' else ThreadType.GROUP
				)
	
	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		self.markAsDelivered(thread_id, message_object.uid)
		
		current_chat = self.user_exists(thread_id)
		message_text = message_object.text.lower()
		
		if str(author_id) == self.admin_id or author_id == self.uid:
			self.admin_commands(current_chat, message_text)
		
		if f'{author_id}' == f'{self.uid}':
			return
		
		self.user_commands(current_chat, message_text)
		
		if self.is_off:
			return

		if current_chat['ban']:
			return
		
		if not self.bot_active(message_text, author_id, current_chat):
			return
		
		self.markAsRead(thread_id)
		
		if author_id != self.uid or thread_id == self.uid:
			self.interaction(message_object, current_chat)


client = MyBot(username, password)
client.listen()
