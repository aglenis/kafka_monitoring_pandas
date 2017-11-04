# Kafka Monitoring using prometheus and JMX exporter

## Install Confluent platform
Head to ``` confluent.io ``` and download the confluent open source release.

I run the confluent processes as my normal user.
```
tar -xvf my_tar
sudo mv my_extracted_files_folder /opt/confluent
chown -R aglenis /opt/confluent
```

## Download JMX exporter
```
sudo mkdir -p /opt/kafka_monitoring
wget https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.6/jmx_prometheus_javaagent-0.6.jar
mv jmx_prometheus_javaagent-0.6.jar /opt/kafka_monitoring
mv prometheus_configs/kafka-0-8-2.yml /opt/kafka_monitoring
```
## Download Prometheus TSDB
Change to the correct release and version for your platform
```
wget https://github.com/prometheus/prometheus/releases/download/v1.2.1/prometheus-1.2.1.linux-amd64.tar.gz
tar -xzf prometheus-*.tar.gz
cd prometheus-*
```

## Setup Kafka to use the JMX exporter
You have to set the following environment variables before starting kafka.
```
KAFKA_JMX_OPTS="-Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=<ipaddress> -Dcom.sun.management.jmxremote.port=$JMX_PORT -Dcom.sun.management.jmxremote.rmi.port=$JMX_PORT"

KAFKA_OPTS="$KAFKA_OPTS -javaagent:/opt/kafka_monitoring/jmx_prometheus_javaagent-0.6.jar=7071:/opt/kafka_monitoring/kafka-0-8-2.yml"

```
## Configure Prometheus to scrape from Kafka JMX exporter
A sample  config file is as follows
```
global:
 scrape_interval: 10s
 evaluation_interval: 10s
scrape_configs:
 - job_name: 'kafka'
   static_configs:
    - targets:
      - localhost:7071
```
## Start Kafka

### Standalone installation
If you prefer to use a standalone installation I would suggest that you add the environment variables on the kafka-server-start file of Kafka.

After you have done this then it is then it is just a matter of starting Kafka and Zookeeper.
```
zookeeper-server-start /opt/confluent/etc/kafka/zookeeper.properties
kafka-server-start standalone_kafka_configs/server.properties
```
### Using supervisord
A much more structured approach is to use supervisord to manage the kafka processes on your system.
It works both on Linux and Mac OS X so there shouldn't be any problems.
```
sudo pip install supervisor
```
To run supervisord you have to have a supervisord.conf file. A sample is provided in the github repo. Make sure to change the folder of the logs in order for it to work.

After you have installed supervisord it is just a matter of pointing supervisord to the correct config files.
Make sure to change the user in the config files to your user.
```
sudo mkdir -p  /usr/local/share/supervisor/conf.d/
sudo cp supervisord_kafka_configs/*.conf /usr/local/share/supervisor/conf.d/
```
```
supervisord -c supervisord.conf
supervisorctl
```
This will automatically start the zookeeper and the kafka broker. After that you can issue:
```
supervisorctl stop broker
```
To stop Kafka.
Relevant stuff:
```
https://nicksergeant.com/running-supervisor-on-os-x/
https://stackoverflow.com/questions/14479894/stopping-supervisord-shut-down
```
## Create a sample topic
```
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 3 --topic test_topic
```
## Run a simple producer to generate traffic
```
date +%s
kafka-producer-perf-test --topic test_topic --throughput 10000 --record-size 300 --num-records 20000 --producer-props bootstrap.servers="localhost:9092"
date +%s
```
## Monitor things from the web-browser
We have setup the jmx exporter to point to port 7071, meaning that you can that you can point your browser to:
```
http://localhost:7071/metrics
```
And see your metrics as json in the browser page.
## Monitor from prometheus page
Since looking at metrics from JSON is not the most convenient for humans head to:
```
http://localhost:9090
```

## Get your metrics using Python

## Run the notebooks

### Install prerequisites
```
pip3 install jupyter
pip3 install pandas
pip3 install matplotlib
pip3 install requests
```
### Open a jupyter notebooks
```
jupyter notebook
```
### Standalone Python stuff
