try:
    import adafruit_dht
    adafruit_dht_AVAILABLE = True
except ImportError:
    adafruit_dht_AVAILABLE = False
    adafruit_dht = None

import logging

logger = logging.getLogger("DHTxxSensor")


class DHTxxSensorCollector:

    def __init__(self, dht_config: dict,):
        if not adafruit_dht_AVAILABLE:
            logger.error("adafruit_dht library not available - cannot read DHTxx sensor")
            return {"error": "adafruit_dht library not available - cannot read DHTxx sensor"}

        sensor_type = dht_config.get("type")
        pin = dht_config.get("pin")

        if sensor_type not in [11, 22]:
            logger.error(
                f"Unsupported sensor type: {sensor_type}. Only DHT11 and DHT22 are supported."
            )
            return {
                "error": f"Unsupported sensor type: {sensor_type}. Only DHT11 and DHT22 are supported."
            }
        elif sensor_type == 11:
            self.sensor = adafruit_dht.DHT11(pin)
        elif sensor_type == 22:
            self.sensor = adafruit_dht.DHT22(pin)

    def get_reading(self):
        temperature = self.sensor.temperature
        humidity = self.sensor.humidity
        if temperature is None or humidity is None:
            logger.error("Failed to read from DHTxx sensor")
            return {"error": "Failed to read from DHTxx sensor"}

        readings = {"temperature_c": temperature, "humidity_percent": humidity}

        return readings
