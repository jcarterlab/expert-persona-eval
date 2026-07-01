"""
Question prompt version 1.

This prompt is used to ask questions based on an eval 
dataset in order to test the accuracy of LLMs.
"""

PROMPT_NAME = 'question'
PROMPT_VERSION = 'v1'


def create_prompt(
        question: str, 
        options: str, 
        category: str, 
        is_expert: bool = False
    ):

    if is_expert:
        persona = 'an expert in ' + category 
    else:
        persona = 'a helpful assistant'

    prompt = f'''
You are {persona}.

I will give you a question and some options. 

I want you to only return the letter (A-J) of the 
correct answer in brackets. 

Example answer: 
(C)

Do not return anything else. 

Question:
{question}

Options:
{options}
'''.strip()
    
    return prompt, PROMPT_NAME + '_' + PROMPT_VERSION