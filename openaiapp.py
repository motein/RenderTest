from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

print(os.getenv("OPENAI_ORGANIZATION"))

app = Flask(__name__)

# 获取 OpenAI API Key
print(os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_API_KEY"))

# client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/', methods=['GET'])
def index():
    return "Hello, this is the OpenAI API integration!"

@app.route("/analyze_trip", methods=["POST"])
def analyze_trip():
    try:
        # 接收纯文本输入
        text = request.data.decode("utf-8").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        prompt = f"""
从下面的出差描述中提取以下字段，并用 JSON 返回：
- 起始地
- 目的地
- 行驶距离
- 行驶时长
- 驾驶时间（日期时间）

示例描述：
{text}

请返回格式如下：
{{
  "start_location": "",
  "end_location": "",
  "distance": "",
  "duration": "",
  "start_time": ""
}}
"""
        # 使用新版本 openai SDK 的调用方式
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )

        result = response.choices[0].message.content.strip()
        print(result)

        # 解析 JSON 格式
        try:
            structured_data = json.loads(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse OpenAI response", "raw": result}), 500

        return jsonify(structured_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 启动 Flask 服务，绑定 0.0.0.0 以支持外部访问
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


