import prestodb.dbapi
from flask import Flask,request
from flask_restplus import Api,Resource,fields
from markupsafe import escape


import cherrypy
from cherrypy.process.plugins import Daemonizer
from paste.translogger import TransLogger

from pyhive import presto
import time
import datetime as dt

flask_app = Flask(__name__)
app=Api(app=flask_app,version="1.0",title="Weather Monitoring",description="Weather Monitoring Apis")

name_space=app.namespace('wm',description='Weather Monitoring')
model = app.model('WeatherDetailModel',{'CityName':fields.String(required=True
                                                                 ,description="Name of City",
                                                                 help="CityName cannot be blank"),
                                        'Tempertaure':fields.String(required=True,
                                                                    description="City's Temperature",
                                                                    help="Temperature cannot be blank"),
                                        'Humidity':fields.String(required='True',
                                                                 description="City's Humidity",
                                                                 help="Humidity cannot be blank"),
                                        'CreationTime':fields.String(required=True,
                                                                     description="Record's CreationTime",
                                                                     help="Humidity cannot be blank"),
                                        'CreationDate':fields.String(required=True,
                                                                     description="Record's EventTime(ReceivedTime)",
                                                                     help="EventTime cannot be blank")


                                        })

weather_detail_pd_df=None

def get_presto_connection():
    print("Creating Presto Connection...")
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    connection_obj=prestodb.dbapi.connect(
        host='localhost',
        port='8099',
        catalog='hive',
        schema='default',
    )
    return connection_obj



def get_weather_details():
    records_list = []
    refresh_time_1 = time.strftime("%Y-%m-%d %H:%M:%S")
    refresh_date_1 = time.strftime("%Y-%m-%d")

    record_1 = {
        "CityName": "agadir",
        "Temperature": 290,
        "Humidity": 56,
        "CreationTime": refresh_time_1,
        "CreationDate": refresh_date_1
    }
    records_list.append(record_1)

    record_2 = {
        "CityName": "sidi ifni",
        "Temperature": 312,
        "Humidity": 45,
        "CreationTime": refresh_time_1,
        "CreationDate": refresh_date_1
    }
    records_list.append(record_2)

    record_3 = {
        "CityName": "casablanca",
        "Temperature": 285,
        "Humidity": 49,
        "CreationTime": refresh_time_1,
        "CreationDate": refresh_date_1
    }
    records_list.append(record_3)

    record_4 = {
        "CityName": "dakhla",
        "Temperature": 322,
        "Humidity": 62,
        "CreationTime": refresh_time_1,
        "CreationDate": refresh_date_1
    }
    records_list.append(record_4)

    return records_list

@name_space.route("/v1")
class WeatherMonitoring(Resource):
    @app.doc(responses={200:'OK',400:'Invalid Argument Provided',500:'Mapping Key Error Occured'})
    def get(self):
        try:
            weather_detail_list = []
            '''connection_obj=get_presto_connection()
            cursor_obj=connection_obj.cursor()
            cursor_obj.execute('SELECT * FROM weather_detail_tbl order by CreationTime desc limit 10')
            rows=cursor_obj.fetchall()
            print(type(rows))
            
            for row in rows:
                print(row)
                weather_detail={"CityName":row[0],"Temperature":row[1],"Humidity":row[2],"CreationTime":row[3],
                                "CreationDate":row[4]}
                weather_detail_list.append(weather_detail)'''



            weather_detail_list=get_weather_details()
            return weather_detail_list
        except KeyError as e:
            name_space.abort(500,e.__doc__,status="could not retrive weather information",statusCode="500")
        except Exception as e :
            name_space.abort(400,e.__doc__,status="could not retrive weather information",statusCode="400")


def run_server(flask_app):
    app_logged=TransLogger(flask_app)
    cherrypy.tree.graft(app_logged,'/')
    cherrypy.config.update(
        {
            'engine.autoreload.on':True,
            'log.screen':True,
            'server.socket_port':8199,
            'server.socket_host':'localhost'
        }
    )
    Daemonizer(cherrypy.engine).subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    print("starting weather monitoring api service app...")
    flask_app.run(port=8090,debug=True)


