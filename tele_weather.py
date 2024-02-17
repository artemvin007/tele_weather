
import pyowm  # Импортируем пакет с помощью которого мы узнаем погоду
import telebot  # Импортируем пакет бота через ввод в CMD "pip install pytelegrambotapi"
import time

owmToken = '0dde369d6504f5f84f2596b7fb73b966'
owm = pyowm.OWM(owmToken)
botToken = '6534262803:AAG8rjKkyAgZAw9qi85JsppD27TuUi_RCqI'
bot = telebot.TeleBot(botToken)


# Когда боту пишут текстовое сообщение вызывается эта функция
@bot.message_handler(content_types=['text'])
def send_message(message):
    """Send the message to user with the weather"""
    # Отдельно реагируем на сообщения /start и /help

    if message.text.lower() == "/start" or message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    else:
        # С помощью try заставляю пройти код, если функция observation не находит город
        # и выводит ошибку, то происходит переход к except
        try:
            # Имя города пользователь вводит в чат, после этого мы его передаем в функцию
            observation = owm.weather_manager()
            weather = observation.weather_at_place(message.text).weather
            temp = weather.temperature("celsius")['temp']
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), temp, "C")

            answer = "В этом городе: " + str(temp) + "°C" + "\nОтносительная влажность: " + str(weather.humidity) + "%\n"

            if weather.clouds < 25:
                answer += "Безоблачно"
            elif weather.clouds < 50:
                answer += "Немного облачно"
            elif weather.clouds < 75:
                answer += "Облачно"
            else:
                answer += "Пасмурно"

        except Exception:
            answer = "Не найден город, попробуйте ввести название снова.\n"
            print(time.ctime(), "User id:", message.from_user.id)
            print(time.ctime(), "Message:", message.text.title(), 'Error')

        bot.send_message(message.chat.id, answer)  # Ответить сообщением


# Запускаем бота
if __name__ == __name__:
    bot.polling(none_stop=True)
