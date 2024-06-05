# Generic imports
from datetime import datetime

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


def test_logger():
	logger.info("INFO message 1")
	logger.debug("DEBUG message 1")
	logger.warning("WARNING message 1")
	logger.error("ERROR message 1")


def main():
	print(f"Time is {get_time()}")
	print(f"Sum of {1} and {2} is {sum(1, 2)}")
	test_logger()


if __name__ == "__main__":
	main()
	logger.info("All done!")
	logger.stop()  # usually not needed - just here for demonstration
