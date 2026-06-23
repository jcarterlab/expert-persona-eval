def create_prompt(question, options, category = None):

    prompt = f'''
You are a helpful assistant.

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
'''
    return prompt