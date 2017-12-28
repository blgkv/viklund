"""
Copyright (C) 2017-2018 Artyom Bulgakov

This file is part of viklund.
Viklund is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Viklund is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with viklund.  If not, see <http://www.gnu.org/licenses/>.
"""

import vk_api
import json
import os
import errno
import sys
import getpass
import viklund
import argparse
from datetime import datetime


class System():
	@staticmethod
	def setup():
		"""
		step 1: parse args
		step 2: auth 
		step 3: create log folder and file
		step 4:	duplicate current process 
		step 5: override file descriptors to output logs to file
		step 6: get api access
		"""
		args = viklund.System.handle_args();
		viklund.vk = viklund.System.auth(args)
		log_file = viklund.Logging.initialize_logs()
		"""
		apparently most users may want to launch the bot in the terminal (e.g. ssh) and then close that terminal sessions
		but we don't want our process to be closed
		so we do auth procedure, clone process with fork() and exit the parent process
		even if user closes terminal, the server process will be alive
		"""
		pid = os.fork()
		success_message = viklund.Logging.success('Bot started with PID ' + str(pid))
		if pid: #parent process code goes here (pid > 0)
			#parent only shows success message and exits
			viklund.Logging.write_log(success_message)
			exit(0)
		else: #child process code goes here
			viklund.Vk_system.override_fd()
			viklund.Logging.write_log(success_message)
			viklund.vkApi = viklund.vk.get_api()	
	@staticmethod
	def handle_args():
		arg_parser = argparse.ArgumentParser()
		arg_parser.add_argument('-g', '--log', choices=['file', 'stdout',], default='file', type=str, action='store', help='select log type') #select logs output type
		arg_parser.add_argument('-l', '--login', nargs='?', type=str, action='store', help='input login, UNSAFE, USE CAREFULLY') #
		arg_parser.add_argument('-p', '--password', nargs='?', type=str, action='store', help='input password, UNSAFE, USE CAREFULLY')
		arg_parser.add_argument('-j', '--json_path', nargs='?', type=str, action='store', help='Path to .json file, needed for group post import, example: /path/to/file.json')
		args_namespace = arg_parser.parse_args(sys.argv[1:])
		if args_namespace.json_path:
			viklund.JSON_PATH = args_namespace.json_path
		else:
			viklund.JSON_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/default.json'
		log_file = None
		return args_namespace

	@staticmethod
	def auth(args_namespace):
		vk = None
		print('Viklund v.0.5')
		#if user haven't provided login as commandline argument, ask him for login
		#otherwise, we'll just copy login from namespace variable to local variable
		if not args_namespace.login: 
			vk_login = input('Login:')
		else:
			vk_login = args_namespace.login
		#same for password
		if not args_namespace.password:
			vk_passwd = getpass.getpass('Password:')
		else:
			vk_passwd = args_namespace.password
		try:
			#get VK API access
			vk = vk_api.VkApi(login = vk_login, password = vk_passwd)
			vk.auth()
			del vk_login; del vk_passwd; del args_namespace #it might be safer to delete import variables manually
		except vk_api.AuthError as error_msg:
			viklund.Logging.write_log(Logging.error('Unable to log in. Please check that you have entered your login and password correctly.'))
			exit(1)
		else:
			viklund.Logging.write_log(Logging.success("Auth successful"))
		return vk