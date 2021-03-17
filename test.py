from chat_ai import BotAI
from answers import AnswerGen


my_bot = BotAI()
my_bot.load_model()

answ_gen = AnswerGen()

while True:
	inp = input('You: ')
	
	if inp == 'quit':
		break
	
	prediction = my_bot.predict_label(inp)
	answ = answ_gen.generate_answer(prediction, inp)

	print('Bot:', answ)
