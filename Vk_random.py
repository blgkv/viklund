import time
import vk_api
import random
import json
import os
import sys
import getpass
import viklund

class Vk_random:
	def abort_random(self, item, flag):
		self.set_toggle_random(False)
		if flag == 0:
			viklund.Vk_messages.send_selective(item, 'msg', u'Что-то пошло не так. Убедитесь, что вы ввели оба числа.')
		else:
			viklund.Vk_messages.send_selective(item, 'msg', u'Рандом: отменено')
	def success_random(self, item):
		self.set_toggle_random(False)
		viklund.Vk_messages.send_selective(item, 'msg', u'Успешно! Ваше случайное число в диапазоне от ' + str(min(self.get_a(), self.get_b())) + u' до ' + str(max(self.get_a(), self.get_b())) + u': ' + str(self.get_result()))
	def find_a_b(self, recieved_str):
		self.set_a('')
		self.set_b('') 
		counter = 0
		for symbol in recieved_str:
			if '1234567890'.find(symbol) != -1:
				counter += 1
		if counter < 2:
			return -1
		else:
			got_a_flag = False
			got_b_flag = False
			digit_flag = False
			for symbol in recieved_str:
				if symbol.isdigit() and not got_a_flag and not got_b_flag:
					digit_flag = True
					self.set_a(self.get_a() + symbol)
				elif symbol.isdigit() and digit_flag and not got_a_flag and not got_b_flag:
					self.set_a(self.get_a() + symbol)
				elif not symbol.isdigit() and digit_flag and not got_a_flag and not got_b_flag:
					digit_flag = False
					got_a_flag = True
				elif symbol.isdigit() and not digit_flag and got_a_flag and not got_b_flag:
					digit_flag = True
					self.set_b(self.get_b() + symbol)
				elif symbol.isdigit() and digit_flag and not got_b_flag and got_a_flag:
					self.set_b(self.get_b() + symbol)
				elif not symbol.isdigit() and digit_flag and not got_b_flag and got_a_flag:
					digit_flag = False
					got_b_flag = True
					self.set_a(int(self.get_a))
					self.set_b(int(self.get_b))
		return 1

	def randint_wrapper(self, a, b):
		a = int(a)
		b = int(b)
		return random.randint(min(a,b), max(a,b))
	def set_a(self, value):	
		self.a = value
	def get_a(self):
		return self.a
	def set_b(self, value):
		self.b = value
	def get_b(self):
		return self.b
	def set_result(self, value):
		self.result = value
	def get_result(self):
		return self.result
	def set_toggle_random(self, value):
		self.toggle_random = value
	def get_toggle_random(self):
		return self.toggle_random
	def __init__(self):
		pass
	a = None
	b = None
	toggle_random = None
	result = None
