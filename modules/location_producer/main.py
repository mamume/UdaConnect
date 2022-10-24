from concurrent import futures
from kafka import KafkaProducer
import json

import grpc
import location_pb2
import location_pb2_grpc
import time


TOPIC_NAME = 'locations'
# KAFKA_SERVER = ""

producer = KafkaProducer(
    # bootstrap_servers=KAFKA_SERVER
)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print('Received a location!')
        
        request_value = {
            "person_id": int(request.person_id),
            "latitude": float(request.latitude),
            "longitude": float(request.longitude),
        }

        print(request_value)

        producer.send(TOPIC_NAME, json.dumps(request_value).encode())
        producer.flush()

        return location_pb2.LocationMessage(**request_value)

# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print('Server starting on port 5005...')
server.add_insecure_port("[::]:5005")
server.start()

# Keep thread alive
server.wait_for_termination()