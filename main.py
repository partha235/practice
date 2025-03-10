import dht
import machine
import time
import bmp180

# **Setup DHT11 sensor**
DHT_PIN = 14  # Change this to your GPIO pin
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN))

# **Setup BMP180 sensor (I2C)**
I2C_SDA = 21  # Default ESP32 SDA
I2C_SCL = 22  # Default ESP32 SCL
i2c = machine.I2C(scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA), freq=100000)
bmp = bmp180.BMP180(i2c)
bmp.oversample_sett = 2
bmp.baseline = 101325  # Default sea level pressure

# **Filename to store data**
FILENAME = "senread.txt"

# **Function to read sensors and log data**
def log_sensor_data():
    try:
        # **Read DHT11 sensor**
        dht_sensor.measure()
        temperature_dht = dht_sensor.temperature()
        humidity = dht_sensor.humidity()

        # **Read BMP180 sensor**
        temperature_bmp = bmp.temperature
        pressure = bmp.pressure
        altitude = bmp.altitude

        # **Format timestamp**
        timestamp = time.localtime()
        log_entry = "{}-{}-{} {}:{}:{} - DHT Temp: {}°C, Humidity: {}%, BMP Temp: {}°C, Pressure: {} hPa, Altitude: {} m\n".format(
            timestamp[0], timestamp[1], timestamp[2],  # Date
            timestamp[3], timestamp[4], timestamp[5],  # Time
            temperature_dht, humidity,
            temperature_bmp, pressure / 100, altitude
        )

        # **Append data to file**
        with open(FILENAME, "a") as file:
            file.write(log_entry)

        print("Logged:", log_entry.strip())

    except Exception as e:
        print("Error reading sensors:", e)

# **Run five times a day (every ~5 hours)**
READ_INTERVAL = 5 * 60 * 60  # 5 hours in seconds
READ_COUNT = 5

for _ in range(READ_COUNT):
    log_sensor_data()
    time.sleep(READ_INTERVAL)
