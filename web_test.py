#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import unittest
import web


class TestWeb(unittest.TestCase):
    def setUp(self):
        self.app = web.app.test_client()

    def test_ping(self):
        response = self.app.get('/ping')
        assert response.status_code == 200
        assert response.data == b'OK'

    # Note: This makes a real HTTP request
    def test_resize_api(self):
        params = {
            'url': 'https://avatars0.githubusercontent.com/u/23497'
        }
        response = self.app.post('/api/v1/resize', data=params)
        assert response.status_code == 200

        response_data = json.loads(response.data)
        response_data['status'] == 'OK'


if __name__ == '__main__':
    unittest.main()
