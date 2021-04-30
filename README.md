## TensorFlow Lite Micro examples

Copyright (c) 2021 [Antmicro](https://www.antmicro.com)

This repository, developed in collaboration between Antmicro and Google's TF Lite Micro team, is a work in progress but is ultimately meant to contain sources, tests, Google colabs and other material which use [TF Lite Micro](https://www.tensorflow.org/lite/microcontrollers) and [Renode](https://renode.io/) to enable easily running TF Lite Micro demos.

### Repo structure

* `.github/workflows` - GH actions files
  * `generate_ipynb_files.yml` - generating `ipynb` files from `py` sources
  * `test_examples.yml` - building and testing examples
* `examples` - scripts, tests and colab files for specific TensorFlow Lite examples
  * `hello-world` - hello world demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/hello-world/hello_world.ipynb)
  * `micro-speech` - micro speech demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/micro-speech/micro_speech.ipynb)
  * `magic-wand` - magic wand demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/magic-wand/magic_wand.ipynb)
  * `person-detection` - person detection demo on Arduino Nano 33 BLE Sense [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/examples/person-detection/person_detection.ipynb)
* `tensorflow` - example sources and Arduino lib, generated from the TF repository by a dedicated GH action [stored in a separate repo](https://github.com/antmicro/tensorflow-examples-generator)
