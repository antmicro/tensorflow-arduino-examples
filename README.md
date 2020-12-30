## TensorFlow Lite Micro Google examples

This repository, developed in collaboration between Antmicro and Google's TF Lite Micro team, is a work in progress but is ultimately meant to contain contains sources, tests, Google colabs and other material which use TF Lite Micro and Renode to enable easily running TF Lite Micro demos.

### Repo structure

* `.github/workflows` - GH actions files (currently only generating `ipynb` files from `py` sources)
* `notebooks` - Colabs (currently person detection nrf52840)
* `tensorflow` - example sources and Arduino lib, generated from the TF repository by a dedicated GH action [stored in a separate repo](https://github.com/antmicro/tensorflow-examples-generator)
