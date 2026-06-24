import logging
import json


logger = logging.getLogger(__name__)


results_file = 'results.jsonl'

def save_result(row: dict, file_path: str = results_file):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row) + '\n')