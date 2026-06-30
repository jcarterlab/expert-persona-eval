import os
import logging
import json


logger = logging.getLogger(__name__)


def filter_questions(
        sample_ds, 
        is_expert,
        config
    ):

    logger.info(
        'filtering questions is_expert=%s',
        is_expert
    )

    successful_questions = set()

    if os.path.exists('results.jsonl'):
        with open('results.jsonl', 'r', encoding='utf-8') as f:

            for line in f:

                if not line.strip():
                    continue

                obj = json.loads(line)

                if obj.get('is_expert') != is_expert:
                    continue

                if config.RETRY_PARSE_FAILURES:

                    if obj.get('result') != 'parse_failure':
                        successful_questions.add(obj['question'])

                else:
                    successful_questions.add(obj['question'])

    filtered_ds = sample_ds.filter(
        lambda x: x['question'] not in successful_questions
    )

    logger.info(
        'question filtering completed questions_filtered=%d',
        len(sample_ds) - len(filtered_ds)
    )

    return filtered_ds