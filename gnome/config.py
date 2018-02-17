
import configparser
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .event import ShellCommandEventHandler
from . import logging

class Config:
    def __init__(self, path):
        self.path = path

    def parse_section(self, title, values) -> list:
        " Parse a section and return a configured list of observers "
        assert "cmd" in values

        cwd = os.path.join(os.getcwd(), values.get("cwd", "."))
        regexes = values.get("patterns", "").split(",")
        ignored_patterns =values.get("ignore_patterns")
        ignore_regexes = ignored_patterns.split(",") if ignored_patterns else []
        recursive = values.get("recursive", True)

        logging.debug(
            "[%(title)s] Watching %(patterns)s and ignoring %(ignore_patterns)s in %(cwd)s" % {
                "title": title,
                "patterns": regexes,
                "ignore_patterns": ignore_regexes,
                "cwd": cwd,
            }
        )

        event_handler = ShellCommandEventHandler(
            title,
            cmd=values.get("cmd"),
            regexes=regexes,
            ignore_regexes=ignore_regexes,
            ignore_directories=True)

        observer = Observer()
        observer.schedule(event_handler, cwd, recursive=recursive)
        yield observer

    def parse(self) -> list:
        """
        Returns a list of configured observers

        Dependihg on the parameter of the sections,
        see parse section for the detail of how this is
        this detailed
        """
        config = configparser.RawConfigParser()
        config.read(self.path)
        sections = config.sections()
        try:
            for section in sections:
                yield from self.parse_section(section, dict(config.items(section)))
        except AssertionError as e:
            logging.error(e)
            exit(1)
