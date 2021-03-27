import datetime


class Message:
    def __init__(self, msg_dict, username):
        self.msg_dict = msg_dict
        self.msg_id = msg_dict.get('msg_id')
        self.sender = username
        self.receiver = msg_dict.get('receiver')
        self.subject = msg_dict.get('subject')
        self.msg_data = msg_dict.get('msg_data')
        self.created_at = msg_dict.get('created_at') or datetime.datetime.utcnow()
        self.unread = msg_dict.get('unread') or True

    def to_json(self):
        json_message = dict(msg_id=self.msg_id,
                            sender=self.sender,
                            receiver=self.receiver,
                            subject=self.subject,
                            msg_data=self.msg_data,
                            created_at=self.created_at)
        return json_message

    def ready_to_DB(self):
        if self.receiver and self.subject and self.msg_data:
            return True
        return False
