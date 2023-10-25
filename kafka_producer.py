import time
import json
from kafka import KafkaProducer  #kafka-python package
import requests

kafka_bootstrap_servers='localhost:9092' #adress de broker kafka
kafka_topic_name='weather_topic'  # adress de topic kafka


Producer =KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,value_serializer=lambda x: json.dumps(x).encode('utf-8'))

json_message=None
city_name=None
temperature=None
humidity=None
openweathermap_api_endpoint=None
appid=None

def get_weather_deatail(openweathermap_api_endpoint):
    api_resonse=requests.get(openweathermap_api_endpoint)
    json_data=api_resonse.json()
    city_name=json_data["name"]
    humidity=json_data["main"]["humidity"]
    temperature=json_data["main"]["temp"]
    json_message={"CityName":city_name,"Temperature":temperature,"Humidity":humidity,
                  "CreationTime":time.strftime("%Y-%m-%d %H:%M:%S")}

    return json_message


while True:
    city_name="Rabat"
    appid="e83b3c4c08285bf87b99f9bbc0abe3f0"
    openweathermap_api_endpoint="https://api.openweathermap.org/data/2.5/weather?appid="+appid+"&q="+city_name
    json_message=get_weather_deatail(openweathermap_api_endpoint)
    Producer.send(kafka_topic_name,json_message)
    print("Published messgae 1 : "+json.dumps(json_message))
    print("wait for 2 seconds ...")
    time.sleep(2)

    city_name="Sale"
    appid="30b09794b537d72cf33c860786698bb2"
    openweathermap_api_endpoint="https://api.openweathermap.org/data/2.5/weather?appid="+appid+"&q="+city_name
    json_message=get_weather_deatail(openweathermap_api_endpoint)
    Producer.send(kafka_topic_name,json_message)
    print("Published messgae 1 : "+json.dumps(json_message))
    print("wait for 2 seconds ...")
    time.sleep(2)

    city_name = "Casablanca"
    appid = "30b09794b537d72cf33c860786698bb2"
    openweathermap_api_endpoint = "https://api.openweathermap.org/data/2.5/weather?appid=" + appid + "&q=" + city_name
    json_message = get_weather_deatail(openweathermap_api_endpoint)
    Producer.send(kafka_topic_name, json_message)
    print("Published messgae 1 : " + json.dumps(json_message))
    print("wait for 2 seconds ...")
    time.sleep(2)

    city_name = "Marrakesh"
    appid = "30b09794b537d72cf33c860786698bb2"
    openweathermap_api_endpoint = "https://api.openweathermap.org/data/2.5/weather?appid=" + appid + "&q=" + city_name
    json_message = get_weather_deatail(openweathermap_api_endpoint)
    Producer.send(kafka_topic_name, json_message)
    print("Published messgae 1 : " + json.dumps(json_message))
    print("wait for 2 seconds ...")
    time.sleep(2)

    city_name = "Beni Mellal"
    appid = "30b09794b537d72cf33c860786698bb2"
    openweathermap_api_endpoint = "https://api.openweathermap.org/data/2.5/weather?appid=" + appid + "&q=" + city_name
    json_message = get_weather_deatail(openweathermap_api_endpoint)
    Producer.send(kafka_topic_name, json_message)
    print("Published messgae 1 : " + json.dumps(json_message))
    print("wait for 2 seconds ...")
    time.sleep(2)



