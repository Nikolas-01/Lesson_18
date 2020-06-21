from flask import Flask, render_template, request
from api_hh_skills import parsing_skills
from api_hh_salary import parsing_av_salary
from db_sqlalchemy_creator import Vacancy_info, City, Vacancy, Contacts
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from datetime import datetime
app = Flask(__name__)
engine = create_engine('sqlite:///orm1.sqlite', echo=False)
Base = declarative_base()
@app.route('/')
def main_index():
    return render_template('index.html')
@app.route('/request_sgk')
def request_sgk():
     return render_template('request_sgk.html')
@app.route('/request_api')
def request_api():
    return render_template('request_api.html')
@app.route('/parsing_answer', methods = ['POST'])
def parsing_answer():
     city = request.form['city']
     vacancy = request.form['vacancy']
     # Получение информации по средней зарплате путем парсинга сайта
     av_salary = round(parsing_av_salary(city, vacancy), 2)
     if av_salary == 0:
         av_salary = 'Нет информации'
     # Получение информации об основных навыках путем парсинга сайта
     skills_list = parsing_skills(city, vacancy)
     len_skills = len(skills_list)
     if len_skills == 0:
         skills_info = 'Нет информации'
     else:
         skills_info = ''
         for i in range(len_skills-1):
            skills_info = skills_info + skills_list[i] + ', '
         skills_info = skills_info + skills_list[len_skills-1]
    # Наполнение шаблона для передачи информации на сайт
     data = {
             'city': city,
             'vacancy': vacancy,
             'av_salary': av_salary,
             'skills_info': skills_info}
     # Загрузка полученной информации в базу SQLAlchemy
     try:
         session.add(City(city))
         session.commit()
     except exc.IntegrityError:
         session.rollback()

     try:
         session.add(Vacancy(vacancy))
         session.commit()
     except exc.IntegrityError:
         session.rollback()
     try:
         session.add(Vacancy_info(session.query(City).filter(City.city == city).first().id,
                                  session.query(Vacancy).filter(Vacancy.vacancy == vacancy).first().id,
                                  av_salary, skills_info))
         session.commit()
     except exc.IntegrityError:
         session.rollback()
     return render_template('parsing_answer.html', data=data)
@app.route('/contacts')
def contacts():
     return render_template('contacts.html')
@app.route('/contacts_ok', methods = ['POST'])
def contacts_ok():
     email = request.form['email']
     name = request.form['name']
     post_mail = request.form['post_mail']
     message = request.form['message'].strip()
     # Загрузка полученной информации в базу SQLAlchemy + сегодняшняя дата
     try:
         session.add(Contacts(email, name, post_mail, message, datetime.today()))
         session.commit()
     except exc.IntegrityError:
         session.rollback()
     return render_template('contacts_ok.html', message=message)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # app.run()  # в режиме отладки на одном компьютере
    # хорош для начала разработки на локальном сервере. Но это потребует ручного перезапуска сервера после каждого изменения в коде.
    # app.run(host='0.0.0.0') # сделать сервер общедоступным в локальной сети
    app.run(debug=True) # сервер будет сам перегружаться после каждого изменения в коде