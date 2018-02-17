import sys
import time
from .config import Config
from . import logging
def main():
    if True:
        logging.setLevel(logging.DEBUG)
    else:
        logging.setLevel(logging.WARNING)
    conf_file = sys.argv[1] if len(sys.argv) > 1 else None
    config = Config(conf_file)

    observers = list(config.parse())
    for observer in observers:
        observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for o in observers:
            o.unschedule_all()
            o.stop()
    for o in observers:
        o.join()

if __name__ == "__main__":
    main()
