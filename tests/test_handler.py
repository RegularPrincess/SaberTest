import json
import os
import random

from tornado.testing import AsyncHTTPTestCase

from app.app import Application


class TestLogsHandler(AsyncHTTPTestCase):
    def get_app(self):
        if not hasattr(self, 'app'):
            self.app = Application()
        return self.app

    def setUp(self):
        super(TestLogsHandler, self).setUp()
        if hasattr(self, 'file_size'):
            return
        self.get_app().settings['LOG_FILE_PATH'] = 'logs/test_log.txt'
        dirname = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(dirname, os.pardir))
        full_path = os.path.join(parent_dir, 'app', 'logs/test_log.txt')# self.get_app().settings['LOG_FILE_PATH']
        f = file(full_path, 'w')
        lines = []
        for i in range(0, 128):
            level = random.choice(('info', 'debug', 'warning', 'error'))
            line = '{"level": %s, "message": "%d log message about some stuff number %d"}\n' % (level, i, i)
            lines.append(line)
        f.writelines(lines)
        f.seek(0, 2)
        self.file_size = f.tell()
        f.close()

    def test_empty_body(self):
        response = self.fetch('/', method="POST", body='{}')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertFalse(data['ok'])
        self.assertTrue('reason' in data)

    def test_wrong_offset(self):
        body = '{ "offset": "r12" }'
        response = self.fetch('/', method="POST", body=body)
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertFalse(data['ok'])
        self.assertTrue('reason' in data)

    def test_success_0(self):
        body = '{ "offset": 0 }'
        response = self.fetch('/', method="POST", body=body)
        self.check_success_response(response)

    def test_success_middle(self):
        offset = self.file_size // 2
        body = '{ "offset": %d }' % offset
        response = self.fetch('/', method="POST", body=body)
        self.check_success_response(response)

    def test_success_end(self):
        offset = self.file_size
        body = '{ "offset": %d }' % offset
        response = self.fetch('/', method="POST", body=body)
        self.check_success_empty_msg(response)

    def test_success_over_size(self):
        offset = self.file_size + 100
        body = '{ "offset": %d }' % offset
        response = self.fetch('/', method="POST", body=body)
        self.check_success_empty_msg(response)

    @classmethod
    def tearDownClass(cls):
        dirname = os.path.dirname(__file__)
        parent_dir = os.path.abspath(os.path.join(dirname, os.pardir))
        full_path = os.path.join(parent_dir, 'app', 'logs/test_log.txt')
        os.remove(full_path)

    def check_success_response(self, response):
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertTrue(data['ok'])
        self.assertTrue(data['total_size'], self.file_size)
        self.assertTrue('next_offset' in data)
        self.assertTrue(str.startswith(str(data['messages'][0]), '{"level":'))

    def check_success_empty_msg(self, response):
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertTrue(data['ok'])
        self.assertTrue(data['total_size'], self.file_size)
        self.assertTrue('next_offset' in data)
        self.assertEqual(len(data['messages']), 0)
