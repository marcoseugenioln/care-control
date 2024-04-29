#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const int guid = 1;

const char* ssid = "NICOLE_E_MARCOS";
const char* password = "Dv010400";

int pin_led_wifi = 22;

HTTPClient http;
int httpCode;

void connect_to_wifi()
{
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(pin_led_wifi, HIGH);
    delay(1000);
    digitalWrite(pin_led_wifi, LOW);
  }

  if (WiFi.status() == WL_CONNECTED)
  {
    digitalWrite(pin_led_wifi, HIGH);
  }
}

void check_wifi_connection()
{
  // check wifi connection 
  if (WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(pin_led_wifi, LOW);

    // try to connect again if necessary
    connect_to_wifi();
  }
}

void request_device_data()
{
  http.begin("http://192.168.1.7:3000/device/data/" + guid);
  httpCode = http.GET();

  if (httpCode > 0) 
  {
    StaticJsonDocument<200> device_data;

    String payload = http.getString();
    
    char device_data_json[payload.length()];

    payload.toCharArray(device_data_json, payload.length());

    // Deserialize the JSON document
    DeserializationError error = deserializeJson(device_data, device_data_json);

    // Test if parsing succeeds.
    if (error) 
    {
      Serial.print(F("deserializeJson() failed: "));
      Serial.println(error.f_str());
      return;
    }

    
  }
}

void trigger_alarm()
{
  if(/* current time matches one of the alarms by a margin */ false)
  {
    /* activate buzzer and led */

    while(/* alarm button not hit */ false)
  	{
      continue;
    }

    /* deactivate buzzer and led */
  }
}

/****************************************************************************************************************/
void setup() 
{
  // set wifi led pin
  pinMode(pin_led_wifi, OUTPUT);

  // init serial communication
  Serial.begin(9600);
  delay(1000);

  // start wifi connection
  connect_to_wifi();
}
/****************************************************************************************************************/
void loop() 
{
  check_wifi_connection();

  request_device_data();

  trigger_alarm();
}
