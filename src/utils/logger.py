import os
import logging
import json
from typing import Optional


# Terminal colors
class TC:
	# Colors
	RED = "\033[91m"
	GREEN = "\033[92m"
	YELLOW = "\033[93m"
	BLUE = "\033[94m"
	CYAN = "\033[96m"
	MAGENTA = "\033[95m"
	# Aliases
	RESET = "\033[0m"
	INFO = RESET
	DEBUG = CYAN
	WARNING = YELLOW
	ERROR = RED
	CRITICAL = MAGENTA


def get_logger(options: dict) -> logging.Logger:
	if "filepath" not in options:
		raise Exception("Missing filepath in options")

	if not os.path.exists(os.path.dirname(options["filepath"])):
		os.makedirs(os.path.dirname(options["filepath"]))

	# Return the logger if it already exists to prevent duplicate handlers
	if logging.getLogger(options["filepath"]).hasHandlers():
		return logging.getLogger(options["filepath"])

	if "level" not in options:
		options["level"] = "INFO"

	if "formatter" not in options:
		options["formatter"] = logging.Formatter(
		    '%(asctime)s.%(msecs)03d %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

	handler = logging.FileHandler(options["filepath"],
	                              mode="a+",
	                              encoding="utf-8")
	handler.setFormatter(options["formatter"])

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(options["formatter"])

	logger = logging.getLogger(options["filepath"])
	logger.propagate = False
	logger.setLevel(options["level"])

	if not logger.hasHandlers():
		logger.addHandler(handler)
		logger.addHandler(console_handler)

	options["fmt"] = options["formatter"]._fmt
	options["datefmt"] = options["formatter"].datefmt

	logger.info("=" * 60)
	logger.info(
	    f"Starting logger with options: {json.dumps(options, indent=2, sort_keys=True, default=str)}"
	)
	return logger


def stop_logger(logger: logging.Logger):
	for handler in logger.handlers[:]:
		try:
			handler.close()
			logger.removeHandler(handler)
		except Exception as e:
			print(f"Exception while closing logger handler: {e}")


def say(message: str, logger: logging.Logger, level: Optional[str] = "INFO"):
	if level is None:
		level = "INFO"
	level = level.upper()

	log_methods = {
	    "INFO": logger.info,
	    "DEBUG": logger.debug,
	    "WARNING": logger.warning,
	    "ERROR": logger.error,
	    "CRITICAL": logger.critical,
	}

	log_colors = {
	    "INFO": TC.INFO,
	    "DEBUG": TC.DEBUG,
	    "WARNING": TC.WARNING,
	    "ERROR": TC.ERROR,
	    "CRITICAL": TC.CRITICAL,
	}

	color = log_colors.get(level, TC.INFO)
	log_method = log_methods.get(level, logger.info)
	log_method(f" {color}{level.rjust(8)}{TC.RESET}  {message}")


def test_get_logger():
	options = {
	    "filepath":
	        "logs/test.log",
	    "level":
	        "DEBUG",
	    "formatter":
	        logging.Formatter(
	            '%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
	            datefmt='%Y-%m-%dT%H:%M:%S')
	}
	logger = get_logger(options)
	logger.info("(LOGGER 1) INFO message")
	logger.debug("(LOGGER 1) DEBUG message")
	# only need to stop the logger when you're done with the logger and want to reuse it (in the same file)
	stop_logger(logger)
	logger = get_logger({"filepath": "logs/test.log"})
	logger.info("(LOGGER 2) INFO message")
	logger.debug("(LOGGER 2) DEBUG message (option 2)")


def test_say():
	logger = get_logger({"filepath": "logs/test.log", "level": "DEBUG"})
	say("(SAY) INFO message 1", logger)
	say("(SAY) INFO message 2", logger, "INFO")
	say("(SAY) DEBUG message", logger, "DEBUG")
	say("(SAY) WARNING message", logger, "WARNING")
	say("(SAY) ERROR message", logger, "ERROR")
	say("(SAY) CRITICAL message", logger, "CRITICAL")


class Logger():
	'''Logger class that wraps the logger and provides a methods for convenience'''

	def __init__(self, options: dict):
		# pass in "typeinit" to skip the init
		# (useful when you want to set it as a placeholder variable so that type hinting works)
		if "typeinit" in options:
			return
		self.options = options
		self.logger = get_logger(options)

	def say(self, message: str, level: Optional[str] = "INFO"):
		say(message, self.logger, level)

	def info(self, message: str):
		self.say(message, "INFO")

	def error(self, message: str):
		self.say(message, "ERROR")

	def debug(self, message: str):
		self.say(message, "DEBUG")

	def warning(self, message: str):
		self.say(message, "WARNING")

	def critical(self, message: str):
		self.say(message, "CRITICAL")

	def stop(self):
		stop_logger(self.logger)

	# def __del__(self):
	# 	self.stop()


def test_Logger():
	logger = Logger({"filepath": "logs/test.log", "level": "DEBUG"})
	logger.say("(LOGGER) INFO message 1")
	logger.say("(LOGGER) INFO message 2", "INFO")
	logger.say("(LOGGER) DEBUG message", "DEBUG")
	logger.say("(LOGGER) WARNING message", "WARNING")
	logger.say("(LOGGER) ERROR message", "ERROR")
	logger.say("(LOGGER) CRITICAL message", "CRITICAL")
	logger.stop()
	logger = Logger({"filepath": "logs/test.log"})
	logger.say("(LOGGER 2) INFO message 1")
	logger.say("(LOGGER 2) INFO message 2", "INFO")
	logger.say("(LOGGER 2) DEBUG message", "DEBUG")
	logger.say("(LOGGER 2) WARNING message", "WARNING")
	logger.say("(LOGGER 2) ERROR message", "ERROR")
	logger.say("(LOGGER 2) CRITICAL message", "CRITICAL")
	logger.stop()
	logger = Logger({"filepath": "logs/test.log", "level": "DEBUG"})
	logger.say("(LOGGER 3) SAY message 1")
	logger.info("(LOGGER 3) INFO message 1")
	logger.debug("(LOGGER 3) DEBUG message 1")
	logger.warning("(LOGGER 3) WARNING message 1")
	logger.error("(LOGGER 3) ERROR message 1")
	logger.critical("(LOGGER 3) CRITICAL message 1")
	logger.info("")
	logger2 = Logger({"filepath": "logs/test.log", "level": "DEBUG"})
	logger2.say("(LOGGER 4) Testing reusing logger")
	red_text_start = "\033[91m"
	reset_text = "\033[0m"
	logger2.say(
	    f"{red_text_start}(LOGGER 4) This message should be red{reset_text}",
	    "ERROR")
	logger.say("(LOGGER 3) INFO message 2")


if __name__ == "__main__":
	# print(f"Testing get_logger()")
	# test_get_logger()
	# print(f"Testing say()")
	# test_say()
	print(f"Testing Logger()")
	test_Logger()
	print("ALL DONE")
