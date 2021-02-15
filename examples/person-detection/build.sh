curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
bin/arduino-cli core install arduino:mbed
bin/arduino-cli lib install JPEGDecoder@1.8.0
git clone --quiet https://github.com/ArduCAM/Arduino.git && cp -r Arduino/ArduCAM $HOME/Arduino/libraries
git clone --quiet https://github.com/antmicro/tensorflow-arduino-examples.git && cp -r tensorflow-arduino-examples/tensorflow $HOME/Arduino/libraries
sed -i'' '/#define DEBUG_SERIAL_OBJECT/s/(Serial)/(Serial1)/' $HOME/Arduino/libraries/tensorflow/src/tensorflow/lite/micro/arduino/system_setup.cpp
 > $HOME/Arduino/libraries/JPEGDecoder/src/User_Config.h
bin/arduino-cli compile -b arduino:mbed:nano33ble --output-dir binaries/person_detection $HOME/Arduino/libraries/tensorflow/examples/person_detection