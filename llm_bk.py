# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import base64
from PIL import Image
import io

# 加载环境变量
load_dotenv()

def check_api_key(provider="deepseek"):
    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY")
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        print("错误: 未找到 API 密钥")
        sys.exit(1)
    if not api_key:
        print("错误: 未找到 DEEPSEEK_API_KEY 环境变量")
        print("请在 .env 文件中设置 DEEPSEEK_API_KEY=你的API密钥")
        sys.exit(1)
    return api_key

def chat_deepseek(message, model="deepseek-chat", stream=False):
    try:
        api_key = check_api_key()
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": message},
            ],
            stream=stream
        )
        if stream:
            return response.choices[0].message.content
        else:
            return response.choices[0].message.content
    except Exception as e:
        import traceback
        print("详细错误堆栈:")
        traceback.print_exc()
        if "Insufficient Balance" in str(e):
            print("错误: Deepseek API 账户余额不足")
            print("请检查您的 Deepseek API 账户余额或充值")
        return None

def create_image(prompt, size="1024x1024", model="dall-e-3"):
    """
    使用 GPT-4 Vision API 创作图片
    :param prompt: 图片描述
    :param size: 图片尺寸，可选 "1024x1024", "1024x1792", "1792x1024"
    :param model: 模型名称，可选 "dall-e-2" 或 "dall-e-3"
    :return: 生成的图片对象
    """
    try:
        api_key = check_api_key(provider="openai")
        client = OpenAI(api_key=api_key)
        
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        
        # 获取图片URL
        image_url = response.data[0].url
        
        # 下载图片
        import requests
        response = requests.get(image_url)
        image = Image.open(io.BytesIO(response.content))
        
        return image
    except Exception as e:
        print(f"生成图片时发生错误: {str(e)}")
        return None

if __name__ == "__main__":
    # 测试聊天功能
    rs = chat_deepseek("你好", stream=True) # 使用stream=True参数
    if rs:
        for chunk in rs:
            print(chunk, end="", flush=True)
    
    # 测试图片生成功能
    # image = create_image("生成一张吉卜力风格的图片，图片中有一只可爱的小猫咪，小猫咪正在吃着美味的鱼", model="dall-e-3")
    # if image:
    #     image.save("generated_image.png")
    #     print("图片已保存为 generated_image.png")