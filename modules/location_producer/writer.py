import grpc
import location_pb2
import location_pb2_grpc

print('Sending location payload...')

channel = grpc.insecure_channel("localhost:5005")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=100,
    latitude=30.04,
    longitude=31.23
)

response = stub.Create(location)
