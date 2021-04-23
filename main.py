import discord
from discord import utils
import config
from discord.ext import commands
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import pyowm
import asyncio
import bs4
from bs4 import BeautifulSoup
import pymorphy2
from translate import Translator
import sqlite3 as sql

client = commands.Bot(command_prefix='.')
client.remove_command('help')


# ready
@client.event
async def on_ready():
    print('Connected')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('Yandex.Lyceum | .help'))


# reaction_add
@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == config.POST_ID:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)
        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])
            if (len([i for i in member.roles if
                     i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print(
                    '[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(
                        member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


# reaction_remove
@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = utils.get(message.guild.members, id=payload.user_id)
    try:
        emoji = str(payload.emoji)
        role = utils.get(message.guild.roles, id=config.ROLES[emoji])
        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member,
                                                                                         role))
    except KeyError as e:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


# money
def get_currency_price(name):
    if name == "dollar":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(config.LINKS_DOLLAR, headers=config.HEADERS)
    elif name == "euro":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(config.LINKS_EURO, headers=config.HEADERS)
    elif name == "frank":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(config.LINKS_FRANK, headers=config.HEADERS)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    # Поиск нужной иформации в строках хода
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})[
        0].text
    convert = convert.replace(" ", "")
    response_letter.append(float(convert.replace(",", ".")))
    return response_letter


def get_currency_price_translate(number_1, alpha, beta):
    if alpha != "rub" and beta == "rub":  # Если одна из выбраных валют - рубль
        # Нахождение актуальной информации о валюте
        currency_now = float(get_currency_price(alpha)[0])
        number = float(number_1.replace(",", "."))
        answer = int(((currency_now * number)) * 1000) / 1000  # Оформление ответа
        return answer  # Запись ответа
    if alpha == "rub" and beta != "rub":  # Если одна из выбраных валют - рубль
        currency_now = float(get_currency_price(beta)[0])
        number = float(number_1.replace(",", "."))
        answer = int(((number / currency_now)) * 1000) / 1000  # Оформление ответа
        return answer  # Запись ответа
    elif alpha != "rub" and beta != "rub":  # Если ни одна из валют рубль
        # Нахождение актуальной информации о валюте
        currency_now_left = float(get_currency_price(alpha)[0])
        # Нахождение актуальной информации о валюте
        currency_now_right = float(get_currency_price(beta)[0])
        number = float(number_1.replace(",", "."))
        rub = int(((number / currency_now_right)) * 1000000000) / 1000000000  # Перевод в рубли
        answer = int(((currency_now_left * rub)) * 1000) / 1000  # Оформление ответа
        return answer  # Запись ответа


# message
@client.event
@commands.has_permissions(administrator=True)
async def on_message(message):
    amount = 1
    msg = message.content.lower()
    if msg[0] != '.':
        for elem in msg.split(" "):
            if elem[-1].isalpha():  # ломается на моменте цикла, мб есть смысл поменять значение
                word = elem
            else:
                word = elem[:-1]
            if config.MORPH.parse(word)[0].normal_form in config.haram:
                author = message.author
                if author not in config.slaves.keys():
                    config.slaves[author] = 1
                    await message.channel.purge(limit=amount)
                    await message.channel.send('Пожалуйста, выражайтесь корректно)')
                    await message.channel.send(
                        f'{author.mention}, у тебя 1 просчет, грядет бан!')
                    break
                else:
                    if config.slaves[author] == 1:
                        config.slaves[author] = 2
                        await message.channel.purge(limit=amount)
                        await message.channel.send('Пожалуйста, выражайтесь корректно)')
                        await message.channel.send(
                            f'{author.mention}, еще раз, и получишь бан!')
                        break
                    elif config.slaves[author] == 2:
                        config.slaves[author] = 3
                        await message.channel.purge(limit=amount)
                        await message.channel.send('Пожалуйста, выражайтесь корректно)')
                        await message.channel.send(f'{author.mention}, take it, boy!')
                        break
            elif word in config.hello_world:
                await message.channel.send('Бонжур! Что-то интересует?')
                break
            elif word in config.antword:
                await message.channel.send('Напиши .help в чат для просмотра списка команд')
                break
            # elif "ты" == elem:
            #    await message.channel.send('ты Слава Мерлоу?')
            #    await message.channel.send(file=discord.File('ti.jpg'))
            #    break

    else:
        await client.process_commands(message)


# hello
@client.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(
        f'{author.mention}, приветствую, но не на немецком! | {author.mention}, привет! как дела?')


# translate
@client.command(pass_context=True)
async def translate(ctx, language_1, language_2, *text):
    translator = Translator(from_lang=language_1, to_lang=language_2)
    answer = []
    for elem in text:
        if elem[-1].isalpha():
            word = elem
            translation = translator.translate(word)
            answer.append(translation)
        else:
            word = elem[:-1]
            translation = translator.translate(word)
            answer.append(translation + elem[-1])
    await ctx.channel.send(" ".join(answer))


# auto role
# @client.event
# async def on_member_join(member):
#    channel = client.get_channel(748059364555751475)
#    role = discord.utils.get(member.guild.roles, id=689430828089868292)
#
#    await member.add_roles(role)
#    await channel.send(
#        embed=discord.Embed(discription=f'Пользователь ''{member.name}'' присоединился к серверу!',
#                            color=0x0c0c0c))

# ban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Ban', color=discord.Color.red())
    await member.ban(reason=reason)
    emb.set_author(name=member.name)
    emb.add_field(name='Ban user',
                  value='Banned user: {}'.format(member.mention))
    emb.set_footer(
        text='Был забанен администратором {}'.format(ctx.author.name))
    await ctx.send(embed=emb)


# unban
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Unban', color=discord.Color.green())
    await member.unban(reason=reason)
    emb.set_author(name=member.name)
    emb.add_field(name='Unban user',
                  value='Unbanned user: {}'.format(member.mention))
    emb.set_footer(
        text='Был разбанен администратором {}'.format(ctx.author.name))
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
    embed = discord.Embed(title="Dollar:",
                          description=f'Курс доллара в рублях: {get_currency_price("dollar")[0]}',
                          colour=discord.Colour.dark_gold())
    await ctx.send(embed=embed)


# euro
@client.command(pass_context=True)
async def euro(ctx):
    embed = discord.Embed(title="Euro:",
                          description=f'Курс евро в рублях: {get_currency_price("euro")[0]}',
                          colour=discord.Colour.dark_gold())
    await ctx.send(embed=embed)


# frank
@client.command(pass_context=True)
async def frank(ctx):
    embed = discord.Embed(title="Frank:",
                          description=f'Курс евро в рублях: {get_currency_price("frank")[0]}',
                          colour=discord.Colour.dark_gold())
    await ctx.send(embed=embed)


# translate
@client.command(pass_context=True)
async def translate_money(ctx, number_1, alpha, beta):
    embed = discord.Embed(title="Translate Money:",
                          description=f'{number_1} в {alpha} = {get_currency_price_translate(number_1, alpha, beta)} в {beta}',
                          colour=discord.Colour.dark_green())
    await ctx.send(embed=embed)


# weather 5 day
@client.command(pass_context=True)
async def weathers(ctx, pred_city):
    try:
        res1 = requests.get("http://api.openweathermap.org/data/2.5/find",
                            params={'q': pred_city, 'type': 'like',
                                    'units': 'metric', 'APPID': config.appid})
        data1 = res1.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data1['list']]
        city_id = data1['list'][0]['id']
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru',
                                   'APPID': config.appid})
    except ValueError:
        pass
    data = res.json()
    text = []
    for i in data['list']:
        text.append([i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']),
                     i['weather'][0]['description']])
    dateeee = []
    data_res = []
    text1 = text[0][0].split(' ')
    if text1[0] not in dateeee:
        dateeee.append(text1[0])
        text2 = [text1[0], text[0][1], text[0][2]]
        data_res.append(text2)
    for i in range(len(text)):
        text1 = text[i][0].split(' ')
        if text1[0] not in dateeee:
            dateeee.append(text1[0])
            text2 = [text1[0], text[i][1], text[i][2]]
            data_res.append(text2)
    a1 = data_res[0][1] + '°C' + ' ' + data_res[0][2]
    # не бейте
    a2 = data_res[1][1] + '°C' + ' ' + data_res[1][2]
    # не бейт°C
    a3 = data_res[2][1] + '°C' + ' ' + data_res[2][2]
    # не бейт°C
    a4 = data_res[3][1] + '°C' + ' ' + data_res[3][2]
    # не бейт°C
    a5 = data_res[4][1] + '°C' + ' ' + data_res[4][2]

    # не бейте, пожалуйста
    b1 = data_res[0][0] + " -- " + a1
    b2 = data_res[1][0] + " -- " + a2
    b3 = data_res[2][0] + " -- " + a3
    b4 = data_res[3][0] + " -- " + a4
    b5 = data_res[4][0] + " -- " + a5

    embed = discord.Embed(title=f"Прогноз погоды в {pred_city} на 5 дней:",
                          description=f"{b1}\n{b2}\n{b3}\n{b4}\n{b5}\n",
                          colour=discord.Colour.dark_purple())
    await ctx.send(embed=embed)


# weather one day
@client.command(pass_context=True)
async def weather(ctx, city):
    try:
        mgr = config.owm.weather_manager()
        observation = mgr.weather_at_place(city)  # тут ищем саму температуру
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        await ctx.send(f'Температура: {temp}°C')  # вот сама функция по выводу
        # погоды в городе
    except ValueError:
        pass
    yandex = requests.get('https://yandex.ru/pogoda/' + city)  # тут получаем
    # страницу с нужным нам городом
    yan1 = bs4.BeautifulSoup(yandex.text, 'html.parser')
    # wie = yan1.find('div', class_='link__feelings fact__feelings').text
    # в этомм классе содержится нужная нам информация
    # f = wie.split('Ощущается как')
    yand2 = requests.get('https://yandex.ru/pogoda/' + city)
    # находим страничку для нужного города
    yande2 = bs4.BeautifulSoup(yand2.text, 'html.parser')
    ya2 = str(yande2.find('span', "temp__value"))
    # ищем в коде страницы информацию о погоде
    f_one_21 = ya2.split('Текущая температура')
    yandex_two_2 = requests.get('https://yandex.ru/pogoda/' + city)
    yan_two_2 = bs4.BeautifulSoup(yandex_two_2.text, 'html.parser')
    wie_two_2 = str(yan_two_2.find('div',
                                   class_="term term_orient_v fact__wind-speed"))
    # ищам информацию о скорости ветра
    humidity_two_2 = str(yan_two_2.find('div',
                                        class_="term term_orient_v fact__humidity"))
    # ищем информацию о влажности
    f_two_2 = humidity_two_2.split('Влажность')
    s = "Влажность: " + f_two_2[0]
    w = "Ветер: " + wie_two_2
    # await ctx.send(f[0])  # выводим наше "состояние погоды"
    await ctx.send(s)  # выводим
    await ctx.send(w)  # выводим


# create_role
@client.command(pass_context=True)
async def create_role(ctx, *text):
    guild = ctx.guild
    text = ' '.join(text)
    await guild.create_role(name=text)
    embed = discord.Embed(title="Role: ", description=f"Роль {text} успешно создана :)",
                          colour=discord.Colour.blue())
    await ctx.send(embed=embed)


# mute
@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, connect=False,
                                          speak=False, send_messages=False,
                                          read_message_history=True, read_messages=False)
    embed = discord.Embed(title="Muted", description=f"{member.mention} был добавлен в мьют",
                          colour=discord.Colour.magenta())
    embed.add_field(name="Причина:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


# unmute
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(title="Unmute", description=f"{member.mention} больше не в мьюте",
                          colour=discord.Colour.gold())
    await ctx.send(embed=embed)


# help
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Список команд:', color=discord.Color.teal())
    emb.add_field(name='{}clear (n)'.format('.'), value='Очистка чата')
    emb.add_field(name='{}kick (member)'.format('.'), value='кик участника')
    emb.add_field(name='{}ban (member)'.format('.'), value='бан участника')
    emb.add_field(name='{}unban (member)'.format('.'), value='разбан участника')
    emb.add_field(name='{}join'.format('.'),
                  value='подключение бота к голосовому каналу')
    emb.add_field(name='{}leave'.format('.'),
                  value='отключение бота от голосового канала')
    emb.add_field(name='{}hello'.format('.'), value='Приветствие')
    emb.add_field(name='{}help'.format('.'), value='Список команд')
    emb.add_field(name='{}dollar'.format('.'), value='Курс доллара')
    emb.add_field(name='{}euro'.format('.'), value='Курс евро')
    emb.add_field(name='{}frank'.format('.'), value='Курс франка')
    emb.add_field(name='{}mute (member)'.format('.'), value='Мьют участника')
    emb.add_field(name='{}unmute (member)'.format('.'), value='Размьют участника')
    emb.add_field(name='{}weathers (city)'.format('.'), value='Прогноз погоды на 5 дней')
    emb.add_field(name='{}weather (city)'.format('.'), value='Прогноз погоды')
    emb.add_field(
        name='{}translate_money (quantity, first_currency, second_currency)'.format('.'),
        value='Перевод одной валюты в другую')
    emb.add_field(name='{}translate (first language, second language, text)'.format('.'),
                  value='Перевод (исходный язык, новый язык, текст)')
    await ctx.send(embed=emb)


client.run(config.TOKEN)
