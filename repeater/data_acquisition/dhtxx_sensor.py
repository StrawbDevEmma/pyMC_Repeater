try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    GPIO = None
try:
    import dht11
    DHT11_AVAILABLE = True
except ImportError:
    DHT11_AVAILABLE = False
    dht11 = None

import logging

logger = logging.getLogger("DHTxxSensor")


class DHTxxSensorCollector:

    def __init__(self, dht_config: dict):
        self.dht_config = dht_config
        self.pin = self.dht_config.get("pin", None) 
        self.sensor = None
        self._init_sensor()

    def _init_sensor(self): 
        if not GPIO_AVAILABLE:
            logger.error("RPi.GPIO library not available - cannot initialize DHTxx sensor")
            return {"error": "RPi.GPIO library not available - cannot initialize DHTxx sensor"}
        if not DHT11_AVAILABLE:
            logger.error("dht11 library not available - cannot read DHTxx sensor")
            return {"error": "dht11 library not available - cannot read DHTxx sensor"}
    
        #setup GPIO for DHT sensor
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        self.sensor = dht11.DHT11(pin = self.pin)
        logger.info(f"DHTxx sensor initialized on pin {self.pin}")

    def get_reading(self):
        result = self.sensor.read()
        if result.is_valid():
            readings = {
                "temperature": result.temperature,
                "humidity": result.humidity
            }
            logger.debug(f"DHTxx sensor reading: {readings}")
            return readings
        else:
            logger.warning(f"DHTxx sensor reading invalid, Error code: {result.error_code}")
            return {"error": f"DHTxx sensor reading invalid, Error code: {result.error_code}"}
