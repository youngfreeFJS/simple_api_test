import requests
from genson import SchemaBuilder
from jsonpath_ng import jsonpath, parse

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.default_headers = headers if headers else {}
        self.request: requests.models.Request = None
        self.prepared_request: requests.models.PreparedRequest = None
        self.response: requests.models.Response = None

        
    def call(self, path, method='GET', data=None, **kwargs) -> 'APIClient':
        """
        发送 HTTP 请求。

        :param url: 请求的 URL。
        :param method: HTTP 方法，例如 'GET', 'POST', 'PUT', 'DELETE' 等。
        :param data: 请求体数据，适用于 POST 和 PUT 请求。
        :param kwargs: 其他请求参数，如 headers, params 等。
        :return: 响应对象。
        """
        # 创建会话
        session = requests.Session()

        # 创建请求对象
        self.request: requests.models.Request = requests.Request(method, f'{self.base_url}{f"/{path}" if not path.startswith("/") else path}', json=data, **kwargs)
        
        # 准备请求
        self.prepared_request: requests.models.PreparedRequest = session.prepare_request(self.request)

        # 发送请求
        self.response: requests.models.Response = session.send(self.prepared_request)

        # 返回响应对象
        return self

    @property
    def total_seconds(self) -> float:
        """返回响应时间（秒）"""
        return self.response.elapsed.total_seconds()

    @property
    def total_milliseconds(self) -> float:
        """返回响应时间（毫秒）"""
        # 使用 total_seconds 获取总秒数并转换为毫秒
        return self.response.elapsed.total_seconds() * 1000

    @property
    def total_minutes(self) -> float:
        """返回响应时间（分钟）"""
        return self.response.elapsed.total_seconds() / 60

    @staticmethod
    def get_json_schema(data):
        """根据输入的 JSON 数据生成 JSON Schema"""
        builder = SchemaBuilder()
        builder.add_object(data)
        return builder.to_schema()
    
    def assert_json_path(self, json_path, expected_value):
        """断言 JSON 路径的值"""

        # JSONPath 表达式
        jsonpath_expression = parse('$.ret[0]')  # 获取 ret 列表中的第一个元素

        # 执行查询
        result = jsonpath_expression.find(json_data)

        # 检查结果并提取值
        if result:
            print("提取的值:", result[0].value)  # 获取到的是 jsonpath_ng.objects.JsonPathMatch 对象
        else:
            print("未找到匹配的结果。")
        assert self.response.json()[json_path] == expected_value
