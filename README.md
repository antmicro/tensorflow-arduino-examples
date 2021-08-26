# TensorFlow Lite Micro on Arduino Nano examples

Copyright (c) 2021 [Antmicro](https://www.antmicro.com)

This repository, developed in collaboration between Antmicro and Google's TF Lite Micro team, contains sources, tests, Google colabs and other material which use [TF Lite Micro](https://www.tensorflow.org/lite/microcontrollers) and [Renode](https://renode.io/) to enable easily running TF Lite Micro demos.

## Repo structure

* `.github/workflows` - GH actions files
  * `generate_ipynb_files.yml` - generating `ipynb` files from `py` sources
  * `test_examples.yml` - building and testing examples
* `examples` - scripts, tests and colab files for specific TensorFlow Lite examples
  * `hello_world` - hello world demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/hello-world/hello_world.ipynb)
  * `micro_speech` - micro speech demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/micro-speech/micro_speech.ipynb)
  * `magic_wand` - magic wand demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/magic-wand/magic_wand.ipynb)
  * `person_detection` - person detection demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/person-detection/person_detection.ipynb)
* `tflite-micro` - `tensorflow/tflite-micro-arduino-examples` submodule
