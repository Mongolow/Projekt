**Project Overview**

This project is a simple smart-home weather station dashboard focused on
monitoring an indoor (home) station while also allowing quick lookups of
outside weather for any city worldwide. It collects, stores and displays
temperature, humidity and pressure measurements from a local device (e.g.
ESP32) and provides both a web UI and a REST API for interaction. The web
interface lets you view the latest home readings, open historical charts,
browse and delete stored measurements. The API supports posting new readings
and retrieving or deleting stored data programmatically.

**Requirements**

- Python 3.8+
- The project's virtual environment (recommended)
- See `requirements.txt` for Python dependencies

**Quick Setup**

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app (development mode):

```bash
python app.py
```

The application will create an empty SQLite database file `Station_database.db`
automatically on first run if it is not present.

**Database and CLI Commands**

- Initialize the database manually: `flask init-db` (creates tables)
- Add example data: `flask seed-db`
- Add a random measurement: `flask add-measure`

Note: The repository ignores `.db` files (see `.gitignore`), so the database
file is not tracked. The application will create the database automatically
when first started.

**API Endpoints**

- `POST /api/weather/post` — Accepts JSON with `temp`, `hum`, and `press`.
  Example body: `{"temp": 23.5, "hum": 45.2, "press": 1012.3}`
  Returns: `201` and a JSON confirmation on success.

- `GET /api/weather/get` — Returns a JSON array of stored measurements.

- `GET /api/weather/get/<id>` — Returns a single measurement by `id`.

- `DELETE /api/weather/delete/<id>` — Deletes a measurement by `id`.

**Curl Examples**

Replace `localhost` with your host IP if running on another machine.

- POST a new measurement:

```bash
curl -X POST http://localhost:5001/api/weather/post \
  -H "Content-Type: application/json" \
  -d '{"temp": 23.5, "hum": 45.2, "press": 1012.3}'
```

- GET all measurements:

```bash
curl http://localhost:5001/api/weather/get
```

- GET a single measurement (id = 1):

```bash
curl http://localhost:5001/api/weather/get/1
```

- DELETE a measurement (id = 1):

```bash
curl -X DELETE http://localhost:5001/api/weather/delete/1
```

**Web Routes**

- `/` — Home page with links
- `/weather` — Displays the latest sensor values (house) and outside weather
  lookup
- `/database` — Paginated table of stored measurements
- `/charts` — Renders charts for temperature, humidity and pressure

**Timezones**

All timestamps stored in the database use UTC. The `created_at` column is set
using SQLite's `datetime('now')`, and the app labels displayed times as UTC.

**ESP32 / Device Notes**

- The `esp32_code.ino` example sends only sensor values (no timestamp); the
  server assigns the timestamp when inserting into the database.
- Configure the `serverName` constant in the sketch to point to your host
  (e.g. `http://<host-ip>:5001/api/weather/post`).

**Configuring the ESP32 sketch**

To use the provided `esp32_code.ino` with your local network, update the
Wi‑Fi credentials and the server address in the sketch. The minimum changes
are the `ssid`, `password` and `serverName` constants near the top of the
file. Example:

```cpp
// WiFi credentials
const char* ssid = "YOUR_SSID";       // <-- replace with your WiFi SSID
const char* password = "YOUR_PASS";   // <-- replace with your WiFi password

// Server endpoint (use the machine IP running the Flask app)
const char* serverName = "http://192.168.1.100:5001/api/weather/post"; // <-- replace with your host IP
```

Notes and tips:

- Make sure the ESP32 and the machine running the Flask app are on the same
  local network (same subnet) so the device can reach `serverName`.
- Use the host machine's LAN IP (not `localhost` or `127.0.0.1`) when
  pointing the ESP32 to the server (e.g. `192.168.1.100`).
- If your development machine has a firewall, allow incoming connections to
  port `5001` or run the server with a host that is reachable from the LAN.
- If you want a fixed address for the ESP32, configure a static IP in the
  sketch or reserve an IP in your router's DHCP settings.
- For debugging, open the Serial Monitor (baud `115200`) and watch connection
  logs printed by `Serial.print` in the sketch.

- The microcontroller sketch was developed and uploaded using the Arduino
  IDE. In the IDE, select the correct ESP32 board, the target port (COM/tty)
  and the correct upload speed before flashing.
- Use the Arduino IDE Serial Monitor (baud `115200`) to view runtime logs.
  Typical messages printed by the sketch include:
  - `Connecting to WiFi` and `.` during connection attempts
  - `Connected WiFi!` and `IP ESP32: <ip>` on successful connection
  - `Sending Data...` when the sketch posts sensor readings

**Sensor Hardware & Wiring**

This project uses a BME280 environmental sensor (temperature, humidity, pressure).

Power and ground:

- Connect `VCC` on the BME280 to the ESP32 `3.3V` supply.
- Connect `GND` on the BME280 to the ESP32 `GND`.

I2C wiring (default in `esp32_code.ino`):

- The sketch uses the I2C interface (`Wire.begin()`), and the code creates the
  BME280 instance with `bme.begin(0x76)` (address `0x76`). If your module uses
  `0x77`, change the address accordingly.
- Typical ESP32 I2C pins: `SDA` -> GPIO21, `SCL` -> GPIO22 (use the pins for
  your board or pass explicit pins to `Wire.begin(sda, scl)` if needed).

SPI wiring (alternative):

- The sketch contains commented examples for SPI initialization. If you want
  to use SPI, wire the sensor SPI pins and update the sketch to one of the
  SPI constructors:
  - `Adafruit_BME280 bme(BME_CS);` // hardware SPI
  - `Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO, BME_SCK);` // software SPI
- The sketch defines SPI pins near the top: `BME_SCK` = 13, `BME_MISO` = 12,
  `BME_MOSI` = 11, `BME_CS` = 10. Change them to match your wiring if needed.

Libraries required on ESP32 side:

- `Wire` (I2C)
- `SPI` (if using SPI)
- `Adafruit_Sensor`
- `Adafruit_BME280`
- `ArduinoJson` (used for POST payloads)

Notes:

- Use the `Adafruit_BME280` examples in the Arduino IDE to verify the sensor
  wiring and address before integrating with this project.
- Always power the BME280 with 3.3V when using ESP32 (not 5V unless the module
  has a level shifter).

**Development Tips**

- If you need to reset the database during development, delete
  `Station_database.db` and restart the app to recreate it.
- Use the provided Flask CLI commands to seed data and test endpoints.
