"""
This example describes how to use the workflow interface to chat.
"""

import os
# Our official coze sdk for Python [cozepy](https://github.com/coze-dev/coze-py)
from cozepy import COZE_CN_BASE_URL
from dotenv import load_dotenv
import json

load_dotenv()

# Get an access_token through personal access token or oauth.
coze_api_token = os.getenv("COZE_API_TOKEN")
# print(f"coze_api_token: {coze_api_token}")
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = COZE_CN_BASE_URL

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa



def search_coze(query, workflow_id='7488540002218901541'):
    # Init the Coze client through the access_token.
    coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

    # Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.

    # Call the coze.workflows.runs.create method to create a workflow run. The create method
    # is a non-streaming chat and will return a WorkflowRunResult class.
    workflow = coze.workflows.runs.create(
        workflow_id=workflow_id,
        parameters={"query": query}
    )
    data = json.loads(workflow.data)

    # print("workflow.data", workflow.data)
    return data["result"]

if __name__ == "__main__":
    rs = search_coze("你好")
    print(rs)