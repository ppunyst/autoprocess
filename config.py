import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(levelname)s:%(asctime)s: %(message)s', '%m/%d/%Y %I:%M:%S %p')
error_formatter = logging.Formatter('%(levelname)s:%(asctime)s: %(message)s\n\tFile "%(pathname)s", Line %(lineno)d, in %(funcName)s', '%m/%d/%Y %I:%M:%S %p')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

file_error_handler = logging.FileHandler('error.log')
file_error_handler.setLevel(logging.ERROR)
file_error_handler.setFormatter(error_formatter)
logger.addHandler(file_error_handler)