from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Извлекаем ключ из файла конфигурации
config_file = "config.txt"
config = ConfigParser()
config.read_file(open(config_file))
api_key = config.get('weather', 'api')
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
weekly_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}'

saved_weather = []  # Список для сохранения данных о погоде и температуре

# Явная функция для получения информации о погоде
def get_weather(city):
    result = requests.get(url.format(city, api_key))

    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = round(temp_kelvin - 273.15)  # Переводим в градусы Цельсия и округляем
        weather1 = json['weather'][0]['main']
        final = [city, country, temp_kelvin, temp_celsius, weather1]
        return final
    else:
        print("Нет данных")

# Явная функция для получения информации о погоде на неделю
def get_weekly_weather(city):
    result = requests.get(weekly_url.format(city, api_key))

    if result:
        json = result.json()
        # Обработка и отображение информации о погоде на неделю
        # Реализуйте здесь логику извлечения и отображения нужной информации
        weather_data = json['list']
        weekly_weather = []
        for weather in weather_data:
            temperature = round(weather['main']['temp'] - 273.15)  # Переводим в градусы Цельсия и округляем
            weather_description = weather['weather'][0]['description']
            wind_speed = weather['wind']['speed']
            date = datetime.strptime(weather['dt_txt'], '%Y-%m-%d %H:%M:%S')
            formatted_date = date.strftime('%d.%m.%Y')  # Форматируем дату в день.месяц.год
            weekly_weather.append(f"Дата: {formatted_date}\nТемпература: {temperature} градусов Цельсия\nПогода: {weather_description}\nСкорость ветра: {wind_speed}")
        return weekly_weather
    else:
        print("Нет данных")

# Явная функция для построения графика погоды
def plot_weather(city):
    result = requests.get(weekly_url.format(city, api_key))

    if result:
        json = result.json()
        weather_data = json['list']
        dates = []
        temperatures = []
        for weather in weather_data:
            temperature = round(weather['main']['temp'] - 273.15)  # Переводим в градусы Цельсия и округляем
            date = datetime.strptime(weather['dt_txt'], '%Y-%m-%d %H:%M:%S')
            dates.append(date)
            temperatures.append(temperature)

        plt.figure(figsize=(8, 5))
        plt.plot(dates, temperatures, 'b.-')
        plt.xlabel('Дата')
        plt.ylabel('Температура (градусы Цельсия)')
        plt.title('Прогноз погоды на неделю')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()
    else:
        print("Нет данных")

# Явная функция для вывода графика погоды
def show_weather_plot():
    city = city_text.get()
    plot_weather(city)

# Явная функция для сохранения данных о погоде и температуре
def save_weather():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        saved_weather.append(weather)
        messagebox.showinfo('Сохранение', f'Информация о погоде в городе {city} сохранена!\nТемпература: {weather[3]} градусов Цельсия')
    else:
        messagebox.showerror('Ошибка', "Невозможно сохранить информацию о погоде для {}".format(city))

# Явная функция для сравнения сохраненных данных о погоде
def compare_weather():
    if len(saved_weather) < 2:
        messagebox.showerror('Ошибка', "Недостаточно сохраненных данных о погоде для сравнения!")
        return

    city = city_text.get()
    current_weather = get_weather(city)
    if current_weather:
        weather_info = f'Текущая погода в городе {city}:\nТемпература: {current_weather[3]} градусов Цельсия\nПогода: {current_weather[4]}\n\n'
    else:
        weather_info = f'Текущая погода в городе {city}: Нет данных\n\n'

    compare_info = 'Сравнение с сохраненными данными:\n\n'
    for weather in saved_weather:
        compare_info += f'Город: {weather[0]}\nТемпература: {weather[3]} градусов Цельсия\nПогода: {weather[4]}\n\n'

    messagebox.showinfo('Сравнение', weather_info + compare_info)

# Явная функция для поиска города
def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        update_weather_info(weather)
        update_weather_image(weather[4])  # Обновляем изображение в соответствии с погодой
        weekly_weather_btn.pack()  # Показываем кнопку для просмотра погоды на неделю
        weather_plot_btn.pack()  # Показываем кнопку для вывода графика погоды
    else:
        messagebox.showerror('Ошибка', "Невозможно найти информацию о погоде для {}".format(city))

def update_weather_info(weather):
    location_lbl['text'] = '{} ,{}'.format(weather[0], weather[1])
    temperature_label['text'] = str(weather[3]) + " градусов Цельсия"
    weather_l['text'] = weather[4]

def update_weather_image(weather_condition):
    image_path = ''
    if weather_condition == 'Clear':
        image_path = 'C:/Users/decop/PycharmProjects/000/Clear.jpg'
    elif weather_condition == 'Clouds':
        image_path = 'C:/Users/decop/PycharmProjects/000/Clouds.jpg'
    elif weather_condition == 'Rain':
        image_path = 'C:/Users/decop/PycharmProjects/000/Rain.jpg'
    elif weather_condition == 'Drizzle':
        image_path = 'C:/Users/decop/PycharmProjects/000/Drizzle.jpg'
    elif weather_condition == 'Thunderstorm':
        image_path = 'C:/Users/decop/PycharmProjects/000/Thunderstorm.jpg'
    elif weather_condition == 'Snow':
        image_path = 'C:/Users/decop/PycharmProjects/000/Snow.jpg'
    elif weather_condition == 'Mist':
        image_path = 'C:/Users/decop/PycharmProjects/000/Mist.jpg'
    elif weather_condition == 'Smoke':
        image_path = 'C:/Users/decop/PycharmProjects/000/Smoke.jpg'
    elif weather_condition == 'Haze':
        image_path = 'C:/Users/decop/PycharmProjects/000/Haze.jpg'
    elif weather_condition == 'Dust':
        image_path = 'C:/Users/decop/PycharmProjects/000/Dust.jpg'
    elif weather_condition == 'Fog':
        image_path = 'C:/Users/decop/PycharmProjects/000/Fog.jpg'
    elif weather_condition == 'Sand':
        image_path = 'C:/Users/decop/PycharmProjects/000/Sand.jpg'
    else:
        image_path = 'C:/Users/decop/PycharmProjects/000/Unknown.jpg'

    image = Image.open(image_path)
    image = image.resize((100, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    weather_image_label.configure(image=photo)
    weather_image_label.image = photo

def get_weekly_weather_info():
    city = city_text.get()
    weekly_weather = get_weekly_weather(city)
    if weekly_weather:
        weekly_weather_list.delete(0, END)  # Очищаем список
        for weather in weekly_weather:
            weekly_weather_list.insert(END, weather)
        weekly_weather_list.pack()  # Показываем список погоды на неделю
    else:
        messagebox.showerror('Ошибка', "Невозможно получить погоду на неделю для {}".format(city))

def change_font():
    selected_font = font_option.get()
    selected_font_size = font_size_scale.get()
    font_style = (selected_font, selected_font_size)
    location_lbl.config(font=font_style)
    temperature_label.config(font=font_style)
    weather_l.config(font=font_style)
    weekly_weather_btn.config(font=font_style)
    weekly_weather_list.config(font=font_style)
    weather_plot_btn.config(font=font_style)
    search_btn.config(font=font_style)
    save_btn.config(font=font_style)
    compare_btn.config(font=font_style)
    font_label.config(font=font_style)
    font_menu.config(font=font_style)
    font_size_scale.config(font=font_style)
    font_apply_btn.config(font=font_style)

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def change_colors():
    bg_color = bg_color_entry.get()
    fg_color = fg_color_entry.get()
    app.config(bg=bg_color, fg=fg_color)

# Создаем объект приложения
app = Tk()
# Устанавливаем заголовок
app.title("Погодное приложение")
# Задаем размер окна
app.geometry("600x500")

# Создаем элементы интерфейса
main_frame = Frame(app)
main_frame.pack(fill=BOTH, expand=1)

# Добавляем возможность скроллинга
canvas = Canvas(main_frame)
canvas.pack(side=LEFT, fill=BOTH, expand=1)

scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", on_mousewheel)

content_frame = Frame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor="nw")

city_text = Entry(content_frame, font=("Arial", 14), width=20)
city_text.pack(pady=20)

search_btn = Button(content_frame, text="Поиск", font=("Arial", 14), command=search)
search_btn.pack()

location_lbl = Label(content_frame, text="", font=("Arial", 20))
location_lbl.pack(pady=20)

temperature_label = Label(content_frame, text="", font=("Arial", 20))
temperature_label.pack(pady=20)

weather_l = Label(content_frame, text="", font=("Arial", 20))
weather_l.pack(pady=20)

weather_image_label = Label(content_frame)
weather_image_label.pack(pady=10)

weekly_weather_btn = Button(content_frame, text="Погода на неделю", font=("Arial", 14), command=get_weekly_weather_info)
weekly_weather_btn.pack()

weekly_weather_list = Listbox(content_frame, width=80, height=10, font=("Arial", 12))
weekly_weather_list.pack(pady=20)

weather_plot_btn = Button(content_frame, text="График погоды", font=("Arial", 14), command=show_weather_plot)
weather_plot_btn.pack()

save_btn = Button(content_frame, text="Сохранить", font=("Arial", 14), command=save_weather)
save_btn.pack(side=LEFT, padx=10)

compare_btn = Button(content_frame, text="Сравнить", font=("Arial", 14), command=compare_weather)
compare_btn.pack(side=LEFT, padx=10)

font_label = Label(content_frame, text="Выберите шрифт и размер", font=("Arial", 14))
font_label.pack(pady=10)

font_option = StringVar()
font_option.set("Arial")  # Значение по умолчанию
font_menu = OptionMenu(content_frame, font_option, "Arial", "Times New Roman", "Verdana", "Courier New")
font_menu.pack()

font_size_scale = Scale(content_frame, from_=10, to=30, orient=HORIZONTAL, resolution=1)
font_size_scale.set(14)  # Значение по умолчанию
font_size_scale.pack(pady=10)

font_apply_btn = Button(content_frame, text="Применить шрифт", font=("Arial", 14), command=change_font)
font_apply_btn.pack()

bg_color_label = Label(content_frame, text="Цвет фона:", font=("Arial", 12))
bg_color_label.pack(pady=10)

bg_color_entry = Entry(content_frame, font=("Arial", 12), width=10)
bg_color_entry.pack()

fg_color_label = Label(content_frame, text="Цвет текста:", font=("Arial", 12))
fg_color_label.pack(pady=10)

fg_color_entry = Entry(content_frame, font=("Arial", 12), width=10)
fg_color_entry.pack()

change_colors_btn = Button(content_frame, text="Изменить цвета", font=("Arial", 12), command=change_colors, relief=FLAT, bd=0, bg="#337ab7", fg="white")
change_colors_btn.pack(pady=10)

content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Запускаем главный цикл приложения
app.mainloop()
