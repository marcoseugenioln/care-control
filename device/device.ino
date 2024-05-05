
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
#define PIN_BUTTON_EVENT_1 12
#define PIN_BUTTON_EVENT_2 14
#define PIN_BUTTON_EVENT_3 27

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

  button_alarm.begin();
  button_event_1.begin();
  button_event_2.begin();
  button_event_3.begin();
  alarm_led.begin();
  wifi_led.begin();
  button_led_1.begin();
  button_led_2.begin();
  button_led_3.begin();
  pinMode(PIN_BUZZER, OUTPUT);

  xTaskCreatePinnedToCore (
    loopButton1,     // Function to implement the task
    "loopButton1",   // Name of the task
    3000,      // Stack size in words
    NULL,      // Task input parameter
    0,         // Priority of the task
    NULL,      // Task handle.
    0          // Core where the task should run
  );

  xTaskCreatePinnedToCore (
    loopButton2,     // Function to implement the task
    "loopButton2",   // Name of the task
    3000,      // Stack size in words
    NULL,      // Task input parameter
    0,         // Priority of the task
    NULL,      // Task handle.
    0          // Core where the task should run
  );

  xTaskCreatePinnedToCore (
    loopButton3,     // Function to implement the task
    "loopButton3",   // Name of the task
    3000,      // Stack size in words
    NULL,      // Task input parameter
    0,         // Priority of the task
    NULL,      // Task handle.
    0          // Core where the task should run
  );

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
  if (millis() - last_millis >= 60*1000UL) 
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
      intapp.alarmOn(alarm_id);

      tone(PIN_BUZZER, ALARM_FREQUENCE);
      
      while(!button_alarm.isReleased()){ continue; }

      intapp.alarmOff(alarm_id);
      noTone(PIN_BUZZER);
    }
    
    // turn alarm led off
    alarm_led.off();
  }
}

// the loop2 function also runs forver but as a parallel task
void loopButton1 (void* pvParameters) 
{
  while (1) 
  {
    // check if event button was clicked
    while (!button_event_1.isReleased()){ continue; }

    button_led_1.on();
    intapp.logEvent(1);
    button_led_1.off();
  }
}

void loopButton2 (void* pvParameters) 
{
  while (1) 
  {
    // check if event button was clicked
    while (!button_event_2.isReleased()){ continue; }

    button_led_2.on();
    intapp.logEvent(2);
    button_led_2.off();
  }
}

void loopButton3 (void* pvParameters) 
{
  while (1) 
  {
    // check if event button was clicked
    while (!button_event_3.isReleased()){ continue; }

    button_led_3.on();
    intapp.logEvent(3);
    button_led_3.off();
  }
}
