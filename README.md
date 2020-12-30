## TensorFlow Lite Micro Google examples

This repository, developed in collaboration between Antmicro and Google's TF Lite Micro team, is a work in progress but is ultimately meant to contain sources, tests, Google colabs and other material which use TF Lite Micro and Renode to enable easily running TF Lite Micro demos.

### Repo structure

* `.github/workflows` - GH actions files (currently only generating `ipynb` files from `py` sources)
* `notebooks` - interactive Google Colab demos
  * `person detection` - person detection demo on nrf52840 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antmicro/tensorflow-arduino-examples/blob/master/notebooks/person_detection/person_detection.ipynb)
* `tensorflow` - example sources and Arduino lib, generated from the TF repository by a dedicated GH action [stored in a separate repo](https://github.com/antmicro/tensorflow-examples-generator)
