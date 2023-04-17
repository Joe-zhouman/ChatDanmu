import datetime
import logging

# import tiktoken

import openai

import requests
import json
from datetime import date
from calendar import monthrange

# Models can be found here: https://platform.openai.com/docs/models/overview
GPT_3_MODELS = ("gpt-3.5-turbo", "gpt-3.5-turbo-0301")
GPT_4_MODELS = ("gpt-4", "gpt-4-0314")
GPT_4_32K_MODELS = ("gpt-4-32k", "gpt-4-32k-0314")
GPT_ALL_MODELS = GPT_3_MODELS + GPT_4_MODELS + GPT_4_32K_MODELS


def default_max_tokens(model: str) -> int:
    """
    Gets the default number of max tokens for the given model.
    :param model: The model name
    :return: The default number of max tokens
    """
    return 1200 if model in GPT_3_MODELS else 2400

class OpenaiHelper:
    """
    ChatGPT helper class.
    """
    def __init__(self, config: dict):
        """
        Initializes the OpenAI helper class with the given configuration.
        :param config: A dictionary containing the GPT configuration
        """
        self.config = config
        self.prompt = config['prompt']
        openai.api_key = config['api_key']
        openai.proxy = config['proxy']
    async def get_chat_response(self, message):
        """
        Request a response from the GPT model.
        :param chat_id: The chat ID
        :param query: The query to send to the model
        :return: The answer from the model and the number of tokens used
        """
        response = await self.__commpm_get_chat_response(message)
        return response.choices[0]['message']['content'].strip()
    async def __commpm_get_chat_response(self, message):
        """
        Request a response from the GPT model.
        :param chat_id: The chat ID
        :param query: The query to send to the model
        :return: The answer from the model and the number of tokens used
        """
        send_message = [
            {
                "role":"system",
                "content":self.prompt
            },
            {
                "role":"user",
                "content":message
            }
        ]
        try:
            return await openai.ChatCompletion.acreate(
                model=self.config['model'],
                messages=send_message,
                temperature=self.config['temperature'],
                n=self.config['n_choices'],
                max_tokens=self.config['max_tokens'],
                presence_penalty=self.config['presence_penalty'],
                frequency_penalty=self.config['frequency_penalty'],
                stream=False
            )

        except openai.error.RateLimitError as e: # type: ignore
            raise Exception(f'⚠️ _OpenAI Rate Limit exceeded_ ⚠️\n{str(e)}') from e

        except openai.error.InvalidRequestError as e: # type: ignore
            raise Exception(f'⚠️ _OpenAI Invalid request_ ⚠️\n{str(e)}') from e

        except Exception as e:
            raise Exception(f'⚠️ _An error has occurred_ ⚠️\n{str(e)}') from e
