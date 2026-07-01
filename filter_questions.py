import os
import logging
from types import ModuleType
import json

from datasets import Dataset

logger = logging.getLogger(__name__)


def filter_questions(
        sample_ds: Dataset, 
        condition: bool,
        prompt_identifier: str,
        config: ModuleType
    ):

    logger.info(
        'filtering questions condition=%s',
        condition
    )

    completed = set()

    if os.path.exists('results.jsonl'):
        with open('results.jsonl', 'r', encoding='utf-8') as f:

            for line in f:

                if not line.strip():
                    continue

                obj = json.loads(line)

                if (
                    obj.get("is_expert") != condition
                    or obj.get("model") != config.BASIC_MODEL
                ):
                    continue

                if config.RETRY_PARSE_FAILURES:
                    if obj.get('result') != 'parse_failure':
                        key = (
                            obj.get('question'),
                            obj.get('is_expert'),
                            obj.get('prompt')
                        )
                        completed.add(key)
                else:
                    key = (
                        obj.get('question'),
                        obj.get('is_expert'),
                        obj.get('prompt')
                    )
                    completed.add(key)

    filtered_ds = sample_ds.filter(
        lambda x: (
            x['question'],
            condition,
            prompt_identifier
        ) not in completed
    )

    logger.info(
        'question filtering completed questions_filtered=%d',
        len(sample_ds) - len(filtered_ds)
    )

    return filtered_ds