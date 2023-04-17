import os
from dotenv import load_dotenv
from BilibiliHelper import BilibiliHelper

def main():
    load_dotenv()
    config = {
        'roomid':int(os.environ['ROOMID']),
        'api_key': os.environ['OPENAI_API_KEY'],
        'prompt': os.environ.get('PROMPT', 'You are a helpful assistant.'),
        'max_tokens': int(os.environ.get('MAX_TOKENS', 2400)),
        'n_choices': int(os.environ.get('N_CHOICES', 1)),
        'temperature': float(os.environ.get('TEMPERATURE', 1.0)),
        'model': os.environ.get('MODEL',"gpt-3.5-turbo"),
        'presence_penalty': float(os.environ.get('PRESENCE_PENALTY', 0.0)),
        'frequency_penalty': float(os.environ.get('FREQUENCY_PENALTY', 0.0)),
    }
    bilihelper = BilibiliHelper(config)
    bilihelper.run()

if __name__ == '__main__':
    main()