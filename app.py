from aiogram import Bot, Dispatcher, executor, types
import sqlite3
from newsapi import NewsApiClient
tok = ''
newsapi = NewsApiClient(api_key='')
class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    def get_users(self, status = True):
        with self.connection:
            return self.cursor.execute('SELECT * FROM `users` WHERE `status` = ?', (status,)).fetchall()
    def users_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
    def add_users(self, user_id, status = True):
        with self.connection:
            return self.cursor.execute('INSERT INTO `users` (`user_id`, `status`) VALUES(?,?)', (user_id,status))
    def update_users(self, user_id, status):
        with self.connection:
            return self.cursor.execute('UPDATE `users` SET `status` = ? WHERE `user_id` = ?', (status, user_id))
    def get_key(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT key FROM `keywords` WHERE `user_id` = ?', (user_id,)).fetchall()
    def key_exists(self, user_id, key):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `keywords` WHERE `user_id` = ? AND `key` = ?', (user_id, key)).fetchall()
            return bool(len(result))
    def add_key(self, user_id, key):
        with self.connection:
            return self.cursor.execute('INSERT INTO `keywords` (`user_id`, `key`) VALUES(?,?)', (user_id,key))
    def del_key(self, user_id, key):
        with self.connection:
            result = self.cursor.execute('DELETE FROM `keywords` WHERE `user_id` = ? AND `key` = ?', (user_id, key)).fetchall()
            return bool(len(result))
    def get_categ(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT name FROM `categories` WHERE `user_id` = ?', (user_id,)).fetchall()
    def categ_exists(self, user_id, name):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `categories` WHERE `user_id` = ? AND `name` = ?', (user_id, name)).fetchall()
            return bool(len(result))
    def add_categ(self, user_id, name):
        with self.connection:
            return self.cursor.execute('INSERT INTO `categories` (`user_id`, `name`) VALUES(?,?)', (user_id,name))
    def del_categ(self, user_id, name):
        with self.connection:
            result = self.cursor.execute('DELETE FROM `categories` WHERE `user_id` = ? AND `name` = ?', (user_id, name)).fetchall()
            return bool(len(result))
    def close(self):
        self.connection.close()
base = SQLighter('base.db')
bot = Bot(token = tok)
dp = Dispatcher(bot)
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not base.users_exists(message.from_user.id)):
        base.add_users(message.from_user.id)
    else:
        base.update_users(message.from_user.id, True)
    await message.answer('Вы успешно подписались на рассылку')
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not base.users_exists(message.from_user.id)):
        base.add_users(message.from_user.id, False)
        await message.answer('Вы небыли подписаны')
    else:
        base.update_users(message.from_user.id, False)
        await message.answer('Вы успешно отписаны от рассылки')
@dp.message_handler(commands=['addk'])
async def subscribek2(message: types.Message):
    keyw = ((message.text)[6:]).strip()
    if keyw != '':
        if (not base.key_exists(message.from_user.id, keyw)):
            base.add_key(message.from_user.id, keyw)
            await message.answer('Вы успешно подписались на ключевое слово')
        else:
            await message.answer('Вы уже подписаны на это ключевое слово')
    else:
        await message.answer('Недопустимое название для ключевого слова')

@dp.message_handler(commands=['delk'])
async def unsubscribek2(message: types.Message):
    keyww = ((message.text)[6:]).strip()
    if (not base.key_exists(message.from_user.id, keyww)):
        await message.answer('Вы небыли подписаны на это ключевое слово')
    else:
        base.del_key(message.from_user.id, keyww)
        await message.answer('Вы успешно отписаны от ключевого слова')
@dp.message_handler(commands=['showk'])
async def showk(message: types.Message):
    await message.answer('Список ключевых слов в подписке:')
    inp = base.get_key(message.from_user.id)
    for i in range(len(inp)):
        inp2 = str(inp[i])
        await message.answer(inp2[2:-3])
@dp.message_handler(commands=['addc'])
async def subscribec(message: types.Message):
    kateg = ((message.text)[6:]).strip()
    if kateg in ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']:
        if (not base.categ_exists(message.from_user.id, kateg)):
            base.add_categ(message.from_user.id, kateg)
            await message.answer('Вы успешно подписались на категорию')
        else:
            await message.answer('Вы уже подписаны на эту категорию')
    else:
        await message.answer('Недопустимое название для '
'категории\nПопробуйте:\nbusiness\nentertainment\ngeneral\nhealth\nscience\nsports\ntechnology')
@dp.message_handler(commands=['delc'])
async def unsubscribec(message: types.Message):
    kategg = ((message.text)[6:]).strip()
    if (not base.categ_exists(message.from_user.id, kategg)):
        await message.answer('Вы небыли подписаны на эту категорию')
    else:
        base.del_categ(message.from_user.id, kategg)
        await message.answer('Вы успешно отписаны от категории')
@dp.message_handler(commands=['showc'])
async def showc(message: types.Message):
    await message.answer('Список категорий в подписке:')
    inp = base.get_categ(message.from_user.id)
    for i in range(len(inp)):
        inp2 = str(inp[i])
        await message.answer(inp2[2:-3])
@dp.message_handler(commands=['newsc'])
async def news15(message: types.Message):
    inp = base.get_categ(message.from_user.id)
    for i in range(len(inp)):
        inp2 = str(inp[i])[2:-3]
        top_headlines = newsapi.get_top_headlines(category=inp2)
        sources = newsapi.get_sources()
        await message.answer('Топ 10 новостей по категории')
        for i in range(10):
            newstext = (top_headlines['articles'][i])
            a = newstext['title']
            b = newstext['url']
            await message.answer('<a href="{}">{}</a>'.format(b, a), parse_mode='html')
@dp.message_handler(commands=['newsk'])
async def news17(message: types.Message):
    inp = base.get_key(message.from_user.id)
    for i in range(len(inp)):
        inp2 = str(inp[i])[2:-3]
        all_articles = newsapi.get_everything(q= inp2, sort_by='relevancy')
        sources = newsapi.get_sources()
        await message.answer('Топ 10 новостей по ключевому слову')
        for i in range(10):
            newstext = (all_articles['articles'][i])
            a = newstext['title']
            b = newstext['url']
            await message.answer('<a href="{}">{}</a>'.format(b, a), parse_mode='html')
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Добро пожаловать в новостной бот\nИспользуйте подсказки в команде /help')

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer('/subscribe - Подписаться на бота\n/addk text - Подписаться на ключ.слово text\n/delk text'
' - Отписаться от ключ.слова text\n/showk - Посмотреть подписки на ключ.слова\n/addc text - Подписаться на категорию'
' text\n/delc text - Отписаться от категории text\n/showc - Посмотреть подписки на категории\n/newsc - Получить 10 '
'свежих новостей для каждого ключ.слова\n/newsk - Получить 10 релевантных новостей для каждой категории\n/unsubscribe '
'- Отписаться от бота')
executor.start_polling(dp, skip_updates=True)