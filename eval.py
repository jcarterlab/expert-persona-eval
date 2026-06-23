import logging
import random
import time
from datetime import datetime, timezone

from google import genai
import pandas as pd
from datasets import load_dataset

import config

from create_prompt import create_prompt
from parse_response import parse_response
from save_result import save_result


logger = logging.getLogger(__name__)


def configure_logging(config):
    """
    Configure application logging.

    Sets global logging format, application log level
    and suppresses noisy third-party library logs.

    Args:
        config: Application configuration object.
    """

    logging.basicConfig(
        level=config.LOG_LEVEL,
        format=(
            '%(asctime)s | %(levelname)s | '
            '%(name)s | %(message)s'
        )
    )

    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('google_genai').setLevel(logging.WARNING)


def run_eval(client, config):
    
    ds = load_dataset('TIGER-Lab/MMLU-Pro', split='test')
    
    sample_ds = ds.shuffle(seed=config.RANDOM_SEED).select(range(config.DS_SAMPLE_NO))

    for q in sample_ds:

        prompt = create_prompt(
            q['question'], 
            q['options'], 
            q['category']
        )

        response = client.models.generate_content(
            model=config.BASIC_MODEL, 
            contents=prompt
        )

        result = parse_response(
            response.text, 
            q['answer']
        )

        save_result({
            'question': q['question'],
            'answer': q['answer'],
            'result': result,
            'category': q['category'],
        })

        logger.info(
                'result=%s response=%s',
                result,
                response.text
            )
        

if __name__ == '__main__':

    configure_logging(config)

    run_id = datetime.now(timezone.utc).strftime(
        '%Y%m%d-%H%M%S'
    )

    try:

        logger.info(
                'run_id=%s | Initialising LLM client',
                run_id
            )

        client = genai.Client(
            api_key=config.GEMINI_API_KEY
        )

        run_eval(client, config)

    except Exception:

        logger.critical(
            'run_id=%s | Pipeline execution failed',
            run_id,
            exc_info=True
        )

        raise