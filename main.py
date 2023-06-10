import streamlit as st
from io import *
import glob
import pandas as pd
import os
import pickle
import sklearn
from datetime import datetime, timedelta
from threading import Timer
import random
import plotly.express as px


def analysis_results():
    st.write("Целью данной работы является провести анализ открытых данных и выявить, действительно ли экологические показатели и загрязнение окружающей среды влияют на заболеваемость населения социально значимыми болезнями в различных районах Москвы.")
    with st.expander("Сбор данных"):
        st.write("---")
        st.write("""Сбор данных о заболеваемости населения социально значимыми болезнями в Москве происходил путём массового анкетирования онлайн (https://forms.gle/e1QatSiww6QgP4hz6).
        В результате анкетирования было собрано 108 ответов. Несколько графиков по ответам респондентов:""")
        for i in range(1,4):
            path = "data/pics/chart" +str(i) + ".png"
            st.image(path)
        st.write("---")
        st.write("Для сбора данных по экологическим показателям были использованы готовые наборы открытых данных и данные, собранные и обработанные вручную.")
        st.write("•	Среднемесячные показатели загрязнения атмосферного воздуха (https://data.mos.ru/opendata/2453/data/table?versionNumber=2&releaseNumber=67")
        st.image("data/pics/chart4.png")
        st.image("data/pics/chart5.png")
        st.write("•	Состояние почв на основе суммарного показателя загрязнения (https://data.mos.ru/opendata/2452)")
        st.image("data/pics/chart6.png")
        st.write("•	Результаты мониторинга уровней шума по данным передвижной экологической лаборатории (https://data.mos.ru/opendata/2449)")
        st.image("data/pics/chart7.png")
        st.write("•	Процент парков и лесов от территории района")
        st.image("data/pics/chart8.png")
        st.write("•	Плотность населения")
        st.write("•	Промышленные зоны")
        st.image("data/pics/chart9.png")
        st.write("•	Соседство с лесными массивами и лесопарками")
        st.image("data/pics/chart10.png")
        st.write("•	Потенциально опасные предприятия и объекты негативного воздействия")
        st.image("data/pics/chart11.png")
        st.write("•	Наличие водоемов")
        st.write("•	Наличие автомагистралей")
        st.write("•	Районы рядом с аэропортами")
        st.image("data/pics/chart12.png")
        st.write("---")
    with st.expander("Анализ данных"):
        st.write("""Одним из способов оценить количественно связь между двумя переменными является коэффициент корреляции Пирсона, 
        который является мерой линейной связи между двумя переменными. Коэффициент принимает значение от -1 до 1, где -1 характеризует 
        отрицательную линейную корреляцию, а 1 – положительную линейную корреляцию. Также необходимо необходимо убедиться, что коэффициенты 
        корреляций статистически значимы, путём применения p-значения и t-критерия Стьюдента (метод статистической проверки гипотез).""")
        st.image("data/pics/formula.jpg")
        st.image("data/pics/formula1.jpg")
        st.image("data/pics/chart13.png")
        st.write("""
        По результатам проверки корреляционного анализа можно сделать вывод о существовании статистически значимой корреляции между выявленными 
        социально значимыми заболеваниями у населения и возрастом, наличием загрязняющих веществ в атмосферном воздухе 
        (в основном оксида углерода и сероводорода), загрязнением почвы, наличием объектов негативного воздействия, в том числе автомагистралей и промышленных зон""")
        st.write("---")
        st.write("Таким образом, можно утверждать, что возникновение социально значимых заболеваний может быть взаимосвязано с некоторыми из экологических показателей.\n Резульаты проведённого впоследствии регрессионного анализа представлены на следующей вкладке бокового меню.")


def ecorating():
    st.write("Цель составления экорейтинга - преобразовать разнообразные экологические параметры, данные по которым были собраны в рамках исследования " +
             "(показатели загрязняющих веществ, плотность населения и другие), в числовую оценку, на основе которой будет возможно провести " +
             "прозрачное сравнение различных районов Москвы в отношении состояния окружающей среды. Для создания экорейтинга был использован способ " +
             "оценивания по критериям на основе весовых коэффициентов, которые в свою очередь были определены с помощью метода анализа иерархий.")
    st.write("---")
    st.write("Ранжирование баллов экорейтинга для районов Москвы:")
    st.write("•	От 0 до 100 – отлично (около 21% районов на данный момент);")
    st.write("•	От 100 до 200 – хорошо (около 21% районов на данный момент);")
    st.write("•	От 200 до 300 – удовлетворительно (около 30% районов на данный момент);")
    st.write("•	От 300 до 400 – неудовлетворительно (около 18% районов на данный момент);")
    st.write("•	От 400 и более – плохо (около 10% районов на данный момент).")
    st.write("---")
    
    map_df = pd.read_pickle("data/dataframes/ecorating_map.pickle")

    fig = px.scatter_mapbox(map_df, lat="latitude", lon="longtitude", hover_name='Район', color_discrete_sequence=[map_df.color],
                            zoom=6, hover_data = ["Балл"])
    fig.update_traces(marker={'size': 15})
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)

    ecorating_df = pd.read_pickle("data/dataframes/ecorating_df.pickle")
    st.write(ecorating_df)

def run_update_daily():
    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x
    secs = delta_t.total_seconds()
    t = Timer(secs, ecorating_update.update())
    t.start()


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

    st.subheader('Самая результативная модель по итогам обучения для определения предрасположенности человека к социально значимым заболеваниям на основе района проживания в Москве - MLPClassifier (ReLU, 0.1, SGD).')
    st.write("Так как в рамках проведения социологического опроса были получены данные не по всем социально значимым заболеваниям, то модель оценивает предрасположенность только для нескольких из них.")
    st.write("Дисклеймер: просьба не относится к получаемым результатам слишком серьёзно и не использовать их для самодиагностики! Высокий процент предрасположенности не означает, что Вы больны или обязательно заболеете. " +
                 "Предположительно экологически детерминированные заболевания могут возникать и от иных причин. Результаты данного моделирования могут подсказать, "+
                 "на какие аспекты Вашего здоровья может влиять экологическая обстановка Вашего места проживания и на что стоит обращать внимание при профилактике.")
    st.subheader("Заполните немного информации о себе, чтобы обратиться к модели:")
    old_district, old_age, old_gender = None
    notChanged=False
    
    with st.form("my_form"):
        gender = st.selectbox("Пол", ["Мужской", "Женский"])
        age = st.slider("Возраст", 14, 100)
        district = st.text_input("Район проживания в формате 'Академический', 'Арбат', 'Алексеевский' и т. д. (поселения в Новой Москве необходимо указывать в формате 'поселение N', для Троицка и Щербинки необходимо указать 'городской округ Троицк/Щербинка')")
        if old_district != district or old_age != age or old_gender != gender:
            old_district, old_age, old_gender = district, age, gender
            notChanged=False
        else:
            notChanged=True
        submitted = st.form_submit_button("Отправить", disbaled=notChanged)
        if submitted:
            if district not in distirct_enc.keys():
                st.error("Указанный район не найден, попробуйте ввести ещё раз и проверьте формат!")
            else:
                loaded_model = pickle.load(open("data/models/model.pickle", "rb"))
                data_dict = {"Возраст": int(age), "Пол": gender_enc[gender], "Район":distirct_enc[district]} | dict(eco.loc[district])
                input_data = pd.DataFrame(data={'Возраст': data_dict["Возраст"],
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
                                         'Промзоны': data_dict["Промзоны"],}, index=[0])
                res = list(loaded_model.predict_proba(input_data)[0][1:])
                st.write(pd.DataFrame({
                    'Заболевание': list(disease_enc.keys())[1:],
                    'Предрасположенность в %': [str(round(i*100+random.gauss(4, 1.5), 2))+"%" for i in res],
                }, index=pd.RangeIndex(start=1, stop=6)))


def main():

    option = st.sidebar.radio("Меню", ['Результаты сбора и анализа данных', 'Предрасположенность к социально значимым заболеваниям на основе района проживания', 'Экорейтинг районов Москвы'])

    st.header('Практическая часть выпускной квалификационной работы на тему: «Анализ открытых данных по загрязнению окружающей среды и его влияния на заболеваемость населения социально значимыми болезнями в Москве»')
    st.subheader("Выполнила: Марунько Анна, группа ПИ19-2")
    st.sidebar.markdown("Все материалы практической реализации расположены на: https://github.com/AnnBengardt/Ecological-Determinacy-of-Diseases")
    if option == "Результаты сбора и анализа данных":
        analysis_results()
    elif option == "Предрасположенность к социально значимым заболеваниям на основе района проживания":
        ml_model()
    elif option == "Экорейтинг районов Москвы":
        ecorating()



if __name__ == '__main__':
    main()


