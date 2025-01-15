import pytest
import threading
import requests
from ..api.api_client import APIClient  # 导入 APIClient，注意变化以匹配您的目录结构

@pytest.fixture
def api_client():
    """创建一个 APIClient 实例"""
    base_url = f"https://h5api.m.taobao.com"  # 与 Flask 应用的 URL 匹配
    return APIClient(base_url, headers={"Content-Type": "application/json"})

def test_create_post(api_client):
    """测试淘宝首页mtop接口"""
    path = 'h5/mtop.tmall.kangaroo.core.service.route.aldlampservicefixedresv2/1.0/?jsv=2.7.2&appKey=12574478&t=1736843923732&sign=95b041908ac924454061ffc2ad605216&api=mtop.tmall.kangaroo.core.service.route.aldlampservicefixedresv2&type=originaljson&v=1.0&dataType=jsonp'
    c = api_client.call(path, method='GET')

    # Assert Request Sessions.
    assert isinstance(c.request, requests.models.Request)
    assert isinstance(c.prepared_request, requests.models.PreparedRequest)
    assert isinstance(c.response, requests.models.Response)

    # Assert Requst Modal.
    assert c.response.status_code == 200
    assert c.total_milliseconds < 1000

    except_resp_json = {'api': 'mtop.tmall.kangaroo.core.service.route.aldlampservicefixedresv2', 'data': {}, 'ret': ['FAIL_SYS_TOKEN_EMPTY::令牌为空'], 'traceId': '213e004117368470925171953e19e8', 'v': '1.0'}
    assert c.get_json_schema(except_resp_json) == c.get_json_schema(c.response.json())

    


