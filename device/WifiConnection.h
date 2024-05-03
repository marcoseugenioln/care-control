#ifndef WIFICONNECTION.H
#define WIFICONNECTION.H

#include <WiFi.h>

class WifiConnection {
private:
  String _ssid;
  String _pass;

public:
  WifiConnection(String ssid, String pass) : 
  _ssid(ssid), 
  _pass(pass) 
  {
    // empty
  }

  void connect() {
    WiFi.mode(WIFI_STA);
    WiFi.begin(this->_ssid, this->_pass);

    while(WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
    }
  }

  bool isConnected() {
    // check wifi connection 
    return WiFi.status() == WL_CONNECTED;
  }
};
#endif