""" --------------------------------------
Filename: config.py
Description: configs parser
Author: hexsix
Date: 2020/12/21
-------------------------------------- """

import os

from configparser import ConfigParser, NoOptionError, NoSectionError


def get_configs() -> dict:
    here = os.path.dirname(__file__)
    ini_path = os.path.join(here, 'config.ini')
    try:
        assert os.path.exists(ini_path)
    except AssertionError:
        print('config.ini not found, '
              '\'cp config_sample.ini config.ini\''
              'then edit the config.ini'
              )
        exit(1)

    config = ConfigParser()
    config.read(ini_path)
    _configs = {}
    section_option = {
        "mirai_http": ['qq', 'authKey', 'port'],
        "dir": ['program_dir', 'img_dir'],
        "rss": ['rss_url'],
        "bot": ['allowedGroups']
    }
    for section in section_option:
        for option in section_option[section]:
            try:
                _configs[option] = config.get(section, option)
            except NoSectionError as e:
                print(e)
                print('please check your config.ini')
                exit(1)
            except NoOptionError as e:
                print(e)
                print('please check your config.ini')
                exit(1)
    # qq
    try:
        _configs['qq'] = int(_configs['qq'])
    except ValueError:
        print('your qq number should be int\n'
              'please check your config.ini')
        exit(1)
    # allowedGroups
    try:
        _configs['allowedGroups'] = [int(group) for group in _configs['allowedGroups'].split(',')]
    except ValueError:
        print('your group number should be int\n'
              'and each group number should be sep by a single comma\n'
              'please check your config.ini')
        exit(1)
    # dir configs
    # 1. program_dir
    if not _configs['program_dir']:
        _configs['program_dir'] = here
    # 2. img_dir
    if not _configs['img_dir']:
        _configs['img_dir'] = os.path.join(_configs['program_dir'], 'imgs')
    if not os.path.exists(_configs['img_dir']):
        os.mkdir(_configs['img_dir'])
    # 3. persist_dir
    persist_dir = os.path.join(_configs['program_dir'], 'persist_files')
    if not os.path.exists(persist_dir):
        os.mkdir(persist_dir)
    # 3.1 saved_list
    _configs['saved_list'] = os.path.join(persist_dir, 'saved_list.txt')
    if not os.path.exists(_configs['saved_list']):
        os.mknod(_configs['saved_list'])
    # 3.2 sent_list
    _configs['sent_list'] = os.path.join(persist_dir, 'sent_list.txt')
    if not os.path.exists(_configs['sent_list']):
        os.mknod(_configs['sent_list'])
    # 3.3 error_list
    _configs['error_list'] = os.path.join(persist_dir, 'error_list.txt')
    if not os.path.exists(_configs['error_list']):
        os.mknod(_configs['error_list'])
    # 4. temp_images dir
    _configs['temp_imgs'] = os.path.join(_configs['program_dir'], 'temp_imgs')
    if not os.path.exists(_configs['temp_imgs']):
        os.mkdir(_configs['temp_imgs'])

    return _configs


configs = get_configs()


if __name__ == '__main__':
    print(configs)
