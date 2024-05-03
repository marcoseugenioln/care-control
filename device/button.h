#ifndef BUTTON.H
#define BUTTON.H
class Button {
private:
  bool _state;
  uint8_t _pin;

public:
  Button(uint8_t pin) : _pin(pin) {}

  void begin() {
    pinMode(this->_pin, INPUT_PULLUP);
    _state = digitalRead(_pin);
  }

  bool isReleased() {
    bool v = digitalRead(_pin);
    if (v != this->_state) {
      this->_state = v;
      if (this->_state) {
        return true;
      }
    }
    return false;
  }
};
#endif