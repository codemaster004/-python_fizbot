import json
import random
from datetime import datetime


class AnswerGen:
	def __init__(self):
		pass
	
	def gen_static_answ(self, tag):
		with open('data/intents.json') as file:
			intents = json.load(file)['intents']
		
		for intent in intents:
			if intent['tag'] == tag:
				response = random.choice(intent['responses'])
		
		return response
	
	def __lesson(self, message):
		with open('config/lessons.json', 'r') as file:
			lessons = json.load(file)
		
		def get_lesson(lessons, add=0):
			now = datetime.now()
			day = int(now.strftime("%w")) - 1
			lesson_n = 0
			for l in lessons[day]:
				lesson_time = now.replace(hour=l['h'], minute=l['m'])
				if now > lesson_time:
					lesson_n += 1

			lesson_n += add

			try:
				return lessons[day][lesson_n]
			except IndexError:
				return None
				
		next_lessons_c = message.count('next')
		lesson = get_lesson(lessons, add=next_lessons_c)
		
		if not lesson:
			return 'You dont have lessons'
		
		response = f'Lesson is {lesson["name"]} at {lesson["h"]}:{lesson["m"]}'
		
		return response
	
	def __plan(self, message):
		next_days_c = message.count('tomorrow') + message.count('next')
		
		with open('config/lessons.json', 'r') as file:
			lessons = json.load(file)
			
		now = datetime.now()
		day = int(now.strftime("%w")) - 1 + next_days_c
		
		days = ['monday', 'tesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		for d in days:
			if d in message:
				day = days.index(d)	
		
		if day >= 5:
			day = day % 5
		
		plan = ''
		for lesson in lessons[day]:
			plan += f'{lesson["name"]}, {lesson["h"]}:{lesson["m"]}\n'
			
		return plan
	
	def gen_custom_answ(self, tag, message):
		if tag == 'lesson':
			response = self.__lesson(message)
		elif tag == 'plan':
			response = self.__plan(message)
		
		return response
	
	def generate_answer(self, tag, message):
		custom_tags = ['plan', 'lesson']
		
		if tag == 'Error':
			return ''
		
		if tag in custom_tags:
			r = self.gen_custom_answ(tag, message)
		else:
			r = self.gen_static_answ(tag)
		
		return r

if __name__ == '__main__':
	generator = AnswerGen()
	r = generator.generate_answer('plan', 'what is my plan on monday')
	print(r)
