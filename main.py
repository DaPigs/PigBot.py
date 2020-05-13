import discord
import asyncio

client = discord.Client()
token = "NzEwMDExNzA0MTg0MTQzOTA1.XrvPVQ.4Lf1tqcm_2Fmhh9MrozZelX-2W8"

def findtime(timespan):
	time = 0
	keep = "0"
	keepsec = 0
	if(timespan.find('h') != -1):
		time += int(timespan[0:timespan.find('h')])*3600
	if(timespan.find('m') != -1):
		for i in range(0, len(timespan)):
			if(timespan[i] == 'h'):
				i += 1;
				if(timespan[i+1] == 'm'):
					keep = timespan[i]
					keepsec = i+2
					break
				else:
					keep = timespan[i] + timespan[i + 1]
					keepsec = i+3
					break
	time += int(keep)*60
	if(timespan.find('s') != -1):
		if(timespan[keepsec+1] == 's'):
			time += int(timespan[keepsec])
		else:
			time += int(timespan[keepsec] + timespan[keepsec + 1])
	return time

async def pigremind(time, rmd, channel):
	await channel.send(str(rmd) + " reminder added, " + str(time) + " seconds")
	await asyncio.sleep(time)
	await client.get_user(489010589503455232).send(rmd)

@client.event
async def on_connect():
	print ("Connected to discord")
	print ("--------------------------")

@client.event
async def on_ready():
	print ("Logged in")
	print ("--------------------------")


@client.event
async def on_message(message):
	if(message.author.id == 280726849842053120):

		#fishing
		if(message.content.find("- You caught ") != -1 and message.content.find("Cooldown: ") != -1):
			time = message.content[message.content.find("Cooldown: ")+10:message.content.find("Cooldown: ")+15]
			if(time[0] == '1'):
				await pigremind(int(time[-3]) + int(time[0])*60, "Fishing", message.channel)
				return 0
			else:
				await pigremind(int(time[0:2]), "Fishing", message.channel)
				return 0

		#hourly
		if(message.content.find(" | Combo:") != -1 and message.content.find("You found") != -1):
			await pigremind(3600, ">hr", message.channel)

		#generator
		if(message.content.find("Your generator has been started. Come back in 4 hours, but don't be too late.") != -1):
			await pigremind(14400, "Generator", message.channel)
			return 0

		#farm claim
		if(message.content.find("Claimed one seed of type : ") != -1):
			await pigremind(28800, ">far c", message.channel)
			return 0

		#cau
		if(message.content.find("You started the creation of ") != -1):
			timespan = message.content[message.content.find("Time remaining : ") + 17:]
			time = findtime(timespan)
			await pigremind(time, ">cau ", message.channel)
			return 0

		#farm harvest
		if(message.content.find("Sucessfully planted") != -1):
			timespan = message.content[message.content.find("it will take ") + 13:]
			time = findtime(timespan)
			await pigremind(time, ">far h", message.channel)
			return 0
		
		#drill
		if(message.content.find("Congratulations ! Your drill has just brought you") != -1):
			await pigremind(86440, ">drill c", message.channel)
			return 0



	if(message.author.id == 489010589503455232):
		if(message.content == "pigmind vote"):
			await pigremind(43200, "vote", message.channel)
			return 0
		if(message.content[0:8] == "pigmind "):
			timespan = message.content[8:message.content.find("rmd ")]
			time = findtime(timespan)
			await pigremind(time, message.content[message.content.find("rmd "):], message.channel)
			return 0
		if(message.content == "pigmind battle cats collect"):
			await pigremind(21600, "battle cats collect", message.channel)

client.run(token, bot=True)
