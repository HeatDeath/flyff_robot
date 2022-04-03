import requests
from flask import Flask, request

from load_yaml_conf import keyword_2_instance_dict, alias_2_keyword_dict

app = Flask(__name__)

white_group_id_set = [818206909]
# myself_qq_id = '1438560198'
myself_qq_id = '847236448'


@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    print(data)

    if 'message_type' not in data:
        print("not target message")
        return 'continue'

    if data["message_type"] != "group":
        print("not group message")
        return "continue"

    if data['group_id'] not in white_group_id_set:
        print("not target group")
        return 'continue'

    if 'CQ:at' not in data['message']:
        print("not at me")
        return 'continue'

    if myself_qq_id not in data['message']:
        print("not at me")
        return 'continue'

    self_id = data['self_id']
    user_id = data['user_id']
    message_id = data['message_id']
    message = data['message']
    raw_message = data['raw_message']

    message = message.split(' ')[1]
    print("message after split, message=" + message)

    if message not in alias_2_keyword_dict.keys():
        print("message=" + message)
        print("not find alias in alias_2_keyword_dict")
        return 'continue'

    keyword = alias_2_keyword_dict[message]
    answer_conf = keyword_2_instance_dict[keyword]

    final_url = ""
    if answer_conf.urls is not None and len(answer_conf.urls) > 0:
        for url in answer_conf.urls:
            final_url = final_url + url + ","

    answer_message = answer_conf.content + "\n" + final_url

    payload = {
        'group_id': 818206909,
        'message': answer_message,
        'auto_escape': True
    }

    requests.post("http://127.0.0.1:5700/send_group_msg", payload)

    return 'ok'


@app.route('/sync_game_notice', methods=["POST"])
def sync_game_notice():
    data = request.get_json()
    print(data)


if __name__ == '__main__':
    # 此处的 host和 port对应上面 yml文件的设置
    app.run(host='127.0.0.1', port=5701)  # 保证和我们在配置里填的一致
