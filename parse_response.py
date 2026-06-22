import logging

logger = logging.getLogger(__name__)

def parse_response(response, answer):

    letters = ['(A)', '(B)', '(C)', '(D)', '(E)', '(F)', '(G)', '(H)', '(I)', '(J)']

    correct_answer = '(' + answer + ')'

    incorect_answers = set(letters) - {correct_answer}

    logger.info(
            'correct_answer=%s incorect_answers=%s',
            correct_answer,
            incorect_answers
        )
    
    correct = correct_answer in response
    incorrect = any([(letter in response) for letter in incorect_answers])

    if correct and not incorrect:
        return 'pass'
    elif incorrect and not correct:
        return 'fail'
    else:
        return 'parse_failure'