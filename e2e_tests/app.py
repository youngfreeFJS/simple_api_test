from flask import Flask, jsonify, request

app = Flask(__name__)

# 存储帖子
posts = []

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200

@app.route('/posts', methods=['POST'])
def create_post():
    new_post = request.json
    posts.append(new_post)
    return jsonify(new_post), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    updated_data = request.json
    for post in posts:
        if post['id'] == post_id:
            post.update(updated_data)
            return jsonify(post), 200
    return jsonify({"error": "Post not found."}), 404

@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [post for post in posts if post['id'] != post_id]
    return jsonify({"message": "Post deleted."}), 200

if __name__ == '__main__':
    app.run(port=5010)  # 确保使用该端口
