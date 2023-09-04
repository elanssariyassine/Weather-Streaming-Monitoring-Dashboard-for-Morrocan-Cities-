# Weather Streaming Monitoring Dashboard for Morrocan Cities
## Introduction
In the realm of modern meteorology and environmental monitoring, real-time data insights are invaluable. 
The project at hand represents an innovative leap forward in the field of weather monitoring by harnessing the power of big data technologies to create a dynamic and responsive streaming dashboard. 
This cutting-edge endeavor seeks to provide meteorologists, researchers, and stakeholders with an unprecedented tool for visualizing, analyzing,
and making critical decisions based on live weather data.

my Weather Monitoring Streaming Dashboard project is poised to transform the way we perceive and interact with weather-related information.
By seamlessly integrating big data technologies, such as real-time data streaming, data processing frameworks, and interactive visualization tools, we are enabling the rapid acquisition, processing, and presentation of meteorological data.
This real-time capability allows for the instant detection of weather anomalies, the tracking of storm systems,
and the monitoring of climate trends as they unfold.

## Data Pipline

![](https://github.com/elanssariyassine/Weather-Streaming-Monitoring-Dashboard-for-Morrocan-Cities-/blob/main/Data%20Pipline.png)

## Data Source 

**OpenWeather API : https://openweathermap.org/api**

![](https://github.com/elanssariyassine/Weather-Streaming-Monitoring-Dashboard-for-Morrocan-Cities-/blob/main/OpenWeather.png)

## Tools 
- **Kafka :** Kafka is an open-source distributed data streaming platform used for real-time event data ingestion, processing, and distribution.
- **Spark :** Spark is an open-source, fast, and versatile big data processing framework for distributed data analytics and machine learning.
- **Hdfs :** Hadoop Distributed File System (HDFS) is a distributed storage system designed for storing and managing vast amounts of data across a cluster of commodity hardware
- **Hive :** Hive is a data warehouse infrastructure built on top of Hadoop that provides a query language (HiveQL) for querying and analyzing large datasets stored in Hadoop Distributed File System (HDFS)
- **PrestoDB :** PrestoDB is an open-source, distributed SQL query engine designed for fast and interactive querying of data across various data sources, including Hadoop, relational databases, and more.

## Project Steps : 

- **Data Collection :* retrieve weather information for multiple morrocan  cities from the OpenWeatherMap API and publishes the data (JSON format) to a Kafka topic using the Kafka Producer from the kafka-python package .
**for that you have to run zookeper and kafka servers firstly and create a kafka topic**

- **Data Processing :* seting up a Spark Structured Streaming job to ingest data from Kafka, process it, and output the results to both the console and HDFS (Csv Format).

- seting up a REST API service for accessing weather data from a PrestoDB database. Clients can make GET requests to the /v1 endpoint to retrieve weather information. The service is run on port 8093 when the script is executed directly.

It is important to note that the code assumes that PrestoDB is properly set up and configured with a 'weather_detail_tbl' table, and it connects to this database to retrieve weather information. Additionally, it uses Flask and CherryPy for serving the API over HTTP

- **Dashboard :*  creation of a web-based dashboard using the Dash framework for real-time weather monitoring.
Key Features:

* The dashboard displays real-time weather data, including temperature and humidity, for morrocan cities.
* The "current time" field is updated every second to indicate the latest refresh time.
* The bar chart displays temperature and humidity for morrocan cities.
* The data table provides a paginated view of weather records.
**Users can access the dashboard through a web browser to monitor real-time weather data. It continuously fetches and updates weather information from the specified API endpoint.**






