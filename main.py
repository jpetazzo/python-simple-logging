#!/usr/bin/env python
import logging
import logging.config
import mylib
import requests

### Default config: get WARNING and above
#logging.basicConfig()

### The basic firehose (give me ALL THE THINGS!)
#logging.basicConfig(level=logging.DEBUG)

### The basic firehose (give me ALL THE THINGS!)
#logging.basicConfig(level=logging.DEBUG)

### Basic firehose with timestamps, file names, line numbers
#logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(filename)s:%(lineno)d:%(message)s', level=logging.DEBUG)

### Selectively enabling the firehose for our lib
#logging.basicConfig()
#logging.getLogger("mylib").setLevel(logging.DEBUG)

### Selectively enabling the firehose for urllib3
# (and all the loggers below it, including urrlib3.connectionpool)
#logging.basicConfig()
#logging.getLogger("urllib3").setLevel(logging.DEBUG)

### If we don't configure logging at all (if we leave all the basicConfig calls
### commented out), we'll only get WARNING logs, and without formatting.

# this will generate some INFO and DEBUG logs
mylib.do_stuff()

# this will also generate a WARNING
mylib.do_stuff(0)

# and this will generate logs in a different logger
# (urllib3.connectionpool)
requests.get("https://1.1.1.1")
