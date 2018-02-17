import subprocess
from watchdog.events import RegexMatchingEventHandler
from . import logging

class ShellCommandEventHandler(RegexMatchingEventHandler):
    def __init__(self, title, cmd="echo %(filename)s", *args, **kwargs):
        self.title = title
        self._cmd = cmd
        super().__init__(*args, **kwargs)

    def execute_action(self, filename):
        full_command = self._cmd % {"filename": filename}
        return_code = subprocess.call(full_command, shell=True)

    def on_modified(self, event):
        logging.debug(
            "[%(title)s] File modified %(file)s" % {
                "title": self.title,
                "file": event.src_path,
            }
        )
        self.execute_action(event.src_path)

    def on_created(self, event):
        logging.debug(
            "[%(title)s] File created %(file)s" % {
                "title": self.title,
                "file": event.src_path,
            }
        )
        self.execute_action(event.src_path)
