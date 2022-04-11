from random import choice

import requests

from load_yaml_conf import qq_proxy_port, qq_proxy_host, base_conf, alias_2_keyword_dict, \
    keyword_2_instance_dict, keyword_2_contents_dict_for_easter_egg, alias_2_keyword_dict_for_easter_egg

concerned_group_ids = base_conf['concerned_group_ids']
notice_sync_group_ids = base_conf['notice_sync_group_ids']

myself_qq_id = str(base_conf['myself_qq_id'])
qq_proxy_url = qq_proxy_host + ':' + str(qq_proxy_port)


# 检查是否是自助查询消息
def is_self_support_query_message(data):
    if 'message_type' not in data:
        print("not target message")
        return False

    if data["message_type"] != "group":
        print("not group message")
        return False

    if data['group_id'] not in concerned_group_ids:
        print("not target group")
        return False

    if 'CQ:at' not in data['message']:
        print("not at me")
        return False

    if myself_qq_id not in data['message']:
        print("not at me")
        return False

    return True


# 检查是否是新成员加入消息
def is_new_member_notice_message(data):
    if 'post_type' not in data:
        print("not target message")
        return False

    if data["post_type"] != "notice":
        print("not notice message")
        return False

    if 'notice_type' not in data:
        print("not target message")
        return False

    if data["notice_type"] != "group_increase":
        print("not group_increase message")
        return False

    if data['group_id'] not in concerned_group_ids:
        print("not target group")
        return False

    return True


# 处理新成员加入通知事件
def handle_new_member_notice_event(data):
    group_id = data['group_id']
    do_answer_question(group_id, '欢迎新人')


# 发送q群消息
def post_group_message(group_id, message):
    payload = {
        'group_id': group_id,
        'message': message,
        'auto_escape': True
    }

    requests.post(qq_proxy_url + "/send_group_msg", payload)


# 回答自助查询问题
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

    post_group_message(group_id, answer_message)

    return 'ok'


# 发送彩蛋
def do_send_easter_egg(group_id, message):
    keyword = alias_2_keyword_dict_for_easter_egg[message]
    content_list = keyword_2_contents_dict_for_easter_egg[keyword]
    post_group_message(group_id, choice(content_list))
    return 'ok'


# 处理自助查询事件
def handle_self_query_event(data):
    origin_message = data['message']
    group_id = data['group_id']

    message = origin_message.split(' ')[1]
    print("message after split, message=" + message)

    if message == '帮助':
        answer_message = '目前支持查询的关键词如下' + str([i for i in keyword_2_instance_dict.keys()])
        post_group_message(group_id, answer_message)
        return 'ok'

    if message in alias_2_keyword_dict.keys():
        do_answer_question(group_id, message)
        return 'ok'

    if message in alias_2_keyword_dict_for_easter_egg.keys():
        do_send_easter_egg(group_id, message)
        return 'ok'

    if message == '召唤兽计算器':
        do_send_summon_beast_time(group_id, origin_message)
        return 'ok'

    post_group_message(group_id, '啊哦，这个问题胖胖还不知道哦。如果大家有谁知道的话，可以私聊告诉胖胖哦')
    return 'ok'


# 计算召唤兽剩余升级时间
def do_send_summon_beast_time(group_id, origin_message):
    beast_level = origin_message.split(' ')[2].lower()
    current_exp = origin_message.split(' ')[3]

    beast_time_dict = {
        'd': 7 * 60 + 40,
        'c': 15 * 60 + 12,
        'b': 30 * 60 + 24,
        'a': 60 * 60 + 53,
    }

    expect_remain_minutes_total = int((beast_time_dict[beast_level] * (100.0 - float(current_exp))) / 100.0)

    expect_remain_hour = expect_remain_minutes_total // 60
    expect_remain_minutes = expect_remain_minutes_total % 60

    return_message = ('预计召唤兽提升至下一等级时间为：{} 分钟（即 {} 小时 {} 分钟）').format(expect_remain_minutes_total,
                                                                     expect_remain_hour, expect_remain_minutes)
    post_group_message(group_id, return_message)
    return 'ok'
