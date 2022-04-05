import requests
from flask import Flask, request

from load_yaml_conf import keyword_2_instance_dict, alias_2_keyword_dict, server_port, server_host, qq_proxy_port, \
    qq_proxy_host, base_conf
from robot_utils import is_self_support_query_message, is_new_member_notice_message

app = Flask(__name__)

concerned_group_ids = base_conf['concerned_group_ids']
notice_sync_group_ids = base_conf['notice_sync_group_ids']

qq_proxy_url = qq_proxy_host + ':' + str(qq_proxy_port)
myself_qq_id = str(base_conf['myself_qq_id'])


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)

    if is_self_support_query_message(data):
        handle_self_query_event(data)
        return 'ok'

    if is_new_member_notice_message(data):
        handle_new_member_notice_event(data)
        return 'ok'

    return 'ok'


def handle_new_member_notice_event(data):
    self_id = data['self_id']
    group_id = data['group_id']

    do_answer_question(group_id, '欢迎新人')


def handle_self_query_event(data):
    self_id = data['self_id']
    user_id = data['user_id']
    message_id = data['message_id']
    message = data['message']
    raw_message = data['raw_message']
    group_id = data['group_id']

    message = message.split(' ')[1]
    print("message after split, message=" + message)

    if message == '帮助':
        payload = {
            'group_id': group_id,
            'message': '目前支持查询的关键词如下' + str([i for i in keyword_2_instance_dict.keys()]),
            'auto_escape': True
        }
        requests.post(qq_proxy_url + "/send_group_msg", payload)
        return 'ok'

    if message not in alias_2_keyword_dict.keys():
        print("message=" + message)
        print("not find alias in alias_2_keyword_dict")
        return 'continue'

    do_answer_question(group_id, message)


def do_answer_question(group_id, message):
    keyword = alias_2_keyword_dict[message]
    answer_conf = keyword_2_instance_dict[keyword]

    final_url = ""
    if answer_conf.urls is not None and len(answer_conf.urls) > 0:
        for url in answer_conf.urls:
            final_url = final_url + url + "\n"

    if len(final_url) != 0:
        answer_message = answer_conf.content + "\n" + final_url
    else:
        answer_message = answer_conf.content

    payload = {
        'group_id': group_id,
        'message': answer_message,
        'auto_escape': True
    }

    requests.post(qq_proxy_url + "/send_group_msg", payload)

    return 'ok'


@app.route('/sync_game_notice', methods=["POST"])
def sync_game_notice():
    data = request.get_json()
    at_total_members = data['at_total_members']
    message = data['message']

    for group_id in notice_sync_group_ids:
        payload = {
            'group_id': group_id,
            'message': '【游戏公告同步】' + message,
            'auto_escape': True
        }

        requests.post(qq_proxy_url + "/send_group_msg", payload)

    return 'ok'


if __name__ == '__main__':
    app.run(host=server_host, port=server_port)
