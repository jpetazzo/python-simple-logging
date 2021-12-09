import logging
import time


log = logging.getLogger(__name__)


def do_stuff(how_long=1, update_interval=0.3):
  log.info("starting to do stuff")
  if how_long==0:
    log.warning("actually doing nothing")
  end_time = time.time() + how_long
  while time.time() < end_time:
    time.sleep(update_interval)
    log.debug("still doing stuff")
  log.info("did some stuff")

