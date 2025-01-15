import pytest
import requests
import threading
import time

# Flask 应用程序的基本配置
BASE_URL = "http://localhost:5010"

# 启动 Flask 应用程序
def run_flask_app():
    from .app import app  # 请确保将这里的 `your_flask_app` 替换为您的 app 文件名
    app.run(port=5010)

@pytest.fixture(scope='module', autouse=True)
def flask_app():
    """用于启动和停止 Flask 应用的 fixture"""
    # 启动 Flask 应用的线程
    server_thread = threading.Thread(target=run_flask_app)
    server_thread.daemon = True
    server_thread.start()

    # 让 Flask 应用程序有时间启动
    time.sleep(1)
    
    yield  # 这里可以执行测试

    # 这里可以添加一些停止 Flask 服务器的代码

@pytest.fixture
def api_client():
    """创建一个 API 客户端实例"""
    return requests.Session()

def test_create_post(api_client):
    """测试创建帖子"""
    new_post = {"id": 1, "title": "First Post", "content": "This is the first post."}
    response = api_client.post(f"{BASE_URL}/posts", json=new_post)
    
    assert response.status_code == 201
    assert response.json() == new_post

def test_get_posts(api_client):
    """测试获取所有帖子"""
    response = api_client.get(f"{BASE_URL}/posts")
    
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "title": "First Post", "content": "This is the first post."}]

def test_update_post(api_client):
    """测试更新帖子"""
    updated_post = {"title": "Updated First Post", "content": "Updated content."}
    response = api_client.put(f"{BASE_URL}/posts/1", json=updated_post)
    
    assert response.status_code == 200
    assert response.json()['title'] == "Updated First Post"

def test_delete_post(api_client):
    """测试删除帖子"""
    response = api_client.delete(f"{BASE_URL}/posts/1")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Post deleted."}

    # 验证帖子是否真的被删除
    response = api_client.get(f"{BASE_URL}/posts")
    assert response.json() == []
