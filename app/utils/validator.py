# -*- coding: utf-8 -*-

import json


def log_handler_validate(handler):
    def f(self):
        try:
            json_data = json.loads(self.request.body)
            if len(json_data) != 1 or 'offset' not in json_data:
                raise ValueError('JSON wrong schema')
            if type(json_data['offset']) != int:
                raise ValueError('JSON wrong schema, offset must be int')
            handler(self)
        except Exception as e:
            res = {
                'ok': False,
                'reason': e.message
            }
            self.write(json.dumps(res))
            self.finish()
    return f
