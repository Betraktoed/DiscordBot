import discord
import os
import pprint
import json
import random
import datetime
import pandas as pd




status = open('./data/status.txt', 'r').read()
client = discord.Bot()
token = '' #токен бота
@client.event
async def on_ready():
	print("Logged in as a bot {0.user}".format(client)) #сообщение об удачной инициализации бота

@client.event #реакции ответы пользователей на сообщения бота
async def on_reaction_add(reaction, user):
	us = str(user) 
	react = str(reaction)
	message_id = str(reaction.message.id)
	print(us)
	print(react)
	if user == client.user:
		return
	with open('./data/A.json', 'r')as f:
		A = json.loads(f.read())
	status = int(open('./data/status.txt', 'r').read().rstrip())
	cur_question = open("./data/current_qestion.txt", 'r').read().rstrip()
	if message_id == cur_question and status == 3:
		QN = open("./data/question_number", 'r').read()
		print(A[QN])
		if react == A[QN]:
			now = datetime.datetime.timestamp(datetime.datetime.now())
			print(now)
			with open('./data/time.json', "r") as f:
				timing = json.loads(f.read())
			score = 60 - now + timing
			print(score)
			if score > 0:
				with open("./data/active_users.json", 'r') as f:
					active_users = json.loads(f.read())
				if us not in active_users.keys():
					active_users[us] = dict()
					active_users[us][QN] = score
				else:
					if QN not in active_users[us].keys():
						active_users[us][QN] = score
					else:
						active_users[us][QN] = 0
				with open("./data/active_users.json", 'w') as f:
					json.dump(active_users, f)
		else:
			now = datetime.datetime.timestamp(datetime.datetime.now())
			print(now)
			with open('./data/time.json', "r") as f:
				timing = json.loads(f.read())
			score = 60 - now + timing
			if score > 0:
				score = 0 
				with open("./data/active_users.json", 'r') as f:
					active_users = json.loads(f.read())
				if us not in active_users.keys():
					active_users[us] = dict()
					active_users[us][QN] = 0
				else:
					active_users[us][QN] = 0
				with open("./data/active_users.json", 'w') as f:
					json.dump(active_users, f)
@client.event
async def on_message(message):
	privat = "ботом-тут" #имя приватного канала для создания бота
	admin_role = "Илита" #роль админа 
	user = str(message.author)
	username = str(message.author).split("#")[0]
	channel = str(message.channel.name)
	user_message = str(message.content)
	with open("./data/active_users.json", 'r') as f:
		active_users = json.loads(f.read())
	with open("./data/done_users.json", 'r') as f:
		done_users = json.loads(f.read())
	with open('./data/Q.json', 'r')as f:
		Q = json.loads(f.read())
	with open('./data/A.json', 'r')as f:
		A = json.loads(f.read())
	with open('./data/time.json', "r") as f:
		timing = json.loads(f.read())
	with open('./data/interval.txt', 'r') as f:
		interval = int(f.read())
	status = int(open('./data/status.txt', 'r').read().rstrip())
	print(f'Message {user_message} by {username} on {channel}')
	if message.author == client.user:
		return
	pprint.pprint(status)
	if channel == privat:
		if user_message.lower() == "hello" or user_message.lower() == "hi":
			await message.channel.send(f'Hello {username}')
			return
		if (user_message.lower() == "make quiz" or user_message.lower() == "create quiz") and admin_role in [ y.name for y in message.author.roles] and status == 0:
			await message.channel.send(f"Напишите ваш вопрос и ответ в формате \n 'Вопрос оцените качество? - \U0001F603 '\n Чтобы задать паузу между вопросами введите 'Интервал 30' \n Для завершение создания введите 'закончить создание'")
			status = 1
		elif (admin_role in [ y.name for y in message.author.roles] and status == 1 and "вопрос" in user_message.lower()):
			if type(Q) == str:
				l = 0
				Q = dict()
				A = dict()
			else:
				l = len(Q.keys())
			print(l)
			Q[l] = user_message.lower().split("вопрос")[1].split("-")[0]
			pprint.pprint(user_message.lower().split("вопрос")[1])
			A[l] = user_message.split("-")[1].strip()
			pprint.pprint(user_message.split("-")[1])
			await message.channel.send(f"Следующий вопрос")
		elif (admin_role in [ y.name for y in message.author.roles] and status == 1 and "интервал" in user_message.lower()):
			await message.channel.send("Интервал задан")
			interval = user_message.lower().split("интервал")[1].strip()
		elif ("закончить создание" in user_message.lower() and admin_role in [ y.name for y in message.author.roles] and status == 1):
			status = 2
			active_users = dict()
			#done_users = dict()
	if user_message.lower() == "bye":
		await message.channel.send(f'Bye {username}')
	elif user_message.lower() == "tell me a joke":
		jokes = [" Can someone please shed more\
		light on how my lamp got stolen?",
			"Why is she called llene? She\
			stands on equal legs.",
			"What do you call a gazelle in a \
			lions territory? Denzel."]
		temp = await message.channel.send(random.choice(jokes))
		await temp.add_reaction('5\ufe0f\u20e3')
		await temp.add_reaction('\U0001F480')
		await temp.add_reaction('\U0001F47D')
		await temp.add_reaction('\U0001F63A')
		await temp.add_reaction('\U0001F497')
	elif user_message.lower() == "start quiz" and status == 2 and admin_role in [ y.name for y in message.author.roles]:
		status = 3
		open("./data/status.txt", 'w').write(str(status))
		print("XR")
		for i in Q.keys():
			open("./data/question_number", 'w').write(i)
			temp = await message.channel.send(Q[i])
			await temp.add_reaction('1\ufe0f\u20e3')#смайлики для ответов
			await temp.add_reaction('2\ufe0f\u20e3')
			await temp.add_reaction('3\ufe0f\u20e3')
			await temp.add_reaction('4\ufe0f\u20e3')
			await temp.add_reaction('5\ufe0f\u20e3')
			timing = datetime.datetime.timestamp(datetime.datetime.now())
			ids = temp.id
			with open('./data/time.json', "w") as f:
				json.dump(timing, f)
			open("./data/current_qestion.txt", 'w').write(str(ids))
			await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=60))
			await message.channel.send(f'Qestion is closed! Wait {interval} seconds to next!')
			await discord.utils.sleep_until(datetime.datetime.now() + datetime.timedelta(seconds=interval))
		status = 2
		with open("./data/active_users.json", 'r') as f:
			active_users = json.loads(f.read())
		pprint.pprint(active_users)
		l = len(done_users.keys())
		done_users[l] = active_users
		active_users = dict()
		with open("./data/active_users.json", 'w') as f:
			json.dump(active_users, f)
		await message.channel.send(f'Quiz ended!')
	elif user_message.lower() == "get results" and admin_role in [ y.name for y in message.author.roles]:
		result = dict()
		for i in done_users.keys():
			result["Quest " + str(i)] = dict()
			for j in done_users[i].keys():
				temp = 0
				for k in done_users[i][j].keys():
					temp += done_users[i][j][k]
				result["Quest " + str(i)][j] = temp
		df = pd.DataFrame(result)
		await message.channel.send(df.to_string())
	elif user_message.lower() == "clear questions" and status == 2 and admin_role in [ y.name for y in message.author.roles]:
		Q = dict()
		A = dict()
		status = 0
	elif user_message.lower() == "clear results" and admin_role in [ y.name for y in message.author.roles]:
		done_users = dict()
			

	with open('./data/time.json', "w") as f:
		json.dump(timing, f)
	with open('./data/Q.json', "w") as f:
		json.dump(Q, f)
	with open('./data/A.json', "w") as f:
		json.dump(A, f)
	#with open("./data/active_users.json", 'w') as f:
		#json.dump(active_users, f)
	with open("./data/done_users.json", 'w') as f:
		json.dump(done_users, f)
	with open('./data/interval.txt', 'w') as f:
		f.write(str(interval))
	open("./data/status.txt", 'w').write(str(status))
async def start_quiz(username):
	if username in done_users.keys():
		await message.channel.send(f'{username} allready end quiz!')
		return
	elif username in active_users.keys():
		await message.channel.send(f'{username} allready start quiz!')
		return
	active_users[username] = 0

client.run(token)

