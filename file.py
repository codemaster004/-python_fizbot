"""
omega: \u03c9
alfa: \u03b1
pi: \u03c0
sqrt: \u221a
pi(p): \u03c1
^2: \u00B2
"""


from fbchat import Client


client = Client('filip.dabkowski.39501', 'jofhym-cyznEk-vofja4')

messages = client.fetchThreadMessages(thread_id="100015183226720", limit=50)

texts = [mess.text for mess in messages]
texts.reverse()

for t in texts:
	print(t)
