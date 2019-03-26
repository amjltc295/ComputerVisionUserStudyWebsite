'''
Main Flask app and routes for create a user study (survey), answer
questions, show usernames and results
'''

__author__ = 'Ya-Liang Chang (Allen)'

from flask import jsonify

from . import app
from .logging_config import logger
from .db_interface import (
    get_results_dict,
    get_answers_dict, get_usernames_dict,
    create_user, create_answer, assign_survey,
    read_video_pairs, get_video_pairs_dict
)
from .config import VIDEO_PARI_FILENAME


# Before started, read video pair data from thie VIDEO_PARI_FILENAME
read_video_pairs(VIDEO_PARI_FILENAME)
logger.info("Ready")


@app.route('/start_survey/<username>')
def start_survey(username):
    '''
    Assigns a survey to the user
    '''
    create_user(username)
    survey_data_dict = assign_survey(username)

    return jsonify(survey_data_dict)


@app.route('/answer_question/<username>/<file_ID>/<ans>')
def answer_question(username, file_ID, ans):
    '''
    Receives the answer of a question from a user
    '''
    create_answer(username, file_ID, ans)
    msg = f"Got {file_ID} answer {ans} from {username}"
    logger.info(msg)
    response = {
        "message": msg
    }
    return jsonify(response)


@app.route('/show_usernames')
def show_usernames():
    '''
    Shows all usernames
    '''
    results = get_usernames_dict()
    return jsonify(results)


@app.route('/show_video_pairs')
def show_video_pairs():
    '''
    Shows all video pairs
    '''
    results = get_video_pairs_dict()
    return jsonify(results)


@app.route('/show_results')
def show_results():
    '''
    Shows all results
    '''
    results = get_results_dict()
    return jsonify(results)


@app.route('/show_answers')
def show_answers():
    '''
    Shows all answers
    '''
    results = get_answers_dict()
    return jsonify(results)


@app.route('/hi')
def hi():
    return 'Hi'


if __name__ == "__main__":
    app.run()
