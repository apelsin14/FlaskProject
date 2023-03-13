import datetime
from flask import Flask
from random import choice


app = Flask(__name__)


@app.route('/hello_world')
def index():
    return "Привет, мир!"


@app.route('/cars')
def cars():
    cars = ['Chevrolet', 'Renault', 'Ford', 'Lada']
    return cars


@app.route('/cats')
def cats():
    cats = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
    return choice(cats)


@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.datetime.now()
    time_now = f'Текущее время: {current_time}'
    return time_now


@app.route('/get_time/future')
def get_time_future():
    current_time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    time_future = f'Точное время через час будет {current_time_after_hour}'
    return time_future


@app.route('/counter')
def counter():
    counter.visits += 1
    return str(counter.visits)


counter.visits = 0


if __name__ == "__main__":
    app.run(debug=True)
