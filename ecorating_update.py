import pandas as pd
import requests
import json
from datetime import datetime
import operator

def count_ecorating(eco, w):
  ratings = {}

  for district in eco.index:
    i = 0
    rating = 0
    for param in eco.loc[district]:
      if i in [8, 10, 12]:
        rating -= param*w.iloc[i][0]
      else:
        rating += param*w.iloc[i][0]
      i+=1
    ratings[district] = rating

    return sorted(ratings.items(), key=operator.itemgetter(1))


def update():

  today = datetime.today().strftime('%d.%m.%Y')

  eco = pd.read_csv("data/dataframes/Экорейтинг_параметры.csv", delimiter=";", index_col="Район")
  w = pd.read_csv("data/dataframes/Экорейтинг_веса.csv", delimiter=";", index_col="Критерий")

  #Почва

  url = "https://apidata.mos.ru/v1/datasets/2452/rows?api_key=df09ef61fe72ab486dd9f0a84c268c3c&$filter=Cells/Year%20eq%202023"

  headers = {
      'Host': 'ovga.mos.ru',
      'User-Agent': 'Magic User-Agent v999.26 Windows PRO 11',
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'X-Requested-With': 'XMLHttpRequest'
  }

  soil_json = requests.get(url, requests)

  soil = json.loads(soil_json)

  new_soil = {}
  if soil:
    for obj in soil:
      district = obj["Cells"]["District"]
      val = obj["Cells"]["EstimatedindexValue"]
      if "район" in district:
        district = district.split(" ")[1] if district.split(" ")[1] != "район" else district.split(" ")[0]
        new_soil[district] = val
      elif "Троицк" in district:
        district = "городской округ Троицк"
        new_soil[district] = val
      elif "Щербинка" in district:
        district = "городской округ Щербинка"
        new_soil[district] = val
      else:
        new_soil[district] = val


  #Шум

  url = "https://apidata.mos.ru/v1/datasets/2449/rows?api_key=df09ef61fe72ab486dd9f0a84c268c3c&$filter=Cells/Date%20eq%20" + today

  headers = {
      'Host': 'ovga.mos.ru',
      'User-Agent': 'Magic User-Agent v999.26 Windows PRO 11',
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'X-Requested-With': 'XMLHttpRequest'
  }

  noise_json = requests.get(url, requests)
  noise = json.loads(noise_json)
  new_noise = {}
  if noise:
    for obj in noise:
      district = obj["Cells"]["District"]
      val = obj["Cells"]["Results"]
      if "не выявлены, выявлены" in val:
        val = 1
      elif "не выявлены" in val:
        val = 0
      elif "выявлены" in val or "Выявлены" in val:
        val = 1
      else:
        val = 0
      if "район" in district:
        district = district.split(" ")[1] if district.split(" ")[1] != "район" else district.split(" ")[0]
        new_noise[district] = val
      elif "Троицк" in district:
        district = "городской округ Троицк"
        new_noise[district] = val
      elif "Щербинка" in district:
        district = "городской округ Щербинка"
        new_noise[district] = val
      else:
        new_noise[district] = val

  today = datetime.today().strftime('%m.%Y')

  #Воздух

  url = "https://apidata.mos.ru/v1/datasets/2453/rows?api_key=df09ef61fe72ab486dd9f0a84c268c3c&$filter=Cells/Period%20eq%20" + today

  headers = {
      'Host': 'ovga.mos.ru',
      'User-Agent': 'Magic User-Agent v999.26 Windows PRO 11',
      'Accept': '*/*',
      'Accept-Encoding': 'gzip, deflate, br',
      'Connection': 'keep-alive',
      'X-Requested-With': 'XMLHttpRequest'
  }

  air_json = requests.get(url, requests)
  air = json.loads(air_json)
  params = ["Диоксид азота",	"Диоксид серы",	"Оксид азота",	"Оксид углерода",	"Сероводород"]

  new_air = {}
  if air:
    for obj in air:
      district = obj["Cells"]["District"]
      param = obj["Cells"]["Parameter"]
      pdk = obj["Cells"]["MonthlyAveragePDKss"]
      if pdk and param in params:
        if "район" in district:
          district = district.split(" ")[1] if district.split(" ")[1] != "район" else district.split(" ")[0]
          if district in new_air.keys():
            new_air[district][param] = pdk
          else:
            new_air[district] = {}
            new_air[district][param] = pdk
        elif "Троицк" in district:
          district = "городской округ Троицк"
          if district in new_air.keys():
            new_air[district][param] = pdk
          else:
            new_air[district] = {}
            new_air[district][param] = pdk
        elif "Щербинка" in district:
          district = "городской округ Щербинка"
          if district in new_air.keys():
            new_air[district][param] = pdk
          else:
            new_air[district] = {}
            new_air[district][param] = pdk
        else:
          if district in new_air.keys():
            new_air[district][param] = pdk
          else:
            new_air[district] = {}
            new_air[district][param] = pdk

  for district in eco.index:
    if district in new_air.keys():
      for param in new_air[district].keys():
        eco.at[district, param] = new_air[district][param]
    if district in new_noise.keys():
      eco.at[district, "Шум"] = new_noise[district]
    if district in new_soil.keys():
      eco.at[district, "Загрязнение почвы"] = new_soil[district]

  updated_rating = count_ecorating(eco, w)
  pd.DataFrame(dict(updated_rating), index=["rating"]).transpose().to_pickle("data/dataframes/ecorating_df.pickle")
