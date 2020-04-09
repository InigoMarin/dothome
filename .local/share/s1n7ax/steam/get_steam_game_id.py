#!/bin/python

import os
import sys
import json
import urllib.request
import re
import subprocess

from pathlib import Path

#------------------------------------------------------------------------------#
#                                   VARIABLES                                  #
#------------------------------------------------------------------------------#
app_details_endpoint = 'https://api.steampowered.com/ISteamApps/GetAppList/v2'


"""
returns the configuration path for the scrpit
IF the dir doesn't exist, dir will be created
"""
def get_config_dir_path():
    conf_path = Path.joinpath(Path(os.environ['HOME']), Path('.config/steam-scripts'))
    conf_path.mkdir(parents=True, exist_ok=True)

    return conf_path

def create_file_if_not_exist(path):
    if not path.exists():
        with open(path, 'w', encoding='utf-8'): pass

def download_app_details():
    with urllib.request.urlopen(app_details_endpoint) as url:
        return json.loads(url.read().decode('utf-8'))
    
def get_history():
    history_path = Path.joinpath(get_config_dir_path(), Path('history.json'))
    create_file_if_not_exist(history_path)

    with open(history_path, 'r+', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as er:
            if 'Expecting value: line 1 column 1 (char 0)' not in str(er):
                raise Exception(er)

            data = json.loads('[]')
            json.dump(data, f)
            return data


def get_app_details():
    apps_path = Path.joinpath(get_config_dir_path(), Path('apps.json'))
    create_file_if_not_exist(apps_path)
    
    with open(apps_path, 'r+', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as e:
            print('requesting from endpoint')
            print(e)
            data = download_app_details()
            json.dump(data, f, ensure_ascii=False, indent=4)
            return data

def get_app_name_list():
    name_list = get_app_details()['applist']['apps']
    return [x.get('name')for x in name_list]

def add_history(history):
    history_path = Path.joinpath(get_config_dir_path(), Path('history.json'))

    data = None
    with open(history_path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read(), strict=False)

    data.append(history)

    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def run_app(id):
    subprocess.run(["steam", f"steam://run/{id}"])

def __main__():
    if sys.stdin.line_buffering is False:

        name = sys.stdin.readline().rstrip()

        # load all apps
        if 'Other' == name:
            for name in get_app_name_list():
                sys.stdout.write(name)
                sys.stdout.write("\n")
                
            sys.stdout.flush()
            return
        
        # load from history
        apps= [history for history in get_history() if history.get('name') == name]
        if len(apps) > 0:
            run_app(apps[0].get('appid'))
            return

        # load from all app
        appslist = get_app_details()['applist']['apps']
        apps = [x for x in appslist if x.get('name') == name]
        if(len(apps) > 0):
            add_history(apps[0])
            run_app(apps[0].get('appid'))
            return

    # display history list in first call
    historylist = [x.get('name') for x in get_history()]
    historylist.append('Other')
    for history in historylist:
        sys.stdout.write(history)
        sys.stdout.write('\n')
        sys.stdout.flush()


__main__()
