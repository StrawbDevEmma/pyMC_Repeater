try:
    from pigpio_dht import DHT11, DHT22
    pigpio_dht_AVAILABLE = True
except ImportError:
    pigpio_dht_AVAILABLE = False
    DHT11 = None
    DHT22 = None

import logging

logger = logging.getLogger("DHTxxSensor")


class DHTxxSensorCollector:

    def __init__(self, dht_config: dict):
        self.dht_config = dht_config
        self.sensor_type = dht_config.get("type")
        self.pin = dht_config.get("pin") 
        self.sensor = None
        self._init_sensor()

    def _init_sensor(self): 
        if not pigpio_dht_AVAILABLE:
            logger.error("pigpio_dht library not available - cannot read DHTxx sensor")
            return {"error": "pigpio_dht library not available - cannot read DHTxx sensor"}

        if self.sensor_type not in [11, 22]:
            logger.error(
                f"Unsupported sensor type: {self.sensor_type}. Only DHT11 and DHT22 are supported."
            )
            return {
                "error": f"Unsupported sensor type: {self.sensor_type}. Only DHT11 and DHT22 are supported."
            }
        elif self.sensor_type == 11:
            self.sensor = DHT11(self.pin)
        elif self.sensor_type == 22:
            self.sensor = DHT22(self.pin)

    def get_reading(self):
        readings = self.sensor.read()
        if not readings.get("valid"):
            logger.error("Failed to read from DHTxx sensor")
            return {"error": "Failed to read from DHTxx sensor"}

        return readings
