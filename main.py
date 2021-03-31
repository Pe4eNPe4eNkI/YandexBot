import discord
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='.')
client.remove_command('help')

hello_world = ['привет', 'hi', 'Hi', 'Hello', 'hello', 'qq', 'q', 'ky', 'Привет', 'здравствуйте',
               'Здравствуйте', 'Ку', 'здорова', 'Хеллоу', "хеллоу"]
antword = ['информация', 'команды', 'help',
           'Help', 'info', 'Info', 'что делать']

# get token
token = open('token.txt', 'r').readline()

client.run(token)
