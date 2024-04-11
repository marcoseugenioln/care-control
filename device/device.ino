#include <WiFi.h>
#include <HTTPClient.h>

const int guid = 1;

const char* ssid = "NICOLE_E_MARCOS";
const char* password = "Dv010400";

int pin_led_wifi = 22;

HTTPClient http;
int httpCode;

String alarms[5];
String events[5];

void connect_to_wifi()
{
  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    digitalWrite(pin_led_wifi, HIGH);
    delay(1000);
    digitalWrite(pin_led_wifi, LOW);
  }

  if (WiFi.status() == WL_CONNECTED)
  {
    digitalWrite(pin_led_wifi, HIGH);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

void check_wifi_connection()
{
  // check wifi connection 
  if (WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(pin_led_wifi, LOW);
    Serial.print("Wifi not connected.");

    // try to connect again if necessary
    connect_to_wifi();
  }
}

void request_alarm_schedule()
{
  http.begin("http://192.168.1.7:3000/request-alarm-schedule/1");
  httpCode = http.GET();

  if (httpCode > 0) 
  {
    String payload = http.getString();
    Serial.println("HTTP Code: ");
    Serial.println(payload);
  }
  
  else 
  {
    Serial.println("Error on HTTP request");
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
  request_alarm_schedule();
}
