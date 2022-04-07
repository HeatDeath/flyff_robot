from flask import Flask, request

from load_yaml_conf import server_port, server_host, base_conf
from robot_utils import is_self_support_query_message, is_new_member_notice_message, handle_new_member_notice_event, \
    handle_self_query_event, do_answer_question

app = Flask(__name__)

notice_sync_group_ids = base_conf['notice_sync_group_ids']


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)

    if is_new_member_notice_message(data):
        handle_new_member_notice_event(data)
        return 'ok'

    if is_self_support_query_message(data):
        handle_self_query_event(data)
        return 'ok'

    return 'ok'


@app.route('/sync_game_notice', methods=["POST"])
def sync_game_notice():
    data = request.get_json()
    at_total_members = data['at_total_members']
    message = data['message']

    for group_id in notice_sync_group_ids:
        do_answer_question(group_id, '【游戏公告同步】' + message)

    return 'ok'


if __name__ == '__main__':
    app.run(host=server_host, port=server_port)
