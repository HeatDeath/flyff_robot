import json
import os

import yaml

cur_path = os.path.dirname(os.path.realpath(__file__))
yaml_path = os.path.join(cur_path, "answer_conf.yaml")

keyword_2_instance_dict = {}
alias_2_keyword_dict = {}


class AnswerConf:
    def __init__(self, keyword, category, alias, content, urls):
        self.keyword = keyword
        self.category = category
        self.alias = alias
        self.content = content
        self.urls = urls


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
