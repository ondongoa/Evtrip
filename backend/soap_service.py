from spyne import Application, rpc, ServiceBase, Float, Integer
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

class TravelService(ServiceBase):
    @rpc(Float, Float, Integer, _returns=Float)
    def calculate_travel_time(ctx, distance_km, autonomy_km, average_charge_time_min):
        # Simplifié: temps de conduite + temps de recharge nécessaire
        avg_speed = 90.0
        drive_time_h = distance_km / avg_speed
        # calcul nombre d'arrêts
        nb_stops = int(distance_km / autonomy_km)
        total_charge_min = nb_stops * average_charge_time_min
        return drive_time_h + (total_charge_min / 60.0)

soap_app = Application([TravelService], 'evtrip.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())
wsgi_app = WsgiApplication(soap_app)

# Pour lancer via gunicorn: exposer wsgi_app ou wrapper
