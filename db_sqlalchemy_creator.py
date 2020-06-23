from sqlalchemy import Column, Integer, String, Float, Date, Text, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
# from sqlalchemy.orm import relationship
from datetime import datetime
# Чтобы соединиться с СУБД, используется функция create_engine():
engine = create_engine('sqlite:///orm1.sqlite', echo=False)
# Декларативное создание таблицы, класса и отображения за один раз
Base = declarative_base()
class Vacancy_info(Base):
    __tablename__ = 'vacancy_info'
    id = Column(Integer, primary_key=True)
    city = Column(Integer, ForeignKey('city.id'))
    vacancy = Column(Integer, ForeignKey('vacancy.id'))
    av_salary = Column(Float)
    skills_list = Column(String)
    def __init__(self, city, vacancy, av_salary, skills_list):
        self.city = city
        self.vacancy = vacancy
        self.av_salary = av_salary
        self.skills_list = skills_list
    def __str__(self):
        return f'{self.city}, {self.vacancy}, {self.av_salary}, {self.skills_list}'
class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    city = Column(String, unique=True)
    def __init__(self, city):
        self.city = city
    def __str__(self):
        return f'{self.city}'
class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy = Column(String, unique=True)
    def __init__(self, vacancy):
        self.vacancy = vacancy
    def __str__(self):
        return f'{self.vacancy}'
def _get_date():
    return datetime.today()
class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    post_mail = Column(String)
    message = Column(String)
    date = Column(Date)
    def __init__(self, email, name, post_mail, message, date):
        self.email = email
        self.name = name
        self.post_mail = post_mail
        self.message = message
        self.date = date
    def __str__(self):
       return f'{self.email}, {self.name}, {self.post_mail}, {self.message}, {self.date}'
if __name__ == '__main__':
    # Создание таблицы
    Base.metadata.create_all(engine)
    # Создание сессии. Теперь мы готовы начать общение с базой данных.
    Session = sessionmaker(bind=engine)
    session = Session()

    # Пробное наполнение базы -----------------------------------------------------------------
    # city = [['Москва'], ['Самара']]
    # vacancy = [['Python'], ['SQL']]
    #
    # vacancy_info = [['Москва', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux'],
    #                 ['Самара', 'SQL', 67437.5, 'sql, t, процедура, ms, интересоваться, функция, триггер, server, хранить, oracle'],
    #                 ['Москва', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux'],
    #                 ['Орел', 'Python', 151363.23, 'python, django, api, веб, flask, web, postgresql, rest, sql, linux'],
    #                 ['Самара', 'SQL', 67437.5, 'sql, t, процедура, ms, интересоваться, функция, триггер, server, хранить, oracle']
    #                 ]
    #
    # contacts = [['q1@mail.ru', 'Борис', 'Москва, ул.Тверская, д.7, кв.1', 'Хочу в отпуск!', '2020.04.10'],
    #             ['q2@mail.ru', 'Ольга', 'Самара, ул.Ленина, д.3, кв.56', 'Хочу на работу!', '2020.04.11']]

    # session.add_all([City(x[0]) for x in city])
    # session.add_all([Vacancy(x[0]) for x in vacancy])
    # session.commit()

    # session.add_all([Vacancy_info(session.query(City).filter(City.city == x[0]).first().id,
    #                               session.query(Vacancy).filter(Vacancy.vacancy == x[1]).first().id,
    #                               x[2], x[3]) for x in vacancy_info])
    # session.commit()

    # session.add_all([Contacts(x[0], x[1], x[2], x[3], x[4]) for x in contacts])
    # session.commit()

    # JOIN ---------------------
    # Объединение 2-х таблиц Vacancy_info и City по столбцу Vacancy_info.city == City.id
    # query = session.query(Vacancy_info, City)
    # query = query.join(Vacancy_info, Vacancy_info.city == City.id)
    # records = query.all()
    # for obj1, obj2 in records:
    #     print(obj1,obj2)

    # FILTER ---------------------
    # Первый найденный по фильтру
    # city_query1 = session.query(Vacancy_info).filter_by(city=1).first()
    # print(city_query1)

    # Все найденные по фильтру
    # city_query = session.query(Vacancy_info).filter(Vacancy_info.city.in_([1])).all()
    # for city in city_query:
    #     print(city.city, city.skills_list)
    # -------------------------------------------------------------------------------
    # Все найденные без фильтров
    # for u in session.query(Vacancy_info).order_by(Vacancy_info.id):
    #     print('print5: ', u)
