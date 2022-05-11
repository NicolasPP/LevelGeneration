import time

def time_func(func):
	def wrapper(*args, **kwargs):
		start = time.time()
		func(*args, **kwargs)
		duration = time.time() - start
		duration = round(duration, 3)
		print(f'{func.__name__} : {duration}')
	wrapper.__name__ = func.__name__
	return wrapper