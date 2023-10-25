
import org.apache.log4j.spi.TriggeringEventEvaluator
import org.apache.spark.sql.{SparkSession, functions}
import org.apache.spark.SparkContext
import org.apache.spark.sql.types.{DateType, DoubleType, IntegerType, StringType, StructField, StructType}
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.streaming.Trigger.ProcessingTime


object weather_monitoring_streaming_demo{
  def main(args:Array[String]):Unit = {
    println("Weather Monitoring streaming with kafka Started ....")

    val KAFKA_TOPIC_NAME_CONS="weather_topic"
    val KAFKA_BOOTSTRAP_SERVERS_CONS="localhost:9092"



    val spark = SparkSession.builder.master("local[*]").appName("spark structed streaming with kafka demo")
      .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    //stream from kafka
    val weather_detail_df=spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers",KAFKA_BOOTSTRAP_SERVERS_CONS)
      .option("subscribe",KAFKA_TOPIC_NAME_CONS)
      .option("startingOffsets","latest")
      .load()

    println("Printing Schema of weather_detail_df : ")
    weather_detail_df.printSchema()
    val weather_detail_df_1 = weather_detail_df.selectExpr("CAST (value AS STRING) ","CAST (timestamp AS TIMESTAMP)")

    // Define a schema for the transaction_detail data
    /*val transaction_detail_schema = StructType(Array(
      StructField("CityName",StringType),
      StructField("Temperature",DoubleType),
      StructField("Humidity",IntegerType),
      StructField("CreationTime",StringType)
    ))*/

    /*val weather_detail_df_2 = weather_detail_df_1.select(from_json (col( "value"), transaction_detail_schema).as( "weather_detail " ),col("timestamp") )

     */

    val weather_detail_df_2 = weather_detail_df_1.select(
      functions.get_json_object(functions.col("value"), "$.CityName").as("CityName"),
      functions.get_json_object(functions.col("value"), "$.Temperature").cast(DoubleType).as("Temperature"),
      functions.get_json_object(functions.col("value"), "$.Humidity").cast(IntegerType).as("Humidity"),
      functions.get_json_object(functions.col("value"), "$.CreationTime").as("CreationTime"),
      functions.col("timestamp")
    )

    val weather_detail_df_3 = weather_detail_df_2.withColumn("CreationDate",weather_detail_df_2("CreationTime").cast(DateType))
    println("printing schema of weather_detail_df_3")
    weather_detail_df_3.printSchema()

    val weather_detail_df_4 = weather_detail_df_3.select("CityName","Temperature","Humidity","CreationTime","CreationDate")

    println("printing schema of weather_detail_df_4")
    weather_detail_df_4.printSchema()

    // write the result in console for debugging purpose
    val weather_detail_write_stream = weather_detail_df_4
      .writeStream
      .trigger(Trigger.ProcessingTime("10 seconds"))
      .outputMode("append")
      .option("truncate", "false")
      .format("console")
      .start()

    // write finale result into hdfs

    weather_detail_df_4.writeStream.format("csv")
      .option("path","hdfs://localhost:9000/user/weather")
      .option("checkpointLocation","hdfs://localhost:9000/user/weather_checkpoint")
      .start()

    weather_detail_write_stream.awaitTermination()
    println("weather monitoring streaming with kafka completed")
    





  }
}