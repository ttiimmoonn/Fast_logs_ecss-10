#!/usr/bin/env python3
import sys
import os
import datetime
import json
import logging
import argparse
import zipfile
import time
import paramiko
import scp 


date_start_test = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
FORMAT = '%(asctime)-15s %(message)s'
logger = logging.getLogger("logger")
logger.setLevel(logging.INFO)
logging.basicConfig(format=FORMAT)



def create_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--custom_config', type=str, required=False, help='The path to the custom_config file. If the path is not specified, then the file custom_config is searched in the local folder of the script.')
	parser.add_argument('-arg_cl', '--arg_clusters', type=str, nargs='+', required=False, help='The list of clusters from which the logs will be requested.')
	parser.add_argument('-v', '--vers_ecss_cluster', action='store_const', const=True, help='Request the current version of clusters in the ssw_version file.')
	parser.add_argument('-z', '--zip_arh', action='store_const', const=True, help='Pack logs to the archive.')
	parser.add_argument('-cl', '--clear_logs', action='store_const', const=True, help='Clear the current logs on the SSW.')
	return parser


	#Метод позволяет скачать с удаленного хоста, параметры которго заданные в host_data файлы по пути path_remote_log(из host_data)+path_remote
	#path_remote - список из путей к файлам, находящимся внутри dir ука//
	#path_remote_log - путь до паки, внутри которой требуется получить файлы указанные в path_remote//
	#host_data - словарь, где {"hostname":[адресс хоста], "username":[имя пользователя], "password":[пароль]}//
def dow_file(path_remote, path_remote_log, host_data):
	log_caunt_succ = 0
	log_caunt_fail = 0
	logger.info("An attempt was made to connect to the server for downloading files.")
	path_loc_log = host_data["%%PATH_LOC_LOG%%"]+ "/" + host_data["%%EXTER_IP%%"] + "/" + date_start_test
	if os.access(path_loc_log, os.F_OK) == False:
		os.makedirs(path_loc_log)
	client_ssh = paramiko.SSHClient()
	client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		client_ssh.connect(hostname=host_data["%%EXTER_IP%%"], username=host_data["%%SSW_USER%%"], password=host_data["%%SSW_PASS%%"])
		logger.info('Successful installation of connections to the server: Host Name: "{}"" IP: "{}"'.format(host_data["%%SSW_USER%%"], host_data["%%EXTER_IP%%"]))
	except Exception:
		logger.error("Сan not connect to the server:", host_data["%%EXTER_IP%%"])
		return False
	client_scp = scp.SCPClient(client_ssh.get_transport())
	for path in path_remote:
		os.makedirs(path_loc_log+path)
		logger.debug("Created a folder by path ", path_loc_log+path, os.access(path_loc_log+path, os.F_OK))
		try:
			client_scp.get(path_remote_log+path, path_loc_log+path)
			logger.debug("A file was successfully received along the path:", path_remote_log+path)
			logger.debug("The file was saved successfully:", path_loc_log+path)
			log_caunt_succ += 1
		except Exception:
			logger.error("Can not get file by path:{}".format(path_remote_log+path))
			log_caunt_fail += 1
	logger.info("Work with the server is completed. {} files are received. Failed to download {} files.".format(log_caunt_succ, log_caunt_fail))
	client_scp.close()
	client_ssh.close()
	return 1


# Достает кастомный конфиг 
def parser_custom_config(path_custom_config):
	logger.info("An attempt was made to parse the main configuration file.")
	try:
		with open(path_custom_config, 'r') as f:
		    data = json.loads(f.read())
	except ValueError:
		logger.error("Can not parse json file:{}".format(path_custom_config))
		return False
	except FileNotFoundError:
		logger.error("Can not open file:{}".format(path_custom_config))
		return False
	host_data = data["SystemVars"][0] 
	logger.info("Successfully.")
	return (host_data)


# Парсит json в формат пути
def parser_json(data, path = "/"):
	result = []
	if type(data) is list:
		for value in data:
			logger.debug("value form list = ", value)
			if type(value) is dict:
				path = path + value + "/"
				logger.debug("list is dict path = ", path)
				result += parser_json(value, path)

			if type(value) is list:
				path = path + value + "/"
				logger.debug("list is list path = ", path)
				result += parser_json(value, path)

			elif type(value) is str:
				result.append(path + value)
				logger.debug("list is str path = ", path +value)
		path = ""
	if type(data) is dict:
		for key, value in data.items():
			logger.debug("key form dicr = ", key)
			logger.debug("value form dicr = ", value)
			if type(value) is dict:
				path = path + key + "/"		
				logger.debug("dict is dict path = ", path)	
				result += parser_json(value, path)

			elif type(value) is list:
				path = path + key + "/"			
				logger.debug("dict is list path = ", path)			
				result += parser_json(value, path)

			elif type(value) is str:
				path = path + key + "/"
				result.append(path + value)
				logger.debug("list is str path = ", path +value)	
			path = "/"
	logger.debug("Result parser: ", result)
	return (result)


# достает json и отправляет в парсер
def parser_directory_structure(path_dir_str):
	logger.info("An attempt was made to parse the file with the directory structure of the requested files.")
	try:
		with open(path_dir_str, 'r') as f:
			try:
				data = json.loads(f.read())
			except ValueError:
				logger.error("Can not parse json file:{}".format(path_dir_str))
				return False
	except FileNotFoundError:
		logger.error("Can not open file:{}".format(path_dir_str))
		return False
	host_data = data["path_log_file"]
	path_log_file = parser_json(host_data)
	logger.info("Successfully.")
	return (path_log_file)


# Запрашивает на сервере список команд и возвращает в файл ssw_version.txt в папку с логами
# host_data - словарь, где {"%%EXTER_IP%%":[удаленный ip], %%SSW_USER%%:[имя пользователя], %%SSW_PASS%%:[пароль],//
# "%%PATH_LOC_LOG%%": [путь до файла с логами (локального)]} //
# command_list - список с командами //
def request_node_version(command_list, host_data, port_rm = 22):
	logger.info("An attempt was made to pass commands to the server.")
	path_loc_log = host_data["%%PATH_LOC_LOG%%"]+ "/" + host_data["%%EXTER_IP%%"] + "/" + date_start_test
	if os.access(path_loc_log, os.F_OK) == False:
		os.makedirs(path_loc_log)
	client_ssh = paramiko.SSHClient()
	client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#
	try:
		client_ssh.connect(hostname=host_data["%%EXTER_IP%%"], username=host_data["%%SSW_USER%%"], password=host_data["%%SSW_PASS%%"], port=port_rm)
	except Exception:
		logger.error("Сan not connect to the server:", host_data["%%EXTER_IP%%"])
		return False
	with client_ssh.invoke_shell() as ssh:
		for command in command_list:
			logger.debug("Remove command:", command)
			ssh.send(command + '\n')
			time.sleep(1)
			result = ssh.recv(10000).decode('utf-8')
			logger.debug("Path to ssw_version.txt: {}/ssw_version.txt".format(path_loc_log))
			with open("{}/ssw_version.txt".format(path_loc_log), 'a') as f:
					f.write(result + "\n")
					logger.debug("Write file")
			logger.debug("Close file.")
	#
		client_ssh.close()
	if os.access(path_loc_log, os.F_OK) == False:
		logger.error("Сan not edit file: {}/ssw_version.txt".format(path_loc_log))
	logger.info("Successfully.")
	return 1

'''
	for command in command_list:
		print (command)
		try:
			client_ssh.connect(hostname=host_data["%%EXTER_IP%%"], username=host_data["%%SSW_USER%%"], password=host_data["%%SSW_PASS%%"], port=port_rm)
		except Exception:
			logger.error("Сan not connect to the server:", host_data["%%EXTER_IP%%"])
			return False
		stdin, stdout, stderr = client_ssh.exec_command(command)
		print (stdout)
		logger.debug("Path to ssw_version.txt: {}/ssw_version.txt".format(path_loc_log))
		with open("{}/ssw_version.txt".format(path_loc_log), 'a') as f:
			for line in stdout:
				print (line)
				f.write('... ' + line.strip('\n') + "\n")
				print ("Записали в файл")
		print ("Закрыли файл")
'''


# Создаем архив с файлами логов
def archiving_log_files(host_data):
	logger.info("An attempt was made to archive log files.")
	path_loc_log = host_data["%%PATH_LOC_LOG%%"]+ "/" + host_data["%%EXTER_IP%%"] + "/" + date_start_test
	work_catalog = os.getcwd()
	os.chdir(path_loc_log)
	logger.debug("The working directory has been changed to path:", os.getcwd())
	ziph = zipfile.ZipFile("log_file_{}.zip".format(date_start_test),"a")
	for root, dirs, files in os.walk(path_loc_log):
		for file in files:
			path = "." + os.path.join(root, file)[len(path_loc_log):]
			if file not in "log_file_{}.zip".format(date_start_test):
				try:		
					ziph.write(path)
					logger.debug("The following file has been added to the archive:", path)
				except Exception:
					logger.error("Can not add file by path: ", path)
	ziph.close()		
	os.chdir(work_catalog)
	logger.debug("The working directory has been changed to path:", os.getcwd())
	logger.info("Successfully.")
	return 1


def add_path_bin():
	if not os.access("/usr/local/bin/down_logs", os.X_OK):
		a = "#!/bin/bash\ncd {0}\n{0}/down_logs.py $*".format(os.getcwd())
		with open("/usr/local/bin/down_logs", 'w') as f:
				f.write(a)
		os.chmod("/usr/local/bin/down_logs", 0o777)
		logger.info("Create a directory to quickly launch the script.")
	return 1



if __name__ == "__main__":


	#Создание объекта парсера аргументов из терминала
	arg_parser = create_parser()
	namespace = arg_parser.parse_args() 

	if namespace.custom_config:
		custom_config = parser_custom_config(namespace.custom_config)
	else:
		print (os.getcwd() + "/custom_config.json")
		custom_config = parser_custom_config(os.getcwd() + "/custom_config.json")


	#Отчистка логов на ssw и завершение скрипта
	if namespace.clear_logs:
		logger.info("An attempt was made to clear logs on the server.")
		request_node_version(["/node/clear-all-logs", "yes"], {"%%EXTER_IP%%":custom_config["%%EXTER_IP%%"],
 					"%%PATH_LOC_LOG%%":custom_config["%%PATH_LOC_LOG%%"], "%%SSW_USER%%":custom_config["%%DEV_USER%%"],
 					"%%SSW_PASS%%":custom_config["%%DEV_PASS%%"]}, 8023)
		sys.exit(0)

	#Массив путей из которых будет производиться загрузка логов
	directory_structure = parser_directory_structure(custom_config["%%PATH_DIR_STRUCT_LOG%%"])

	#Проверка указаны ли кластеры
	if namespace.arg_clusters:
		clast_lst = ""
		for name_lst in namespace.arg_clusters:
			clast_lst = clast_lst + " " + name_lst 	
		logger.info("Logs will be received for the following clusters: {}".format(clast_lst))
		new_dir_str = []
		for bn in namespace.arg_clusters:
			for an in directory_structure:
				if bn in an:
					new_dir_str.append(an)
		dow_file(new_dir_str, custom_config["%%PATH_REMOTE_LOG%%"], custom_config)
	else:
		dow_file(directory_structure, custom_config["%%PATH_REMOTE_LOG%%"], custom_config)

	#Добавляем файл с версиями кластеров SSW
	if namespace.vers_ecss_cluster:
		logger.info("Attempt to get information about the version of the cluster.")
		request_node_version(["/domain/list", 'cluster/adapter/sip1/sip/network/info'], {"%%EXTER_IP%%":custom_config["%%EXTER_IP%%"],
 					"%%PATH_LOC_LOG%%":custom_config["%%PATH_LOC_LOG%%"], "%%SSW_USER%%":custom_config["%%DEV_USER%%"],
 					"%%SSW_PASS%%":custom_config["%%DEV_PASS%%"]}, 8023)
		request_node_version(['dpkg -l | grep ecss'], custom_config)

	#Создаем архив с файлами логов
	if namespace.zip_arh:
		archiving_log_files(custom_config)

	#проверяем и если нет, создаем файл запуска скрипта по пути /usr/locate/bin
	add_path_bin()

