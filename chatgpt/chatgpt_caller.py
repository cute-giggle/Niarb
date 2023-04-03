import openai
import os


os.environ["HTTP_PROXY"] = "192.168.31.44:7890"
os.environ["HTTPS_PROXY"] = "192.168.31.44:7890"


openai.api_key_path = os.path.join(os.path.dirname(__file__), '../data/openai/api-key.txt')


class ChatGPTCaller(object):    
    def __init__(self, model='gpt-3.5-turbo', temperature=0):
        self.model = model
        self.temperature = temperature

    def call(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
            request_timeout=20,
        )
        return response
    
    def call_simple(self, content):
        messages = [
            {'role': 'user', 'content': content},
        ]
        response = self.call(messages)
        return response


def main():
    caller = ChatGPTCaller()
    response = caller.call_simple('Left-Pallidum number of voxels too low may cause what?')
    print(response['choices'][0]['message']['content'])


if __name__ == '__main__':
    main()
