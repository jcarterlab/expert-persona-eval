import logging
from types import ModuleType
from datetime import datetime, timezone

from google import genai
from google.genai import types
from datasets import load_dataset

import config
from evaluate_questions import evaluate_questions


logger = logging.getLogger(__name__)


def configure_logging(config: ModuleType):
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

    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('google_genai').setLevel(logging.WARNING)


def run_eval(client: genai.Client, config):
    
    ds = load_dataset('TIGER-Lab/MMLU-Pro', split='test')

    sample_ds = ds.shuffle(seed=config.RANDOM_SEED).select(range(config.DS_SAMPLE_NO))

    evaluate_questions(
        client, 
        sample_ds, 
        config
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
            api_key=config.GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=60000)
        )

        run_eval(client, config)

    except Exception:

        logger.critical(
            'run_id=%s | Pipeline execution failed',
            run_id,
            exc_info=True
        )

        raise