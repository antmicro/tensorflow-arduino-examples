# %% [markdown]
"""
![Renode](https://antmicro.com/OpenSource/assets/images/projects/renode.png)
"""

# %% [markdown]
"""
## Install requirements
"""

# %%
!pip install -q git+https://github.com/antmicro/pyrenode.git git+https://github.com/antmicro/renode-colab-tools.git Pillow
!rm -rf renode-tflite-nrf52840-person-detection renode
!git clone --quiet https://github.com/antmicro/renode-tflite-nrf52840-person-detection.git
!mkdir -p renode && cd renode && tar -xzf ../renode-tflite-nrf52840-person-detection/renode-1.11.0.linux-portable.tar.gz --strip 1
!pip install -q -r renode/tests/requirements.txt

import os
from renode_colab_tools import *
os.environ['PATH'] = os.getcwd()+"/renode:"+os.environ['PATH']

# %%
!mkdir -p binaries/person_detection && cd binaries/person_detection && wget https://github.com/antmicro/tensorflow-arduino-examples-binaries/raw/master/person_detection/person_detection.ino.elf # fetch prebuilt binaries

# %% [markdown]
"""## Take a photo"""

# %%
from IPython.display import Image
photo = take_photo()
display(Image(photo))

# %% [markdown]
"""## Convert the photo, required size < 4096 bytes"""

# %%
from PIL import Image
image = Image.open('photo.jpg')
image.thumbnail((120, 120))
image.save('photo.jpg')

# %% [markdown]
"""## Run a person-detection example with a captured photo in Renode"""

# %%
import time
from pyrenode import *
shutdown_renode()
connect_renode() # this sets up a log file, and clears the simulation (just in case)
tell_renode('using sysbus')
tell_renode('mach create')
tell_renode('machine LoadPlatformDescription @/content/renode-tflite-nrf52840-person-detection/nrf52840.repl')
tell_renode('sysbus LoadELF @/content/binaries/person_detection/person_detection.ino.elf')

tell_renode('uart0 CreateFileBackend @uart.dump true')
tell_renode('logLevel 3')
tell_renode('spi2.camera ImageSource @/content/photo.jpg')
tell_renode('machine EnableProfiler "metrics.dump"')
tell_renode('s')
time.sleep(5) #waits for creating uart.dump
!timeout 60 tail -c+2 -f renode/uart.dump | sed '/^Person score: .*$/ q'
tell_renode('q')
expect_cli('Renode is quitting')
shutdown_renode()

# %% [markdown]
"""## Renode metrics analysis"""

# %%
from renode.tools.metrics_analyzer.metrics_parser import MetricsParser
init_notebook_mode(connected=False)
parser = MetricsParser('renode/metrics.dump')

# %%
configure_plotly_browser_state()
show_executed_instructions(parser)

# %%
configure_plotly_browser_state()
show_memory_access(parser)

# %%
configure_plotly_browser_state()
show_exceptions(parser)