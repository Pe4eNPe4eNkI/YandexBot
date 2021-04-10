import discord
from discord.ext import commands
from discord.utils import get
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/86.0.4240.111 Safari/537.36'}

LINKS = "https://www.google.com/search?sxsrf=ALeKk01-G5_9JcFxgjtDU7651F-Pn7Jyeg%3A1603202429242&ei" \
        "=fe2OX7OmDu6krgS49qMw&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1" \
        "%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp" \
        "=CgZwc3ktYWIQAxgAMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgQIABANMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgQIABBHUPMZWPYbYLkoaABwA3gAgAGGAYgB9AGSAQMwLjKYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab "

client = commands.Bot(command_prefix='.')
client.remove_command('help')

hello_world = ['привет', 'hi', 'Hi', 'Hello', 'hello', 'qq', 'q', 'ky', 'Привет', 'здравствуйте',
               'Здравствуйте', 'Ку', 'здорова', 'Хеллоу', "хеллоу"]
antword = ['информация', 'команды', 'help',
           'Help', 'info', 'Info', 'что делать']


def get_currency_price():
    response_letter = []
    # Подключение ссылки
    full_page = requests.get(LINKS, headers=HEADERS)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    # Поиск нужной иформации в строках хода
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})[0].text
    convert = convert.replace(" ", "")
    response_letter.append(float(convert.replace(",", ".")))
    return response_letter


@client.event
async def on_ready():
    print('Connected')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('Yandex.Lyceum | .help'))


@client.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(
        f'{author.mention}, приветствую, но не на немецком! | {author.mention}, привет! как дела?')


# auto role
@client.event
async def on_member_join(member):
    channel = client.get_channel(689176999578697755)
    role = discord.utils.get(member.guild.roles, id=689430828089868292)

    await member.add_roles(role)
    await channel.send(
        embed=discord.Embed(discription=f'Пользователь ''{member.name}'' присоединился к серверу!',
                            color=0x0c0c0c))


# ban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Ban', color=discord.Color.red())

    await ctx.channel.purge(limit=1)
    await member.ban(reason=reason)

    emb.set_author(name=member.name)
    emb.add_field(name='Ban user',
                  value='Banned user: {}'.format(member.mention))
    emb.set_footer(
        text='Был забанен администратором{}'.format(ctx.author.name))

    await ctx.send(embed=emb)


# kick
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Kick', color=discord.Color.red())

    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)

    emb.set_author(name=member.name)
    emb.add_field(name='Kick user',
                  value='Kicked user: {}'.format(member.mention))
    emb.set_footer(text='Был кикнут администратором{}'.format(ctx.author.name))

    await ctx.send(embed=emb)


# clear
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# join voice
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к  {channel}')


# leave voice
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await ctx.send(f'Бот отключился от  {channel}')
        await voice.disconnect()
    else:
        voice = await channel.conneсt()
        await voice.disconnect()


# dollar
@client.command(pass_context=True)
async def dollar(ctx):
    await ctx.send(
        f'Курс доллара в рублях: {get_currency_price()[0]}')


# help
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Список команд:')

    emb.add_field(name='{}clear'.format('.'), value='Очистка чата')
    emb.add_field(name='{}kick'.format('.'), value='кик участника')
    emb.add_field(name='{}ban'.format('.'), value='бан участника')
    emb.add_field(name='{}unban'.format('.'), value='разбан участника')
    emb.add_field(name='{}join'.format('.'),
                  value='подключение бота к голосовому каналу')
    emb.add_field(name='{}leave'.format('.'),
                  value='отключение бота от голосового канала')
    emb.add_field(name='{}hello'.format('.'), value='Приветствие')
    emb.add_field(name='{}help'.format('.'), value='Список команд')
    emb.add_field(name='{}dollar'.format('.'), value='Курс доллара')

    await ctx.send(embed=emb)


# get token
token = open('token.txt', 'r').readline()

client.run(token)
