"""
Question prompt version 2.

This prompt is used to ask questions based on an eval 
dataset in order to test the accuracy of LLMs.

Changes:
- ask explicitly not to explain reasoning
- instruct to attempt question regardless of sufficient info
- remove 'helpful assistant' persona for control condition
- replace triple-quotes with explicit string concatenation
"""

PROMPT_NAME = 'question'
PROMPT_VERSION = 'v2'


def create_prompt(
        question: str, 
        options: str, 
        category: str, 
        is_expert: bool = False
    ):

    persona = ''
    if is_expert:
        persona = f'You are an expert in {category}.\n\n'

    prompt = (
        f'{persona}'
        'I will give you a question and some options.\n\n'
        'I want you to only return the letter (A-J) of the correct answer in brackets.\n\n'
        'Example answer:\n'
        "(C)\n\n"
        'Do not return anything else. Do not explain your reasoning.\n\n'
        'Even if you think you do not have enough information to answer the question, try anyway.\n\n'
        f'Question:\n{question}\n\n'
        f'Options:\n{options}'
    )

    return prompt.strip(), PROMPT_NAME + '_' + PROMPT_VERSION