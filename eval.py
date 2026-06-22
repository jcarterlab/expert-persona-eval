import logging
import config
from google import genai
import pandas as pd
import random
from datasets import load_dataset
from create_prompt import create_prompt
from parse_response import parse_response


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=config.LOG_LEVEL,
    format=(
        '%(asctime)s | %(levelname)s | '
        '%(name)s | %(message)s'
    )
)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('google_genai').setLevel(logging.WARNING)




client = genai.Client(api_key=config.GEMINI_API_KEY)

model = 'gemini-2.5-flash-lite'

ds = load_dataset('TIGER-Lab/MMLU-Pro', split='test')

sample_ds = ds.shuffle(seed=2026).select(range(5))

for q in sample_ds:
    question = q['question']
    options = q['options']
    answer = q['answer']
    category = q['category']

    prompt = create_prompt(question, options)

    response = client.models.generate_content(
        model=model, 
        contents=prompt
    )

    result = parse_response(response.text, answer)

    logger.info(
            'result=%s response=%s',
            result,
            response.text
        )