# Импортируем необходимые классы.
from telegram import Bot, Message
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import get_image
from pyrogram import Client

api_id = 2068353
api_hash = "6dab5b1a12075e923bfb7201e698bf4b"
app = Client("my_account", api_id, api_hash)


TOKEN = "1793035255:AAFjDGWFPHN3qjiM6kVrpC44YqmZos38KrI"
dog_link = 'https://random.dog/woof.json'
cat_link = "https://api.thecatapi.com/v1/images/search"
# Определяем функцию-обработчик сообщений.
# У неё два параметра, сам бот и класс updater, принявший сообщение.
dubu = Bot(TOKEN)
def mother(update, context):
    text = update.message.text
    if text.startswith('dubu ') or text.startswith('дубу '):
        dubu.send_message(update.effective_chat.id, text[5:])
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.


def start(update, context):
    dubu.send_message(update.effective_chat.id, 'dubu is running')


def random_dog(update, context):
    url = get_image.get_image_url(dog_link)
    update.message.reply_photo(photo=url, quote=True)


def random_cat(update, context):
    url = get_image.get_image_url(cat_link)
    update.message.reply_photo(photo=url, quote=True)


def help(update, context):
    dubu.send_message(update.effective_chat.id, """привки няшки! я дубу :)
ничего пока толком не могу но...
    
/start - выводится сообщение о том, работает ли сейчас бот
dubu/дубу (message) - напечатаю ваше сообщение <3
/help - хелп он и в африке хелп...
    
стэньте твайс.""")


def main():
    # Создаём объект updater.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    updater = Updater(TOKEN, use_context=True)
    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаём обработчик сообщений типа Filters.text
    # из описанной выше функции echo()
    # После регистрации обработчика в диспетчере
    # эта функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, mother)
    # Регистрируем обработчик в диспетчере.
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('dog', random_dog))
    dp.add_handler(CommandHandler('cat', random_cat))
    dp.add_handler(text_handler)

    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()
    # Ждём завершения приложения.
    # (например, получения сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()