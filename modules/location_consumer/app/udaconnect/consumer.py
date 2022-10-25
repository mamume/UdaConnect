import json
import logging
from typing import Dict

from __init__ import db
from geoalchemy2.functions import ST_Point
from kafka import KafkaConsumer
from models import Location
from schemas import LocationSchema

logger = logging.getLogger("udaconnect-locations-api")

TOPIC_NAME = 'locations'
KAFKA_SERVER = '10.43.42.146:9092'

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_SERVER,
    api_version=(0, 10, 2)
)


def create_location(location):
    validation_results: Dict = LocationSchema().validate(location)

    if validation_results:
        logger.warning(
            f"Unexpected data format in payload: {validation_results}")
        raise Exception(f"Invalid payload: {validation_results}")

    new_location = Location()
    new_location.person_id = location["person_id"]
    new_location.creation_time = location["creation_time"]
    new_location.coordinate = ST_Point(
        location["latitude"], location["longitude"])
    db.session.add(new_location)
    db.session.commit()

    return new_location


for message in consumer:
    location_data = message.value.decode('utf-8')

    print(location_data)
    location = json.loads(location_data)
    create_location(location)
