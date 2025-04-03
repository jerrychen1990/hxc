import unittest
from hxc import process_query
import requests

class TestAPI(unittest.TestCase):
    def test_process_query(self):
        # 测试基本功能

        response = requests.post(
            "http://localhost:8000/api/query",
            json={
                "education": "本科",
                "graduation_years": 3,
                "query": "给我推荐一个创业场地"
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                print(line.decode('utf-8'))



if __name__ == '__main__':
    unittest.main()
