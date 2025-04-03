from coze_bk import search_coze
from llm_bk import chat_deepseek
from liteai.api import chat

def process_query(education, graduation_years, query, stream=False):
    """
    处理用户信息并获取相关建议
    
    Args:
        education (str): 用户学历
        graduation_years (int): 毕业年限
    
    Returns:
        str: 处理结果和建议
    """
    # 构建查询
    search_query = f"用户学历为{education}，毕业{graduation_years}年，提出问题：{query}"
    print(f"search_query: {search_query}")
    
    # 首先从coze知识库获取信息
    coze_result = search_coze(search_query)
    kb_info = "\n".join([f"{i+1}. {item['output']}" for i, item in enumerate(coze_result)])
    print(f"kb_info: {kb_info}")
    
    # 构建发送给deepseek的提示
    prompt = f"""
    基于以下信息,做出回答：
    1. 用户学历：{education}
    2. 毕业年限：{graduation_years}年
    3. 知识库检索结果：{kb_info}
    4. 用户提出的问题：{query}
    
    """
    
    print(f"prompt: {prompt}")
    # 调用deepseek获取最终回答
    resp = chat(model="deepseek-chat", messages=prompt, stream=stream)
    
    return resp

if __name__ == "__main__":
    # 测试示例
    result = process_query("本科", 3, "给我推荐一个创业场地", stream=True)
    from liteai.utils import show_response
    show_response(result)
  
