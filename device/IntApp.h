#ifndef INTAPP.H
#define INTAPP.H
#include <HTTPClient.h>

class IntApp {
private:
  String _host;
  HTTPClient _client;
  int _code;
  int _device_id;

public:
  IntApp(String host, int device_id) : 
  _host(host),
  _device_id(device_id) 
   {
    //empty
   }

  void alarmOn(int alarm_id)
  {
    String request = this->_host + "/device/alarm-on/" + String(this->_device_id) +  "/" + String(alarm_id);

    this->_client.begin(request);
    this->_code = this->_client.GET();

    if (this->_code > 0) 
    {
        String payload = this->_client.getString();
    }
  }

  void alarmOff(int alarm_id)
  {
    String request = this->_host + "/device/alarm-off/" + String(this->_device_id) +  "/" + String(alarm_id);

    this->_client.begin(request);
    this->_code = this->_client.GET();

    if (this->_code > 0) 
    {
        String payload = this->_client.getString();
    }
  }

  void logEvent(int button_id)
  {
    String request = this->_host + "/device/log/" + String(this->_device_id) +  "/" + String(button_id);

    this->_client.begin(request);
    this->_code = this->_client.GET();

    if (this->_code > 0) 
    {
        String payload = this->_client.getString();
    }
  }

  int triggerAlarm()
  {
    String request = this->_host + "/device/trigger-alarm/" + String(this->_device_id);

    this->_client.begin(request);
    this->_code = this->_client.GET();

    if (this->_code > 0) 
    {
        String payload = this->_client.getString();
        return payload.toInt();
    }
    else{
      return 0;
    }
  }
};
#endif