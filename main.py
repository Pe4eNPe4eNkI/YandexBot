# Импорт библиотек
import translate
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
import os

client = commands.Bot(command_prefix='.')
client.remove_command('help')


# Подключение бота к каналу
@client.event
async def on_ready():
    print('Connected')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('Yandex.Lyceum | .help'))


# Реакции бота на смайлики
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


# Удаление ролей
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


# Вывод данных о валюте
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


# Калькулятор валют
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


# Реакции на слова в сообщениях
@client.event
@commands.has_permissions(administrator=True)
async def on_message(message):
    amount = 1
    msg = message.content.lower()
    if msg[0] != '.':
        for elem in msg.split(" "):
            if elem[-1].isalpha():
                word = elem
            else:
                word = elem[:-1]
            # Выявление нецензурной брани
            if config.MORPH.parse(word)[0].normal_form in config.haram:
                author = message.author
                if author.guild_permissions.administrator:
                    await message.channel.send('Мой master может материться столько, сколько хочет)')
                elif author not in config.slaves.keys():
                    config.slaves[author] = 1
                    await message.channel.purge(limit=amount)
                    await message.channel.send('Пожалуйста, выражайтесь корректно)')
                    await message.channel.send(
                        f'{author.mention}, у тебя 1 просчет, грядет бан!')
                    print(config.slaves)
                    break
                else:
                    if config.slaves[author] == 0:
                        config.slaves[author] = 1
                        await message.channel.purge(limit=amount)
                        await message.channel.send('Пожалуйста, выражайтесь корректно)')
                        await message.channel.send(
                            f'{author.mention}, у тебя 1 просчет, грядет бан!')
                        print(config.slaves)
                        break
                    elif config.slaves[author] == 1:
                        config.slaves[author] = 2
                        await message.channel.purge(limit=amount)
                        await message.channel.send('Пожалуйста, выражайтесь корректно)')
                        await message.channel.send(
                            f'{author.mention}, еще раз, и получишь бан!')
                        print(config.slaves)
                        break
                    elif config.slaves[author] == 2:
                        config.slaves[author] = 3
                        await message.channel.purge(limit=amount)
                        await message.channel.send('Пожалуйста, выражайтесь корректно)')
                        await message.channel.send(f'{author.mention}, take it, boy!')
                        print(config.slaves)
                        # ban
                        emb = discord.Embed(title='Ban', color=discord.Color.red())
                        await author.ban(reason=None)
                        emb.set_author(name=author.name)
                        emb.add_field(name='Ban user',
                                      value='Banned user: {}'.format(author.mention))
                        emb.set_footer(text='Был забанен за нецензурную лексику')
                        await message.channel.send(embed=emb)
                        break
            # Приветствие
            elif word in config.hello_world:
                await message.channel.send('Бонжур! Что-то интересует?')
                break
            elif word in config.antword:
                await message.channel.send('Напиши .help в чат для просмотра списка команд')
                break
            # elif "ты" == elem:
                # await message.channel.send('ты Слава Мерлоу?')
                # await message.channel.send(file=discord.File('ti.jpg'))
                # break
    else:
        await client.process_commands(message)


# Приветствие по команде
@client.command(pass_context=True)
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(
        f'{author.mention}, приветствую, но не на немецком! | {author.mention}, привет! как дела?')


# Переводчик на другой язык
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


# Бан
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Ban', color=discord.Color.red())
    await member.ban(reason=reason)
    emb.set_author(name=member.name)
    emb.add_field(name='Ban user',
                  value='Banned user: {}'.format(member.mention))
    emb.set_thumbnail(url="https://i.ytimg.com/vi/MTh5nRh8cHc/maxresdefault.jpg")

    emb.set_footer(
        text='Был забанен администратором {}'.format(ctx.author.name))
    await ctx.send(embed=emb)


# Вывод из бана
@client.command(pass_context=True)
async def unban(ctx, names):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = names.split('#')
    member_a = '@' + names
    print(member_a)

    emb = discord.Embed(title='Unban', color=discord.Color.green())
    emb.add_field(name='Unban user',
                  value='Unbanned user: {}'.format(member_name))
    emb.set_thumbnail(url="https://i.ytimg.com/vi/Dfjnztl-R0Q/maxresdefault.jpg")
    emb.set_footer(
        text='Был разбанен администратором {}'.format(ctx.author.name))
    await ctx.send(embed=emb)

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) != (member_name, member_discriminator):
            await ctx.guild.unban(user)


# Кик с сервера
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Kick', color=discord.Color.red())
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    emb.set_author(name=member.name)
    emb.add_field(name='Kick user',
                  value='Kicked user: {}'.format(member.mention))
    emb.set_thumbnail(
        url="https://www.pngkit.com/png/detail/369-3694735_this-is-an-image-of-a-person-kicking.png")
    emb.set_footer(text='Был кикнут администратором{}'.format(ctx.author.name))
    await ctx.send(embed=emb)


# Удаление сообщений
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.channel.purge(limit=amount)


# Вступление в голосовой чат
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


# Выход из голосового чата
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


# Курс доллара
@client.command(pass_context=True)
async def dollar(ctx):
    embed = discord.Embed(title="Dollar:",
                          description=f'Курс доллара в рублях: {get_currency_price("dollar")[0]}',
                          colour=discord.Colour.dark_gold())
    embed.set_thumbnail(
        url="https://www.publicdomainpictures.net/pictures/40000/velka/dollar-sign-black.jpg")

    await ctx.send(embed=embed)


# Курс евро
@client.command(pass_context=True)
async def euro(ctx):
    embed = discord.Embed(title="Euro:",
                          description=f'Курс евро в рублях: {get_currency_price("euro")[0]}',
                          colour=discord.Colour.dark_gold())
    embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2014/09/19/13/10/euro-452467_1280.jpg")

    await ctx.send(embed=embed)


# Курс франка
@client.command(pass_context=True)
async def frank(ctx):
    embed = discord.Embed(title="Frank:",
                          description=f'Курс евро в рублях: {get_currency_price("frank")[0]}',
                          colour=discord.Colour.dark_gold())
    embed.set_thumbnail(
        url="https://s3.amazonaws.com/static.graphemica.com/glyphs/i500s/000/012/491/original/20A3-500x500.png?1275331266")

    await ctx.send(embed=embed)


# Переводчик одной валюты в другую
@client.command(pass_context=True)
async def translate_money(ctx, number_1, alpha, beta):
    embed = discord.Embed(title="Translate Money:",
                          description=f'{number_1} в {alpha} = {get_currency_price_translate(number_1, alpha, beta)} в {beta}',
                          colour=discord.Colour.dark_green())
    embed.set_thumbnail(
        url="https://lh3.googleusercontent.com/ViS41J5SwDI91ZFNb5BX5fMmWqpdNp8qp6t8imv23OEF6mQomDhXcHL_Pg_cvpkXkhbJ")
    await ctx.send(embed=embed)


# Погода на 5 дней
@client.command(pass_context=True)
async def weather_n(ctx, pred_city):
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
    embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
    await ctx.send(embed=embed)


# Подробная погода на день
@client.command(pass_context=True)
async def weather(ctx, *, city: str):
    city_name = city
    complete_url = config.base_url + "appid=" + config.appid + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    channel = ctx.message.channel
    if x["cod"] != "404":
        async with channel.typing():
            y = x["main"]
            current_temperature = y["temp"]
            current_temperature_celsiuis = str(round(current_temperature - 273.15))
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            embed = discord.Embed(title=f"Погода в {city_name}",
                                  color=ctx.guild.me.top_role.color,
                                  timestamp=ctx.message.created_at, )
            embed.add_field(name="Описание", value=f"**{weather_description}**", inline=False)
            embed.add_field(name="Температура(C)", value=f"**{current_temperature_celsiuis}°C**",
                            inline=False)
            embed.add_field(name="Влажность(%)", value=f"**{current_humidity}%**", inline=False)
            embed.add_field(name="Атмосферное давление(hPa)", value=f"**{current_pressure}hPa**",
                            inline=False)
            embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
            embed.set_footer(text=f"Запрошено {ctx.author.name}")
            await channel.send(embed=embed)
    else:
        await channel.send("Город не найден.")


# Создание роли
@client.command(pass_context=True)
async def create_role(ctx, *text):
    guild = ctx.guild
    text = ' '.join(text)
    await guild.create_role(name=text)
    embed = discord.Embed(title="Role: ", description=f"Роль {text} успешно создана :)",
                          colour=discord.Colour.blue())
    embed.set_thumbnail(
        url="https://www.pikpng.com/pngl/b/443-4431813_png-file-svg-roles-icon-transparent-clipart.png")
    await ctx.send(embed=embed)


# Отправка человека в мут
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
    embed.set_thumbnail(
        url="https://www.pngkey.com/png/detail/215-2154601_mute-unmute-mute-unmute-icon-png.png")
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


# Вывод человека из мута
@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(title="Unmute", description=f"{member.mention} больше не в мьюте",
                          colour=discord.Colour.gold())
    embed.set_thumbnail(
        url="https://cdn0.iconfinder.com/data/icons/prohibition/100/prohibition_prohibited_prohibit-10-512.png")
    await ctx.send(embed=embed)


# Вызов подсказки
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Список команд:', color=discord.Color.teal())
    emb.add_field(name='{}clear (n)'.format('.'), value='Очистка чата')
    emb.add_field(name='{}kick (member)'.format('.'), value='кик участника')
    emb.add_field(name='{}ban (member)'.format('.'), value='бан участника')
    emb.add_field(name='{}unban (member#discriminator)'.format('.'), value='разбан участника')
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
    emb.add_field(name='{}weather_n (city)'.format('.'), value='Прогноз погоды на 5 дней')
    emb.add_field(name='{}weather (city)'.format('.'), value='Прогноз погоды')
    emb.add_field(
        name='{}translate_money (quantity, first_currency, second_currency)'.format('.'),
        value='Перевод одной валюты в другую')
    emb.add_field(name='{}translate (first language, second language, text)'.format('.'),
                  value='Перевод (исходный язык, новый язык, текст)')
    emb.set_thumbnail(url="https://psv4.userapi.com/c520036/u208096156/docs/d2/e51f8cf6c035/16c.png?extra=5oSt8tGehVe-5C8MCMN7Hs_UMmW9LphBY3c93tA9wSeyXYmgtTpgZqcirTfBDkM0aE8docG_yzlfFlk8K7TSVMyNDYGT-cKQ6zsNnfZG-kql1cxS3IINzM-RXJGc3xCx0JTJrW7qXBqYl2rE0NroYjk")

    await ctx.send(embed=emb)

# Получение токена с Heroku
token = os.environ.get("BOT_TOKEN")
# Запуск программы
client.run(str(token))
