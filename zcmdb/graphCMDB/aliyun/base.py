# -*- coding: UTF-8 -*-
"""
    aliyun.base
    ~~~~~~~~~~~
"""
from __future__ import print_function
import os
import json
import ConfigParser

from aliyunsdkcore import client


class AliyunBase(object):
    """Aliyun base class."""
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform = str
    cfg_dir = os.path.dirname(__file__)
    cfg.read(os.path.join(cfg_dir, 'config.ini'))
    clts = []
    sections = cfg.sections()
    for section in sections:
        options = dict(cfg.items(section))
        for reg in options['REGION'].split(','):
            clts.append(client.AcsClient(
                options['ACCESSKEY'],
                options['ACCESS_SECRET'],
                reg
            ))

    @classmethod
    def do_request(cls, Request, page_num=1, page_size=100):
        """Send requests to aliyun open APIs.

        :param Request:  aliyun RpcRequest class.
        :type Request: aliyunsdkcore.request.RpcRequest
        :param page_num: page number.
        :type page_num: int
        :param page_size: page size.
        :type page_size: int
        :return: list of [client, response].
        :rtype: list
        """
        responses = []
        for c in cls.clts:
            # one instance, one request only. so do the fuck below
            request = Request()
            request.set_accept_format('json')
            request.add_query_param('PageNumber', page_num)
            request.add_query_param('PageSize', page_size)
            resp = json.loads(c.do_action(request))
            responses.append([c, resp])
        return responses

    @classmethod
    def do_single_request(cls, client, request, page_num=1, page_size=100):
        """Send a request to aliyun open APIs.

        :param client:  aliyun client.
        :type client: aliyunsdkcore.client.AcsClient
        :param request:  aliyun request instance.
        :type request: aliyunsdkcore.request.RpcRequest
        :param page_num: page number.
        :type page_num: int
        :param page_size: page size.
        :type page_size: int
        :return: aliyun response.
        :rtype: dict
        """
        request.set_accept_format('json')
        request.add_query_param('PageNumber', page_num)
        request.add_query_param('PageSize', page_size)
        response = json.loads(client.do_action(request))
        return response
