import pyowm #api for weather reading
import telebot #telegram api
from telebot import types
import time
from datetime import datetime
from pytz import timezone


bot = telebot.TeleBot('6534262803:AAG8rjKkyAgZAw9qi85JsppD27TuUi_RCqI')
owm = pyowm.OWM('0dde369d6504f5f84f2596b7fb73b966')

class City:
    def __init__(self, name, composition, photos):
        self.menu = [
            name,
            "Узнать погоду",
            "Узнать время",
            "Посмотреть отели",
            "Выбрать другой город"
        ]
        self.name = name
        self.composition = composition
        self.photos = photos

    def get_weather(self):
        observation = owm.weather_manager()
        weather = observation.weather_at_place(self.name).weather
        temp = weather.temperature("celsius")['temp']

        answer = "В этом городе: " + str(temp) + "°C" + "\nОтносительная влажность: " + str(
            weather.humidity) + "%\n"

        if weather.clouds < 25:
            answer += "Безоблачно"
        elif weather.clouds < 50:
            answer += "Немного облачно"
        elif weather.clouds < 75:
            answer += "Облачно"
        else:
            answer += "Пасмурно"
        return answer

    def get_time(self):
        try:
            # Определяем часовой пояс для введенного города
            city_timezone = timezone(self.name)
            # Конвертируем текущее время в часовой пояс города
            city_time = datetime.now(city_timezone)

            # Форматируем и выводим время
            return city_time.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return f"Ошибка: {e}"


menu = {
    "city_choise_menu": {
        "Горно-Алтайск": City("Горно-Алтайск",
                              "В краю гор, лесов, бурных рек и чистейших озер до сих пор чтут традиции предков и радушно встречают путешественников. Регион ежегодно принимает порядка двух миллионов человек. Путешественники выбирают экологический, аграрный, гастрономический, познавательный или спортивный туризм, кто-то объединяет несколько направлений.Здесь находится самая высокая точка Сибири и одна из крупнейших горных вершин России — гора Белуха, или Музтау Шыны. Местные зачастую называют гору Уч-Сюре, что переводится как «жилище трех богов». Именно эта гора изображена на гербе Республики Алтай.",
                              ["Горно-Алтайск1.jpeg", "Горно-Алтайск2.jpeg", "Горно-Алтайск3.jpeg"]),
    },
    "current_city": None
}

def create_markup(menu_items):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in (menu_items):
        markup.add(types.KeyboardButton(i))
    return markup

@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(
        message.from_user.id, "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n",
        reply_markup=create_markup(menu["city_choise_menu"].keys())
    )



@bot.message_handler(content_types=["text"])
def send_message(message):
    """Send the message to user with the weather"""
    try:
        print(time.ctime(), "User id:", message.from_user.id)
        print(time.ctime(), "Message:", message.text.title())
        if (menu["current_city"] == None):
            if (message.text in menu["city_choise_menu"].keys()):
                menu["current_city"] = menu["city_choise_menu"][message.text]
            else:
                menu["current_city"] = City(message.text, "Это отличный город!", ["default.png"])

        if (menu["current_city"] != None):
            if (message.text == menu["current_city"].name):
                bot.send_message(message.chat.id, menu["current_city"].name)
                for i in menu["current_city"].photos:
                    bot.send_photo(message.chat.id, open(i, "rb"))
                bot.send_message(message.chat.id, menu["current_city"].composition, reply_markup=create_markup(menu["current_city"].menu))
            if (message.text == "Узнать погоду"):
                bot.send_message(message.chat.id, menu["current_city"].get_weather())
            if(message.text == "Узнать время"):
                bot.send_message(message.chat.id, menu["current_city"].get_time())
            if (message.text == "Выбрать другой город"):
                bot.send_message(message.chat.id, "Введите название другого города", reply_markup=create_markup(menu["city_choise_menu"].keys()))
                menu["current_city"] = None


    except Exception:
        print(time.ctime(), "User id:", message.from_user.id)
        print(time.ctime(), "Message:", message.text.title(), 'Error')
        bot.send_message(message.chat.id, "Не найден город, попробуйте ввести название снова.\n")


if __name__ == __name__:
    bot.polling(none_stop=True)

