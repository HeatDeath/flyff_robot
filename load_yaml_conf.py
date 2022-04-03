import json
import os

import yaml

cur_path = os.path.dirname(os.path.realpath(__file__))

keyword_2_instance_dict = {}
alias_2_keyword_dict = {}

server_host = ''
server_port = ''

qq_proxy_host = ''
qq_proxy_port = ''

base_conf = {}


class AnswerConf:
    def __init__(self, keyword, category, alias, content, urls):
        self.keyword = keyword
        self.category = category
        self.alias = alias
        self.content = content
        self.urls = urls


yaml_path = os.path.join(cur_path, "answer_conf.yaml")
with open(yaml_path, 'r', encoding='utf-8') as f:
    config = f.read()
    answer_conf_list = yaml.load(config, Loader=yaml.FullLoader)

    for answer_conf in answer_conf_list:
        answer_conf_instance = AnswerConf(answer_conf['keyword'], answer_conf['category'], answer_conf['alias'],
                                          answer_conf['content'], answer_conf['urls'])
        keyword_2_instance_dict[answer_conf['keyword']] = answer_conf_instance
        for alias in answer_conf['alias']:
            alias_2_keyword_dict[alias] = answer_conf['keyword']

    json_str = json.dumps(alias_2_keyword_dict, ensure_ascii=False)
    print(json_str)

yaml_path = os.path.join(cur_path, "base_conf.yaml")
with open(yaml_path, 'r', encoding='utf-8') as f:
    config = f.read()
    base_conf_dict = yaml.load(config, Loader=yaml.FullLoader)
    server_host = base_conf_dict['server_host']
    server_port = base_conf_dict['server_port']

    qq_proxy_host = base_conf_dict['qq_proxy_host']
    qq_proxy_port = base_conf_dict['qq_proxy_port']
    print(server_host + ':' + str(server_port))
    print(qq_proxy_host + ':' + str(qq_proxy_port))

    base_conf = base_conf_dict
