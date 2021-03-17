from chat_ai import BotAI
from answers import AnswerGen


my_bot = BotAI()
my_bot.load_model()

answ_gen = AnswerGen()

def use_bot():
	while True:
		inp = input('You: ')
		
		if inp == 'quit':
			break
		
		prediction = my_bot.predict_label(inp)
		answ = answ_gen.generate_answer(prediction, inp)

		print('Bot:', answ)

def test_questions():
	global my_bot
	
	tests = []
	with open('test/test_question.txt') as test_file:
		for line in test_file:
			qest_answ = line[0:-1]
			qest_answ = qest_answ.split(';')
			
			tests.append((qest_answ[0], qest_answ[1]))
	
	for t_set in tests:
		
		assert my_bot.predict_label(t_set[0]) == t_set[1], f'Mistake in {t_set[0]}'


if __name__ == '__main__':
	print('Begun Testing')
	test_questions()
	print('All Tests passed')
