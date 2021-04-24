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

TOKEN = '-'

MORPH = pymorphy2.MorphAnalyzer()

appid = "97150f95dc173b86e58b20c0754d2634"  # токен

base_url = "http://api.openweathermap.org/data/2.5/weather?"

owm = pyowm.OWM('97150f95dc173b86e58b20c0754d2634')  # это токен, который мы получаем

slaves = {}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.111 Safari/537.36'}

LINKS_DOLLAR = "https://www.google.com/search?sxsrf=ALeKk01-G5_9JcFxgjtDU7651F-Pn7Jyeg%3A1603202429242&ei" \
               "=fe2OX7OmDu6krgS49qMw&q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D1%80%D1" \
               "%83%D0%B1%D0%BB%D1%8E&oq=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp" \
               "=CgZwc3ktYWIQAxgAMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgQIABANMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgQIABBHUPMZWPYbYLkoaABwA3gAgAGGAYgB9AGSAQMwLjKYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab "

LINKS_EURO = "https://www.google.com/search?sxsrf=ALeKk035VJ5f25dYB621YODHsOewYnaCLg%3A1603876654233&ei" \
             "=LjeZX_nkDcPmrgTptq7QDg&q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B5%D0" \
             "%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp" \
             "=CgZwc3ktYWIQAzIHCAAQsQMQQzIECAAQQzIECAAQQzICCAAyAggAMgIIADICCAAyAggAMgcIABAUEIcCMgIIADoHCAAQRxCwAzoGCAAQBxAeOggIABAHEAoQHjoJCAAQsQMQBxAeOgQIABAKUPT9jwFY94WQAWDoh5ABaAJwAHgAgAF-iAG9BJIBAzAuNZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwj5s_SR-tbsAhVDs4sKHWmbC-oQ4dUDCA0&uact=5 "

LINKS_FRANK = "https://www.google.com/search?sxsrf=ALeKk01pScRniXA8RAy8HfnlTLSk0jCyAw%3A1603879015895&ei" \
              "=Z0CZX5WbNuH3qwG0jbrwDw&q=%D1%84%D1%83%D0%BD%D1%82+%D1%81%D1%82%D0%B5%D1%80%D0%BB%D0%B8%D0%BD%D0%B3%D0" \
              "%B0+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D1%84%D1%83%D0%BD%D1%82%D0%BA+%D1%80%D1%83%D0%B1%D0%BB" \
              "%D1%8E&gs_lcp=CgZwc3ktYWIQAxgBMgkIABCxAxAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BwgAEEcQsANQyooBWPGQAWCkqAFoAnAAeACAAYsBiAHWA5IBAzAuNJgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab "

POST_ID = 832997258868949013

ROLES = {
    '🍪': 832946932237991951,
    '🍩': 832956119533355008
}

citys = ''

EXCROLES = ()

MAX_ROLES_PER_USER = 3

client = commands.Bot(command_prefix='.')
client.remove_command('help')

hello_world = ['привет', 'hi', 'Hi', 'Hello', 'hello', 'qq', 'q', 'ky', 'Привет', 'здравствуйте',
               'Здравствуйте', 'Ку', 'здорова', 'Хеллоу', "хеллоу"]

antword = ['информация', 'команды', 'help',
           'Help', 'info', 'Info', 'что делать']

# осуждаем код ниже
haram = ['апездал', 'апездошенная', 'блядь', 'блять', 'блядство', 'выебон', 'выебать', 'вхуюжить',
         'гомосек', 'долбоёб',
         'ебло', 'еблище', 'ебать', 'ебическая сила', 'ебунок', 'еблан', 'ёбнуть', 'ёболызнуть',
         'ебош', 'заебал',
         'заебатый', 'злаебучий', 'заёб', 'иди на хуй', 'колдоебина', 'манда', 'мандовошка',
         'мокрощелка', 'наебка',
         'наебал', 'наебаловка', 'напиздеть', 'отъебись', 'охуеть', 'отхуевертить', 'опизденеть',
         'охуевший',
         'отебукать', 'пизда', 'пидарас', 'пиздатый', 'пиздец', 'пизданутый', 'поебать',
         'поебустика', 'проебать',
         'подзалупный', 'пизденыш', 'припиздак', 'разъебать', 'распиздяй', 'разъебанный', 'сука',
         'сучка', 'трахать',
         'уебок', 'уебать', 'угондошить', 'уебан', 'хитровыебанный', 'нахуй', 'хуй', 'хуйня',
         'заебать', 'пидор', 'бля', 'заебал', 'заебешь']
