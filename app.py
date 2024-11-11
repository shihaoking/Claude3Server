from flask import Flask, request
import boto3
from claude_3 import Claude3Wrapper

app = Flask(__name__)

chat_history = []

@app.route('/conversation', methods=['POST'])
def reset_string():
    if request.method == 'POST':
        # 获取 POST 请求中的数据
        data = request.json
        
        if 'chat_content' in data:
            chat_content = data['chat_content']

            client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
            wrapper = Claude3Wrapper(client)

            chat_history.append({
                                "role": "user",
                                "content": [{"type": "text", "text": chat_content}]
                                })
            
            # Invoke Claude 3 with a text prompt
            print(f"Invoking Claude 3 Sonnet with '{chat_content}'...")
            response = wrapper.invoke_claude_3_with_text('你是一位慈祥的中国老人，性别男，年龄是80岁，姓名李一恒；你有一个2015年出生的孙子，名字叫李小涵，你十分疼爱他。你不太爱说话，说话不会超过70个字，甚至更少。特别注意，回答的内容不需要统计字符数，不需要添加任何动作的注释，完全模仿真人说话内容', 
                                                         chat_history)

            chat_result = response['content'][0]['text']

            chat_history.append({
                    "role": "assistant",
                    "content": [{"type": "text", "text": chat_result}]
                    })
            
            # 在这里进行你的处理，比如重置字符串的逻辑
            # 这里只是简单地将字符串转换为大写形式
            return chat_result, 200
        else:
            return "Error: 'chat_content' parameter is missing in the request.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
