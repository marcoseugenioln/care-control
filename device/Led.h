#ifndef LED.H
#define LED.H
class Led {
private:
  bool _state = false;
  uint8_t _pin;

public:
  Led(uint8_t pin) : _pin(pin) {}

  void begin() {
    pinMode(this->_pin, OUTPUT);
  }

  void on()
  {
    this->_state = true;
    digitalWrite(this->_pin, HIGH);
  }

  void off()
  {
    if (this->_state)
    {
      this->_state = false;
      digitalWrite(this->_pin, LOW);
    }
  }

  bool isOn()
  {
    return this->_state;
  }
};
#endif