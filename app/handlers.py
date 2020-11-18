# -*- coding: utf-8 -*-

import json
import os
import tornado.web

from utils.validator import log_handler_validate


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self.PAGE_SIZE = self.application.settings['PAGE_SIZE']
        self.LOG_FILE_PATH = self.application.settings['LOG_FILE_PATH']


class LogsHandler(BaseHandler):

    @log_handler_validate
    def post(self):
        data = json.loads(self.request.body)
        offset = data.get('offset', 0)

        dirname = os.path.dirname(__file__)
        full_path = os.path.join(dirname, self.LOG_FILE_PATH)
        try:
            log_file = file(full_path)
        except IOError:
            raise IOError('Log file not found')

        with log_file as log_file:
            log_file.seek(0, 2)
            size = log_file.tell()

            start_position = self._get_line_start_offset(log_file, offset)
            cur_position = start_position
            log_file.seek(start_position, 0)
            log_lines = []
            while cur_position < start_position + self.PAGE_SIZE\
                    and cur_position < size:
                log_lines.append(log_file.readline())
                cur_position = log_file.tell()

            res = {
                'ok': True,
                'next_offset': cur_position,
                'total_size': size,
                'messages': log_lines
            }
            self.write(json.dumps(res))

    def _get_line_start_offset(self, log_file, offset):
        if offset <= 0:
            return 0
        else:
            log_file.seek(offset-1, 0)
            ch = log_file.read(1)
            if ch == '\n':
                return offset
            else:
                log_file.readline()
                return log_file.tell()
