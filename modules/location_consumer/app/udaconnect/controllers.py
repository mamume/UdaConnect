from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource


api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa