import streamlit as st
from io import *
import glob
import pandas as pd
import os
import pickle
import sklearn


def analysis_results():
    pass

def ecorating():
    pass

def ml_model():

    disease_enc = {'0': 0,
                     'Болезни, характеризующиеся повышенным кровяным давлением': 1,
                     'Злокачественные новообразования': 2,
                     'Психические расстройства и расстройства поведения': 3,
                     'Сахарный диабет': 4,
                     'Туберкулёз': 5}
    gender_enc = {"Мужской": 1, "Женский": 0}
    distirct_enc = {'Академический': 0,
                     'Алескеевский': 1,
                     'Алтуфьевский': 2,
                     'Арбат': 3,
                     'Аэропорт': 4,
                     'Бабушкинский': 5,
                     'Басманный': 6,
                     'Беговой': 7,
                     'Бескудниковский': 8,
                     'Бибирево': 9,
                     'Бирюлёво Восточное': 10,
                     'Бирюлёво Западное': 11,
                     'Богородское': 12,
                     'Братеево': 13,
                     'Бутырский': 14,
                     'Вешняки': 15,
                     'Внуково': 16,
                     'Войковский': 17,
                     'Восточное Дегунино': 18,
                     'Восточное Измайлово': 19,
                     'Восточный': 20,
                     'Выхино-Жулебино': 21,
                     'Гагаринский': 22,
                     'Головинский': 23,
                     'Гольяново': 24,
                     'Даниловский': 25,
                     'Дмитровский': 26,
                     'Донской': 27,
                     'Дорогомилово': 28,
                     'Замоскворечье': 29,
                     'Западное Дегунино': 30,
                     'Зюзино': 31,
                     'Зябликово': 32,
                     'Ивановское': 33,
                     'Измайлово': 34,
                     'Капотня': 35,
                     'Коньково': 36,
                     'Коптево': 37,
                     'Косино-Ухтомский': 38,
                     'Котловка': 39,
                     'Красносельский': 40,
                     'Крылатское': 41,
                     'Крюково': 42,
                     'Кузьминки': 43,
                     'Кунцево': 44,
                     'Куркино': 45,
                     'Левобережный': 46,
                     'Лефортово': 47,
                     'Лианозово': 48,
                     'Ломоносовский': 49,
                     'Лосиноостровский': 50,
                     'Люблино': 51,
                     'Марфино': 52,
                     'Марьина роща': 53,
                     'Марьино': 54,
                     'Матушкино': 55,
                     'Метрогородок': 56,
                     'Мещанский': 57,
                     'Митино': 58,
                     'Можайский': 59,
                     'Молжаниновский': 60,
                     'Москворечье-Сабурово': 61,
                     'Нагатино-Садовники': 62,
                     'Нагатинский Затон': 63,
                     'Нагорный': 64,
                     'Некрасовка': 65,
                     'Нижегородский': 66,
                     'Ново-Переделкино': 67,
                     'Новогиреево': 68,
                     'Новокосино': 69,
                     'Обручевский': 70,
                     'Орехово-Борисово Северное': 71,
                     'Орехово-Борисово Южное': 72,
                     'Останкинский': 73,
                     'Отрадное': 74,
                     'Очаково-Матвеевское': 75,
                     'Перово': 76,
                     'Печатники': 77,
                     'Покровское-Стрешнево': 78,
                     'Преображенское': 79,
                     'Пресненский': 80,
                     'Проспект Вернадского': 81,
                     'Раменки': 82,
                     'Ростокино': 83,
                     'Рязанский': 84,
                     'Савёлки': 85,
                     'Савёловский': 86,
                     'Свиблово': 87,
                     'Северное Бутово': 88,
                     'Северное Измайлово': 89,
                     'Северное Медведково': 90,
                     'Северное Тушино': 91,
                     'Северный': 92,
                     'Силино': 93,
                     'Сокол': 94,
                     'Соколиная Гора': 95,
                     'Сокольники': 96,
                     'Солнцево': 97,
                     'Старое Крюково': 98,
                     'Строгино': 99,
                     'Таганский': 100,
                     'Тверской': 101,
                     'Текстильщики': 102,
                     'Тимирязевский': 103,
                     'Тропарёво-Никулино': 104,
                     'Тёплый Стан': 105,
                     'Фили-Давыдково': 106,
                     'Филёвский Парк': 107,
                     'Хамовники': 108,
                     'Ховрино': 109,
                     'Хорошёво-Мнёвники': 110,
                     'Хорошёвский': 111,
                     'Царицыно': 112,
                     'Чертаново Северное': 113,
                     'Чертаново Центральное': 114,
                     'Чертаново Южное': 115,
                     'Черёмушки': 116,
                     'Щукино': 117,
                     'Южное Бутово': 118,
                     'Южное Медведково': 119,
                     'Южное Тушино': 120,
                     'Южнопортовый': 121,
                     'Якиманка': 122,
                     'Ярославский': 123,
                     'Ясенево': 124,
                     'городской округ Троицк': 125,
                     'городской округ Щербинка': 126,
                     'поселение "Мосрентген"': 127,
                     'поселение Внуковское': 128,
                     'поселение Вороновское': 129,
                     'поселение Воскресенское': 130,
                     'поселение Десёновское': 131,
                     'поселение Киевский': 132,
                     'поселение Клёновское': 133,
                     'поселение Кокошкино': 134,
                     'поселение Краснопахорское': 135,
                     'поселение Марушкинское': 136,
                     'поселение Михайлово-Ярцевское': 137,
                     'поселение Московский': 138,
                     'поселение Новофедоровское': 139,
                     'поселение Первомайское': 140,
                     'поселение Роговское': 141,
                     'поселение Рязановское': 142,
                     'поселение Сосенское': 143,
                     'поселение Филимонковское': 144,
                     'поселение Щаповское': 145}
    eco = pd.read_csv("data/dataframes/Eco_for_web.csv", delimiter=";", index_col = "Район")

    st.subheader('Самая результативная модель по итогам обучения для определения предрасположенности человека к социально значимым заболеваниям на основе района проживания в Москве - MLPClassifier (ReLU, 0.1, SGD)')
    st.write("Так как в рамках проведения социологического опроса были получены данные не по всем социально значимым заболеваниям, то модель оценивает предрасположенность только для нескольких из них")
    st.write("Дисклеймер: просьба не относится к получаемым результатам слишком серьёзно и не использовать их для самодиагностики! Высокий процент предрасположенности не означает, что Вы больны или обязательно заболеете. " +
                 "Предположительно экологически детерминированные заболевания могут возникать и от иных причин. Результаты данного моделирования могут подсказать, "+
                 "на какие аспекты Вашего здоровья может влиять экологическая обстановка Вашего места проживания и на что стоит обращать внимание при профилактике.")
    st.subheader("Заполните немного информации о себе, чтобы обратиться к модели:")
    with st.form("my_form"):
        gender = st.selectbox("Пол", ["Мужской", "Женский"])
        age = st.slider("Возраст", 14, 100)
        district = st.text_input("Район проживания в формате 'Академический', 'Арбат', 'Алексеевский' и т. д. (поселения в Новой Москве необходимо указывать в формате 'поселение N', для Троицка и Щербинки необходимо указать 'городской округ Троицк/Щербинка')")

        submitted = st.form_submit_button("Отправить")
        if submitted:
            if district not in distirct_enc.keys():
                st.error("Указанный район не найден, попробуйте ввести ещё раз и проверьте формат!")
            else:
                loaded_model = pickle.load(open("data/models/model.pickle", "rb"))
                data_dict = {"Возраст": int(age), "Пол": gender_enc[gender], "Район":distirct_enc[district]} | dict(eco.loc[district])
                input_data = pd.DataFrame(data={{'Возраст': data_dict["Возраст"],
                                         'Диоксид азота': data_dict["Диоксид азота"],
                                         'Диоксид серы': data_dict["Диоксид серы"],
                                         'Оксид азота': data_dict["Оксид азота"],
                                         'Оксид углерода': data_dict["Оксид углерода"],
                                         'Сероводород': data_dict["Сероводород"],
                                         'Плотность населения': data_dict["Плотность населения"],
                                         'Почва': data_dict["Почва"],
                                         'Озеленение': data_dict["Озеленение"],
                                         'Пол': data_dict["Пол"],
                                         'Район': data_dict["Район"],
                                         'Объекты негативного воздействия': data_dict["Объекты негативного воздействия"],
                                         'Водоемы': data_dict["Водоемы"],
                                         'Автомагистрали': data_dict["Автомагистрали"],
                                         'Шум': data_dict["Шум"],
                                         'Соседство с лесными массивами': data_dict["Соседство с лесными массивами"],
                                         'Аэропорт': data_dict["Аэропорт"],
                                         'Промзоны': data_dict["Промзоны"],}}, index=[0])
                res = list(loaded_model.predict_proba(input_data)[0][1:])
                st.write(pd.DataFrame({
                    'Заболевание': list(disease_enc.keys())[1:],
                    'Предрасположенность в %': [str(round(i*100, 2))+"%" for i in res],
                }))


def main():

    option = st.sidebar.radio("Меню", ['Результаты корреляционно-регрессионного анализа', 'Предрасположенность к социально значимым заболеваниям на основе района проживания', 'Экорейтинг районов Москвы'])

    st.header('Практическая часть выпускной квалификационной работы на тему: «Анализ открытых данных по загрязнению окружающей среды и его влияния на заболеваемость населения социально значимыми болезнями в Москве»')
    st.subheader("Выполнила: Марунько Анна, группа ПИ19-2")
    st.sidebar.markdown("Все материалы практической реализации расположены на: ")
    if option == "Результаты корреляционно-регрессионного анализа":
        analysis_results()
    elif option == "Предрасположенность к социально значимым заболеваниям на основе района проживания":
        ml_model()
    elif option == "Экорейтинг районов Москвы":
        ecorating()


if __name__ == '__main__':
    main()


