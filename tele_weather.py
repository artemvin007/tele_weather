import pyowm #api for weather reading
import telebot #telegram api
from telebot import custom_filters
import time

owm = pyowm.OWM('0dde369d6504f5f84f2596b7fb73b966')
bot = telebot.TeleBot('6534262803:AAG8rjKkyAgZAw9qi85JsppD27TuUi_RCqI')\

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.from_user.id, "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    bot.set



@bot.message_handler()
def send_message(message):
    """Send the message to user with the weather"""
    try:
        bot.send_message(message.chat.id, get_weather(message.text))  # Ответить сообщением
        print(time.ctime(), "User id:", message.from_user.id)
        print(time.ctime(), "Message:", message.text.title())
    except Exception:
        print(time.ctime(), "User id:", message.from_user.id)
        print(time.ctime(), "Message:", message.text.title(), 'Error')
        send_message(message.chat.id, "Не найден город, попробуйте ввести название снова.\n")

def get_weather(city):
    observation = owm.weather_manager()
    weather = observation.weather_at_place(city).weather
    temp = weather.temperature("celsius")['temp']

    answer = "В этом городе: " + str(temp) + "°C" + "\nОтносительная влажность: " + str(weather.humidity) + "%\n"

    if weather.clouds < 25:
        answer += "Безоблачно"
    elif weather.clouds < 50:
        answer += "Немного облачно"
    elif weather.clouds < 75:
        answer += "Облачно"
    else:
        answer += "Пасмурно"
    return answer




if __name__ == __name__:
    bot.polling(none_stop=True)
