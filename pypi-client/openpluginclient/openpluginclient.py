import json
import requests
import os

SUPPORTED_MODELS = ["gpt-4-0613", "gpt-3.5-turbo-0613"]
DEVELOPMENT = False
if (os.getenv("DEVELOPMENT") == "true"):
    DEVELOPMENT = True

def get_supported_plugins():
    current_dir = os.getcwd()
    print("current_dir", current_dir)
    file_path = os.path.join(current_dir, 'pypi-client', 'openpluginclient', 'plugins.json')
    print("file_path", file_path)
    with open(file_path, 'r') as f:
        return json.load(f)

def openplugin_completion(early_access_token: str, plugin_name: str = None, fail_silently: bool = False, **chatgpt_args):
    # Ensure the provided model is supported.
    model = chatgpt_args.get("model", "gpt-3.5-turbo-0613")
    if model not in SUPPORTED_MODELS:
        raise ValueError(f"Unsupported model: {model}. Try 'gpt-4-0613' or 'gpt-3.5-turbo-0613'.")

    # Ensure the plugin is supported.
    supported_plugins = get_supported_plugins()
    if plugin_name and plugin_name not in supported_plugins:
        raise ValueError(f"Unsupported plugin '{plugin_name}'. For full list of supported plugins, visit, https://github.com/CakeCrusher/openplugin-clients/blob/main/PLUGINS.md .")
    
    # Ensure messages are passed
    if not chatgpt_args.get("messages", None):
        raise ValueError(f"Messages must be passed to the openplugin_completion function.")
    # Ensure messages are not empty
    if len(chatgpt_args.get("messages", [])) == 0:
        raise ValueError(f"Messages cannot be empty.")

    body = {
        "early_access_token": early_access_token,
        "plugin_name": plugin_name,
        **chatgpt_args,
        "model": model,
        "messages": chatgpt_args.get("messages"),
    }

    try:
        # make a post request to localhost:3000
        server = "https://openplugin-api-30b78451a615.herokuapp.com"
        if DEVELOPMENT:
            server = "http://localhost:3000"
        
        response = requests.post(f"{server}/chat_completion", json=body)
        json_response = response.json()
        if ('error' in json_response):
            raise Exception(f"Error: {json_response['error']}")
    except Exception as e:
        if fail_silently:
            return print(e)
        else:
            raise e

    return response.json()  # Assume server responds with json content