import spacy
import numpy
import tflearn
import tensorflow
import json
import pickle


spacy_nlp = spacy.load('pl_core_news_sm')


class BotAI:
	
	polish_letters = ['ąa', 'ęe', 'łl', 'żz', 'źz', 'óu', 'śs', 'ćc', 'ńn']
	
	def __init__(self):
		with open('data/intents.json') as file:
			self.data = json.load(file)
		
		self.get_data()
	
	def get_data(self):
		self.words = []
		self.labels = []
		docs_x = []
		docs_y = []

		for intent in self.data['intents']:
			for pattern in intent['patterns']:
				
				for p_l in self.polish_letters:
					pattern = pattern.replace(p_l[0], p_l[1])
				
				doc = spacy_nlp(pattern)
				
				interpunction = [',', '.', '"', '\'', '?', '!']
				wrds = [token.lemma_ for token in doc if not token.lemma_ in interpunction]
				
				self.words.extend(wrds)
				docs_x.append(wrds)
				docs_y.append(intent['tag'])
				
				if intent['tag'] not in self.labels:
					self.labels.append(intent['tag'])
		
		self.words = sorted(list(set(self.words)))

		self.labels = sorted(self.labels)

		self.traning = []
		self.output = []

		out_empty = [0 for _ in range(len(self.labels))]

		for x, doc in enumerate(docs_x):
			bag = []
			
			wrds = doc
			
			for w in self.words:
				if w in wrds:
					bag.append(1)
				else:
					bag.append(0)
			
			output_row = out_empty[:]
			output_row[self.labels.index(docs_y[x])] = 1
			
			self.traning.append(bag)
			self.output.append(output_row)

		self.traning = numpy.array(self.traning)
		self.output = numpy.array(self.output)
		
		with open('data/data.pickle', 'wb') as f:
			pickle.dump((self.words, self.labels, self.traning, self.output), f)

	def load_model(self):
		net = tflearn.input_data(shape=[None, len(self.traning[0])])
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, len(self.output[0]), activation='softmax')
		net = tflearn.regression(net)

		self.model = tflearn.DNN(net)
		self.model.load('model/model.tflearn')

	def train_model(self):
		net = tflearn.input_data(shape=[None, len(self.traning[0])])
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, len(self.output[0]), activation='softmax')
		net = tflearn.regression(net)
		
		self.model = tflearn.DNN(net)
		self.model.fit(self.traning, self.output, n_epoch=1000, batch_size=8, show_metric=True)
		self.model.save('model/model.tflearn')

	def __bag_of_words(self, s, words):
		bag = [0 for _ in range(len(words))]
		
		doc = spacy_nlp(s)
			
		interpunction = [',', '.', '"', '\'', '?', '!']
		s_words = [token.lemma_ for token in doc if not token.lemma_ in interpunction]
		
		for se in s_words:
			for i, w, in enumerate(words):
				if w == se:
					bag[i] = 1
		
		return numpy.array(bag)
	
	def predict_label(self, text):
		text = text.lower()
		
		for p_l in self.polish_letters:
			text = text.replace(p_l[0], p_l[1])
		
		results = self.model.predict([self.__bag_of_words(text, self.words)])[0]
		results_index = numpy.argmax(results)
		tag = self.labels[results_index]
		
		if results[results_index] > 0.80:
			return tag
		else:
			return 'Error'

if __name__ == '__main__':
	bot = BotAI()
	bot.train_model()