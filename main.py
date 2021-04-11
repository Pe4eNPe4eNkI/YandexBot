import discord
from discord.ext import commands
from discord.utils import get
import requests
import pyowm
import bs4
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36'}

LINKS_DOLLAR = "https://www.google.com/search?sxsrf=ALeKk01-G5_9JcFxgjtDU7651F-Pn7Jyeg%3A1603202429242&ei" \
               "=fe2OX7OmDu6krgS49qMw&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1" \
               "%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp" \
               "=CgZwc3ktYWIQAxgAMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgQIABANMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgQIABBHUPMZWPYbYLkoaABwA3gAgAGGAYgB9AGSAQMwLjKYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab "

appid = "97150f95dc173b86e58b20c0754d2634"  # токен
owm = pyowm.OWM('97150f95dc173b86e58b20c0754d2634')  # это токен, который мы получаем

LINKS_EURO = "https://www.google.com/search?sxsrf=ALeKk035VJ5f25dYB621YODHsOewYnaCLg%3A1603876654233&ei" \
             "=LjeZX_nkDcPmrgTptq7QDg&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B5%D0" \
             "%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp" \
             "=CgZwc3ktYWIQAzIHCAAQsQMQQzIECAAQQzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgcIABAUEIcCMgIIADoHCAAQRxCwAzoGCAAQBxAeOggIABAHEAoQHjoJCAAQsQMQBxAeOgQIABAKUPT9jwFY94WQAWDoh5ABaAJwAHgAgAF-iAG9BJIBAzAuNZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwj5s_SR-tbsAhVDs4sKHWmbC-oQ4dUDCA0&uact=5 "

LINKS_FRANK = "https://www.google.com/search?sxsrf=ALeKk01pScRniXA8RAy8HfnlTLSk0jCyAw%3A1603879015895&ei" \
              "=Z0CZX5WbNuH3qwG0jbrwDw&q=%D1%84%D1%83%D0%BD%D1%82+%D1%81%D1%82%D0%B5%D1%80%D0%BB%D0%B8%D0%BD%D0%B3%D0" \
              "%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D1%84%D1%83%D0%BD%D1%82%D0%BA+%D1%80%D1%83%D0%B1%D0%BB" \
              "%D1%8E&gs_lcp=CgZwc3ktYWIQAxgBMgkIABCxAxAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BwgAEEcQsANQyooBWPGQAWCkqAFoAnAAeACAAYsBiAHWA5IBAzAuNJgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab "

client = commands.Bot(command_prefix='.')
client.remove_command('help')

hello_world = ['привет', 'hi', 'Hi', 'Hello', 'hello', 'qq', 'q', 'ky', 'Привет', 'здравствуйте',
               'Здравствуйте', 'Ку', 'здорова', 'Хеллоу', "хеллоу"]
antword = ['информация', 'команды', 'help',
           'Help', 'info', 'Info', 'что делать']
haram = ['апездал', 'апездошенная', 'блядь', 'блядство', 'выебон', 'выебать', 'вхуюжить', 'гомосек', 'долбоёб',
         'ебло', 'еблище', 'ебать', 'ебическая сила', 'ебунок', 'еблан', 'ёбнуть', 'ёболызнуть', 'ебош', 'заебал',
         'заебатый', 'злаебучий', 'заёб', 'иди на хуй', 'колдоебина', 'манда', 'мандовошка', 'мокрощелка', 'наебка',
         'наебал', 'наебаловка', 'напиздеть', 'отъебись', 'охуеть', 'отхуевертить', 'опизденеть', 'охуевший',
         'отебукать', 'пизда', 'пидарас', 'пиздатый', 'пиздец', 'пизданутый', 'поебать', 'поебустика', 'проебать',
         'подзалупный', 'пизденыш', 'припиздак', 'разъебать', 'распиздяй', 'разъебанный', 'сука', 'сучка', 'трахать',
         'уебок', 'уебать', 'угондошить', 'уебан', 'хитровыебанный', 'хуй', 'хуйня', 'заебешь',
         'пидор', 'бля', 'заебешь']


def get_currency_price(name):
    if name == "dollar":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(LINKS_DOLLAR, headers=HEADERS)
    elif name == "euro":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(LINKS_EURO, headers=HEADERS)
    elif name == "frank":
        response_letter = []
        # Подключение ссылки
        full_page = requests.get(LINKS_FRANK, headers=HEADERS)

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
async def on_message(message, amount=1):
    msg = message.content.lower()
    for elem in msg.split(" "):
        if elem[-1].isalpha():
            word = elem
        else:
            word = elem[:-1]
        if word in haram:
            await message.channel.purge(limit=amount)
            await message.channel.send('Пожалуйста, выражайтесь корректно)')
            break
        elif word in hello_world:
            await message.channel.send('Бонжюр! Что-то интересует?')
            break
        elif word in antword:
            await message.channel.send('Напиши .help в чат для просмотра списка команд')
            break


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
        f'Курс доллара в рублях: {get_currency_price("dollar")[0]}')


# euro
@client.command(pass_context=True)
async def euro(ctx):
    await ctx.send(
        f'Курс евро в рублях: {get_currency_price("euro")[0]}')


# frank
@client.command(pass_context=True)
async def frank(ctx):
    await ctx.send(
        f'Курс франка в рублях: {get_currency_price("frank")[0]}')


# translate
@client.command(pass_context=True)
async def translate(ctx, number_1, alpha, beta):
    await ctx.send(
        f'{number_1} в {alpha} = {get_currency_price_translate(number_1, alpha, beta)} в {beta}')


# help
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title='Список команд:')

    emb.add_field(name='{}clear (n)'.format('.'), value='Очистка чата')
    emb.add_field(name='{}kick (name)'.format('.'), value='кик участника')
    emb.add_field(name='{}ban (name)'.format('.'), value='бан участника')
    emb.add_field(name='{}unban (name)'.format('.'), value='разбан участника')
    emb.add_field(name='{}join'.format('.'),
                  value='подключение бота к голосовому каналу')
    emb.add_field(name='{}leave'.format('.'),
                  value='отключение бота от голосового канала')
    emb.add_field(name='{}hello'.format('.'), value='Приветствие')
    emb.add_field(name='{}help'.format('.'), value='Список команд')
    emb.add_field(name='{}dollar'.format('.'), value='Курс доллара')
    emb.add_field(name='{}euro'.format('.'), value='Курс евро')
    emb.add_field(name='{}frank'.format('.'), value='Курс франка')
    emb.add_field(name='{}weathers (city)'.format('.'), value='Прогноз погоды на 5 дней')
    emb.add_field(name='{}weather (city)'.format('.'), value='Прогноз погоды')

    emb.add_field(name='{}translate (quantity, first_currency, second_currency)'.format('.'),
                  value='Перевод одной валюты в другую')

    await ctx.send(embed=emb)


# weather 5 day
@client.command(pass_context=True)
async def weathers(ctx,
                   pred_city):  # тут мы с помощью цыганских махинаций передаем город и он находит его на сайте
    try:

        res1 = requests.get("http://api.openweathermap.org/data/2.5/find",
                            params={'q': pred_city, 'type': 'like',
                                    'units': 'metric', 'APPID': appid})
        data1 = res1.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data1['list']]
        city_id = data1['list'][0]['id']

        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru',
                                   'APPID': appid})
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
    b1 = data_res[0][0] + " - " + a1
    b2 = data_res[1][0] + " - " + a2
    b3 = data_res[2][0] + " - " + a3
    b4 = data_res[3][0] + " - " + a4
    b5 = data_res[4][0] + " - " + a5
    mes = "Прогноз погоды в " + pred_city + ' на 5 дней:'
    await ctx.send(mes)  # не бейте, пожалуйста
    await ctx.send(b1)  # не бейте, пожалуйста
    await ctx.send(b2)  # не бейте, пожалуйста
    await ctx.send(b3)  # не бейте, пожалуйста
    await ctx.send(b4)  # не бейте, пожалуйста
    await ctx.send(b5)  # не бейте, пожалуйста


# weather one day
@client.command(pass_context=True)
async def weather(ctx, city):
    try:
        mgr = owm.weather_manager()

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
    wie = yan1.find('div', class_='link__feelings fact__feelings').text
    # в этомм классе содержится нужная нам информация
    f = wie.split('Ощущается как')

    yand2 = requests.get('https://yandex.ru/pogoda/' + city)
    # находим страничку для нужного города
    yande2 = bs4.BeautifulSoup(yand2.text, 'html.parser')
    ya2 = yande2.find('span', "temp__value").text
    # ищем в коде страницы информацию о погоде
    f_one_21 = ya2.split('Текущая температура')

    yandex_two_2 = requests.get('https://yandex.ru/pogoda/' + city)
    yan_two_2 = bs4.BeautifulSoup(yandex_two_2.text, 'html.parser')
    wie_two_2 = yan_two_2.find('div',
                               class_="term term_orient_v fact__wind-speed").text
    # ищам информацию о скорости ветра
    humidity_two_2 = yan_two_2.find('div',
                                    class_="term term_orient_v fact__humidity").text
    # ищем информацию о влажности
    f_two_2 = humidity_two_2.split('Влажность')

    s = "Влажность: " + f_two_2[0]
    w = "Ветер: " + wie_two_2
    await ctx.send(f[0])  # выводим наше "состояние погоды"
    await ctx.send(s)  # выводим
    await ctx.send(w)  # выводим


# get token
# token = open('token.txt', 'r').readline()
token = "-"

client.run(token)
