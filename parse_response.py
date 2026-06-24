import logging


logger = logging.getLogger(__name__)


def parse_response(response_text: str, answer: str):

    letters = [
        '(A)', '(B)', '(C)', '(D)', '(E)', '(F)', '(G)', '(H)', '(I)', '(J)'
    ]

    correct_answer = '(' + answer + ')'

    incorect_answers = set(letters) - {correct_answer}

    logger.info(
            'correct_answer=%s incorect_answers=%s',
            correct_answer,
            incorect_answers
        )
    
    correct = correct_answer in response_text
    
    incorrect = any([(letter in response_text) for letter in incorect_answers])

    if correct and not incorrect:
        return 'pass'
    elif incorrect and not correct:
        return 'fail'
    else:
        return 'parse_failure'