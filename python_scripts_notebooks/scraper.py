from prometheus_client.parser import text_string_to_metric_families
import requests
import json
import pandas as pd

prometheus_hostname = 'localhost'
prometheus_port = '9090'
target_metric = 'kafka_server_brokertopicmetrics_bytesout_total'
prometheus_query = 'sum({0}) by (topic)'.format(target_metric)
start_time_unix = '1507893710'
end_time_unix = '1507893730'
step = '10s'
query_str = "http://{0}:{1}/api/v1/query_range?query={2}&start={3}&end={4}&step={5}".format(prometheus_hostname,
                    prometheus_port,
                    prometheus_query,
                    start_time_unix,
                    end_time_unix,
                    step)

metrics = requests.get(query_str).content

target_topic = 'test_topic'

#print(metrics)
json_object = json.loads(metrics.decode('utf-8'))
result=json_object['data']['result']
#print(result)
for partial_result in result:
    try:
        if partial_result['metric']['topic'] == target_topic :
             print(partial_result)
             #print(partial_result['metric']['topic'])
    except KeyError:
        pass
final_data = pd.DataFrame(data = partial_result['values'],
                          columns = ['Timestamp','value'])
print(final_data)
