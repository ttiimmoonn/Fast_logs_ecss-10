<h1> Fast logs ECSS-10 </h1>
Python 3.5. or greater

<h2> [en] </h2>
A script for working log files from SSW ECSS-10 companies Eltex.
<h3> File structure </h3>
The script consists of three files:
<li> down_logs.py </li>
<li> custom_config.json </li>
<li> directory_structure.json </li>
<h4> down_logs </h4>
This file initializes the start of the script. The script at startup requires at least one argument:

<li> <code> -h </code>, <code> - help </code> Show help and exit. </li>
<li> <code> -c CUSTOM_CONFIG </code>, <code> - custom_config CUSTOM_CONFIG </code> The path to the custom_config file. If the path is not specified, then the file custom_config is searched in the local folder of the script. </li>
<li> <code> -arg_cl ARG_CLUSTERS [ARG_CLUSTERS ...] </code>, <code> - arg_clusters ARG_CLUSTERS [ARG_CLUSTERS ...] </code> The list of clusters from which the logs will be requested. </li>
<li> <code> -v </code>, <code> - vers_ecss_cluster </code> Request the current version of clusters in the ssw_version file. </li>
<li> <code> -z </code>, <code> - zip_arh </code> Pack logs to the archive. </li>
<li> <code> -cl </code>, <code> - clear_logs </code> Clear the current logs on the SSW. </li>

<h4> directory_structure </h4>
This file is in json format, where the directory structure of the SSW log file is stored. In this file, you can add your pointers to the log directory files that you want to retrieve from the SSW.

<h4> directory_structure </h4>
This is a json file that specifies the main SSW server configurations for the connection.

Also there is a path to the directory with log files, whose structure is represented in the file directory_structure and the path to the location of the log files on the local disk.
Naming fields.

<li> "%% EXTER_IP %%" - SSW IP address </li>
<li> "%% DEV_USER %%" is the name for authentication in the Cocon SSW shell </li>
<li> "%% DEV_PASS %%" - password for authorization in the Cocon SSW shell </li>
<li> "%% SSW_USER %%" is the name for authorization on the SSW server </li>
<li> "%% SSW_PASS %%" is the password for SSW authorization </li>
<li> "%% PATH_LOC_LOG %%" - path to the directory where the logs downloaded from SSW will be stored </li>
<li> %% PATH_REMOTE_LOG %% "- the path to the directory on the remote server where the SSW logs are stored </li>
<li> "%% PATH_DIR_STRUCT_LOG %% - path to file directory_structure </li>


<h2> [ru] </h2>
Скрипт для работы с log файлами SSW ECSS-10 компании Eltex.
<h3>Структура файлов</h3>
Скрипт состоит из трех файлов:
<li>down_logs.py</li>
<li>custom_config.json</li>
<li>directory_structure.json</li>
<h4>down_logs</h4>
Это файл инициализирует запуск скрипта. Скрипт при запуске требует хотя бы один аргумент:

<li> <code>-h</code>, <code>--help</code> Вывести помощь и выйти. </li>
<li> <code>-c CUSTOM_CONFIG</code>, <code>--custom_config CUSTOM_CONFIG</code> Путь до файла custom_config. Если путь не указан, то файл custom_config ищется в локальной папке скрипта. </li>
<li> <code>-arg_cl ARG_CLUSTERS [ARG_CLUSTERS ...]</code>, <code>--arg_clusters ARG_CLUSTERS [ARG_CLUSTERS ...]</code> Список кластеров с которых будут запрошены логи. </li>
<li> <code>-v</code>, <code>--vers_ecss_cluster</code> Запрашивать в файл ssw_version текущую версию кластеров. </li>
<li> <code>-z</code>, <code>--zip_arh</code> Упаковать логи в архив. </li>
<li> <code>-cl</code>, <code>--clear_logs</code> Отчистить текущие логи на SSW. </li>

<h4>directory_structure</h4>
Это файл в формате json, где хранится структура каталога лог файлов SSW. В этот файл можно добавить свои указатели на файлы директории логов, которые требуется получить с SSW.

<h4>directory_structure</h4>
Это файл в формате json, где указываются основные конфигурации сервера SSW для подключения. 

Также там указывается путь до каталога с лог файлами, структура которого представлена в файле directory_structure и путь до места хранения лог файлов на локальном диске.
Значащие поля. 

<li>"%%EXTER_IP%%" - IP адрес SSW</li> 
<li>"%%DEV_USER%%" - имя для авторизации в оболочке Cocon SSW</li>
<li>"%%DEV_PASS%%" - пароль для авторизации в оболочке Cocon SSW</li>
<li>"%%SSW_USER%%" - имя для авторизации на сервере SSW</li>
<li>"%%SSW_PASS%%" - пароль для авторизации на сервере SSW</li>
<li>"%%PATH_LOC_LOG%%" - путь до директории, где будут храниться логи загруженные с SSW</li>
<li>%%PATH_REMOTE_LOG%%" - путь до директории на удаленном сервере, где хранятся логи с SSW</li>
<li>"%%PATH_DIR_STRUCT_LOG%% - путь до файла directory_structure</li>

