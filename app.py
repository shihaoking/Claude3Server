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
            response = wrapper.invoke_claude_3_with_text('你是一个人工智能机器人，尽量模仿真人的说话交流方式，并且你的回答通常比较简练', 
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
