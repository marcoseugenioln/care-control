
#include "button.h"
#include "WifiConnection.h"
#include "IntApp.h"
#include "Led.h"

// pin leds
#define PIN_LED_ALARM 23
#define PIN_LED_WIFI 22
#define PIN_LED_EVENT_1 21
#define PIN_LED_EVENT_2 19
#define PIN_LED_EVENT_3 18

// pin buzzer
#define PIN_BUZZER 2

// pin buttons
#define PIN_BUTTON_ALARM 13
#define PIN_BUTTON_EVENT_1 21
#define PIN_BUTTON_EVENT_2 19
#define PIN_BUTTON_EVENT_3 18

// auxiliar data
#define ALARM_FREQUENCE 250
#define DEVICE_ID 1
#define NO_ALARM 0
#define SSID "NICOLE_E_MARCOS"
#define PASS "Dv010400"
#define HOST "http://192.168.1.7:3000/"

// leds objects
Led wifi_led(PIN_LED_WIFI);
Led alarm_led(PIN_LED_ALARM);
Led button_led_1(PIN_LED_EVENT_1);
Led button_led_2(PIN_LED_EVENT_2);
Led button_led_3(PIN_LED_EVENT_3);

// button objects
Button button_alarm(PIN_BUTTON_ALARM);
Button button_event_1(PIN_BUTTON_EVENT_1);
Button button_event_2(PIN_BUTTON_EVENT_2);
Button button_event_3(PIN_BUTTON_EVENT_3);

// wifi connection class
WifiConnection wifi(String(SSID), String(PASS));

// interface with web application
IntApp intapp(String(HOST), DEVICE_ID);

unsigned long last_millis;
int alarm_id;

/****************************************************************************************************************/
void setup() 
{
  // init serial communication
  Serial.begin(9600);
  delay(1000);

  Serial.println("Starting device components");
  button_alarm.begin();
  button_event_1.begin();
  button_event_2.begin();
  button_event_3.begin();
  alarm_led.begin();
  wifi_led.begin();
  button_led_1.begin();
  button_led_2.begin();
  button_led_3.begin();
  //alarm_buzzer.begin();
  pinMode(PIN_BUZZER, OUTPUT);

  Serial.println("Starting wifi connection");
  
  // start wifi connection
  wifi.connect();

  if (wifi.isConnected())
  {
    wifi_led.on();
  }
}
/****************************************************************************************************************/
void loop() 
{
  // check wifi connection 
  if (!wifi.isConnected())
  {
    // turn wifi led off
    wifi_led.off();

    // try to connect again if necessary
    wifi.connect();

    // turn led on again
    wifi_led.on();
  }


  // perform alarm check every minute
  if (millis() - last_millis >= 2*1000UL) 
  {
    // turn alarm led on
    alarm_led.on();

    // prepare for next iteration
    last_millis = millis(); 

    // obtain alarm info from server
    alarm_id = intapp.triggerAlarm();

    // check if alarm should be triggered
    if (alarm_id != NO_ALARM)
    {
      Serial.println("sending alarm on request.");
      intapp.alarmOn(alarm_id);

      Serial.println("ringing buzzer.");
      tone(PIN_BUZZER, ALARM_FREQUENCE);
      
      Serial.println("wating for button clicked.");
      while(!button_alarm.isReleased()){ continue; }
      Serial.println("button clicked.");

      Serial.println("sending alarm off request.");
      intapp.alarmOff(alarm_id);
      noTone(PIN_BUZZER);
    }
    
    // turn alarm led off
    alarm_led.off();
  }

  // check if event button was clicked
  if (button_event_1.isReleased())
  {
    intapp.logEvent(1);
  }

  if (button_event_2.isReleased())
  {
    intapp.logEvent(2);
  }

  if (button_event_3.isReleased())
  {
    intapp.logEvent(3);
  }
}
