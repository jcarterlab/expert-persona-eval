import os
import logging
import json


logger = logging.getLogger(__name__)


def filter_questions(sample_ds):

    successful_questions = set()

    if os.path.exists('results.jsonl'):
        with open('results.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    obj = json.loads(line)

                    question = obj.get('question')
                    result = obj.get('result')

                    if result != 'parse_failure':
                        successful_questions.add(question)

    return sample_ds.filter(lambda x: x['question'] not in successful_questions)

