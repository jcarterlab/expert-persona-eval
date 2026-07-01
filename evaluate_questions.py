import logging
from types import ModuleType
import time
from datetime import datetime, timezone

from google import genai
from google.genai import types
from datasets import Dataset

from prompts.question import v2
from parse_response import parse_response
from filter_questions import filter_questions
from save_result import save_result


logger = logging.getLogger(__name__)


prompt_identifier = v2.PROMPT_NAME + '_' + v2.PROMPT_VERSION


def loop_over_questions(
        client: genai.Client, 
        filtered_ds: Dataset, 
        config: ModuleType,
        is_expert: bool = False
    ):

    retry_attempts = config.LLM_RETRY_ATTEMPTS
    llm_wait_time = config.LLM_WAIT_TIME

    first_inference = True

    for row in filtered_ds:

        for attempt in range(1, retry_attempts + 1):

            wait_time = llm_wait_time * (2 ** (attempt - 1))

            if first_inference:
                first_inference = False
            else:
                time.sleep(wait_time)

            try:

                prompt = v2.create_prompt(
                    row['question'], 
                    row['options'], 
                    row['category'],
                    is_expert
                )

                response = client.models.generate_content(
                    model=config.BASIC_MODEL, 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.0
                    )
                )

                result = parse_response(
                    response.text, 
                    row['answer']
                )

                response_time = datetime.now(timezone.utc).isoformat(timespec="seconds")

                save_result({
                    'result': result,
                    'category': row['category'],
                    'is_expert': is_expert,
                    'question': row['question'],
                    'correct_answer': row['answer'],
                    'llm_answer': response.text,
                    'asked_at': response_time,
                    'prompt': prompt_identifier,
                    'model': config.BASIC_MODEL
                })

                logger.info(
                        'result=%s',
                        result
                    )

                break 

            except Exception:

                if attempt < retry_attempts:

                    logger.error(
                        'LLM call failed on attempt %d',
                        attempt,
                        exc_info=True
                    )

                else:

                    logger.error(
                        'LLM call failed after %d attempts - moving on',
                        retry_attempts,
                        exc_info=True
                    )
  

def evaluate_questions(
        client: genai.Client, 
        sample_ds: Dataset, 
        config: ModuleType
    ):

    is_expert_conditions = [True, False]

    for condition in is_expert_conditions:

        filtered_ds = filter_questions(
            sample_ds, 
            condition,
            prompt_identifier,
            config
        )

        loop_over_questions(
            client, 
            filtered_ds, 
            config,
            is_expert=condition
        )