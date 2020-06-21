# средняя з.п.
import requests
def parsing_av_salary(city, vacancy):
    url_currency = 'https://www.cbr-xml-daily.ru/daily_json.js'
    response_currency = requests.get(url_currency)
    result_json_currency = response_currency.json()
    koef_USD = result_json_currency['Valute']['USD']['Value']
    koef_EUR = result_json_currency['Valute']['EUR']['Value']
    # print(f"Курс валюты н: {result_json_currency['Date']}")
    # print(f"USD = {koef_USD}")
    # print(f"Евро = {koef_EUR}")
    data_whole = []
    wage = 0
    sum_n = 0
    url = 'https://api.hh.ru/vacancies'
    for page in range(10): # 100 страниц вакансий
        params = {'text': 'NAME:' + vacancy + ' AND ' + city, 'per_page':'10', 'page':page}
        # params = {'text': vacancy, 'area':'1','per_page':'10', 'page':page}
        result = requests.get(url, params=params)
        result_json = result.json()
        data_whole.append(result_json)
        # print(result_json)
    for item in data_whole: # Перебираем вакансии
        # print('for item')
        data = item['items']
        n = 0 # количество рассмотренных вакансий с указанными зарплатами
        sum_zp = 0 # Сумматор зарплат
        for record in data: # Перебираем
            if record['salary'] != None: # Есть ли инфа по зп в вакансии
                salary = record['salary']
                if salary['from'] != None: # инфа по минимальной зарпоате в вакансии
                    n += 1
                    # курс валюты на сегодняшнюю дату
                    if salary['currency'] == 'USD':
                        koef = koef_USD
                    elif salary['currency'] == 'EUR':
                        koef = koef_EUR
                    else: koef = 1
                    # зарплата или диапазон зарплат
                    if salary['to'] != None:  # инфа по максимальной зарплате в вакансии
                        sum_zp += koef*(salary['from'] + salary['to'])/2
                    else:
                        sum_zp += koef*salary['from']
        wage += sum_zp
        sum_n += n
    if sum_n == 0:
        av_salary = 0
    else:
        av_salary = wage/sum_n
    # print(f"Средняя зарплата по {city} по ключевому слову {vacancy} составляет {round(av_salary,2)} рублей.")
    return av_salary
# print(round(parsing_av_salary('Москва', 'Python'),0))
# print(round(parsing_av_salary('Ижевск', 'Python'),2))