# Generic imports
import os
from datetime import datetime
from dotenv import load_dotenv

# Local imports
from utils.logger import Logger

# Globals
logger = Logger({"filepath": "logs/test.log", "level": "DEBUG"})


# Example type annotations and docstrings
def sum(a: int, b: int) -> int:
	'''
	Sum two integers
	:param a: First integer
	:param b: Second integer
	:return: Summed value
	
	Example:
	>>> sum(1, 2)
	3
	'''
	return a + b


def get_time() -> datetime:
	return datetime.now()


def test_env():
	# NOTE: This is just a demonstration of how to use dotenv
	#       Never store sensitive information in code or in the repository
	path = "sample.env"
	load_dotenv(dotenv_path=path)
	print(f"SOME_VARIABLE: {os.getenv('SOME_VARIABLE')}")


def test_logger():
	logger.info("INFO message 1")
	logger.debug("DEBUG message 1")
	logger.warning("WARNING message 1")
	logger.error("ERROR message 1")


def main():
	print(f"Time is {get_time()}")
	print(f"Sum of {1} and {2} is {sum(1, 2)}")
	test_env()
	test_logger()


if __name__ == "__main__":
	main()
	logger.info("All done!")
	logger.stop()  # usually not needed - just here for demonstration
