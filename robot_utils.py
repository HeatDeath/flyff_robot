from load_yaml_conf import base_conf

concerned_group_ids = base_conf['concerned_group_ids']
notice_sync_group_ids = base_conf['notice_sync_group_ids']

myself_qq_id = str(base_conf['myself_qq_id'])


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
