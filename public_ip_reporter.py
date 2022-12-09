import requests
import json
import os
import platform
import yaml
import time
import re
from datetime import datetime


current_directory = os.getcwd()
config_file = 'config.yml'


def load_config(yaml_to_load):
	with open(yaml_to_load, 'rt') as f:
		config_file = yaml.load(f, Loader=yaml.FullLoader)
	return config_file


config_data = load_config(config_file)
log_file = config_data['log_file_name_with_extension']
api_url = config_data['telegram_api_url']
token = config_data['telegram_token']
chat_id = config_data['telegram_chat_id']
ip_url = config_data['ip_address_url']
location_url = config_data['ip_address_location_url']
country_code = config_data['country_code']
os_type = platform.system()
slash = '\\' if os_type == 'Windows' else '/'
log_file_path = f"{current_directory}{slash}{log_file}"


def logger(text, file_path=log_file_path):
    current_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    log_message = "{} - {}".format(current_time,text)
    with open(file_path,'at') as log_file:
        log_file.write(log_message + '\n')


def send_msg(msg, tg_token=token, tg_chat_id=chat_id):
    try:
        requests.get(f'{api_url}{tg_token}/sendMessage?chat_id={tg_chat_id}&text={msg}')
    except Exception as e:
        error_msg = f"Error sending alert to telegram: {e}"
        logger(error_msg)


def get_ip(url=ip_url):
    try:
        response = requests.get(url).json()
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",response["ip"]):
            send_msg(f"Invalid IP - {response['ip']} - was obtained from {url}")
            raise ValueError(f"{response['ip']} is an invalid IP address")
        return response["ip"]
    except Exception as e:
        error_msg = f"Error getting IP address: {e}"
        logger(error_msg)
	

def get_ip_location(url=location_url):
    ip_address = get_ip()
    full_location_url = f"{url}{ip_address}"
    try:
        response = requests.get(full_location_url)
        interim_result = response.content.decode()
        result = interim_result.split("(")[1].strip(")")
        return json.loads(result)
    except Exception as e:
        error_msg = f"Error getting IP address location: {e}"
        logger(error_msg)


def main():
    while True:
        time.sleep(3)
        location_info = get_ip_location()
        ip_v4 = location_info['IPv4']
        actual_code = location_info['country_code']
        if actual_code == country_code: continue
        alert = f"Public IP - {ip_v4} is NOT from {country_code}. Detected country - {actual_code}!!!"
        send_msg(alert)


if __name__ == '__main__':
    main()