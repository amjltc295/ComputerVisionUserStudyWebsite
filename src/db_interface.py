'''
All operations for the database
'''
import random

import pandas

from .model import VideoPair, SurveyData, Answer, User
from . import db
from .config import QUESTIONS_NUM_PER_SURVEY, QUESTIONS_RANDOM_FACTOR
from .logging_config import logger


#################################################
# Operations that involve changing the database #
#################################################

def create_answer(username, file_ID, ans):
    answer = Answer(username=username, file_ID=file_ID, ans=ans)
    db.session.add(answer)
    db.session.commit()
    return answer


def create_user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    return user


def create_survey_data(username, video_pairs):
    file_IDs = [video_pair.file_ID for video_pair in video_pairs]
    file_IDs_str = ", ".join(file_IDs)
    survey_data = SurveyData(username=username, video_pairs=file_IDs_str)
    db.session.add(survey_data)
    db.session.commit()
    return survey_data


def create_video_pair(file_ID, method_A, method_B, mask_type, mask_ratio):
    video_pair = VideoPair.query.filter_by(file_ID=file_ID).first()
    if video_pair is None:
        video_pair = VideoPair(
            file_ID=file_ID, method_A=method_A, method_B=method_B,
            mask_type=mask_type, mask_ratio=mask_ratio
        )
        db.session.add(video_pair)
        db.session.commit()
    return video_pair


def read_video_pairs(filename):
    '''
    Read video pair data from a csv with columns:
        file_ID, mask_type, mask_ratio, method_A, method_B
    '''
    df = pandas.read_csv(filename)
    logger.info(f"Reading video pair list from {filename}")
    for i, row in df.iterrows():
        file_ID, method_A, method_B, mask_type, mask_ratio = row[:5]
        create_video_pair(
            file_ID, method_A, method_B, mask_type, mask_ratio
        )


def receive_answer(file_ID, ans):
    if ans == 'A':
        video_pair = VideoPair.query.filter_by(file_ID=file_ID).first()
        video_pair.answer_A = video_pair.answer_A + 1
        db.session.commit()
    elif ans == 'B':
        video_pair = VideoPair.query.filter_by(file_ID=file_ID).first()
        video_pair.answer_B = video_pair.answer_B + 1
        db.session.commit()
    else:
        raise IOError(f"Invalid answer {ans} for {file_ID}")


def assign_video_pairs():
    '''
    Select videos from self.videopairs
    '''
    candidate_pairs = get_video_pairs(QUESTIONS_NUM_PER_SURVEY * QUESTIONS_RANDOM_FACTOR)
    random.shuffle(candidate_pairs)
    selected_pairs = candidate_pairs[:QUESTIONS_NUM_PER_SURVEY]
    assert len(selected_pairs) == QUESTIONS_NUM_PER_SURVEY
    return selected_pairs


def assign_survey(username):
    '''
    Assign video pairs to a survey
    '''
    video_pairs = assign_video_pairs()
    survey_data = create_survey_data(username, video_pairs)
    logger.info(f"Assigned survey_ID {survey_data.id}")
    survey_data_dict = get_survey_data_dict(survey_data)
    return survey_data_dict


###########
# Queries #
############

def get_video_pairs(n):
    video_pairs = VideoPair.query.order_by(
        VideoPair.answer_A + VideoPair.answer_B
    ).limit(n).all()
    return video_pairs


def get_results_dict():
    '''
    Get results from the database and return a nested dictionary
    '''
    answer_num = len(Answer.query.all())
    results_dict = {
        "answer_num": answer_num,
        "video_answers": {}
    }
    all_results = {}

    video_pairs = VideoPair.query.all()
    for video_pair in video_pairs:
        result = get_video_pair_result(video_pair)
        exp_name = get_video_pair_exp_name(video_pair)
        if exp_name not in all_results:
            all_results[exp_name] = result
        else:
            all_results[exp_name]["ours_win"] += result["ours_win"]
            all_results[exp_name]["ours_lose"] += result["ours_lose"]

    results_dict["results"] = all_results
    return results_dict


def get_answers_dict():
    answers = Answer.query.all()
    answers_dict = {}
    for answer in answers:
        answers_dict[answer.id] = {
            "username": answer.username,
            "file_ID": answer.file_ID,
            "ans": answer.ans,
            "timestamp": answer.timestamp
        }
    return answers_dict


def get_video_pairs_dict():
    video_pairs = VideoPair.query.all()

    video_pairs_dict = {}
    for video_pair in video_pairs:
        video_pairs_dict[video_pair.file_ID] = {
            "method_A": video_pair.method_A,
            "method_B": video_pair.method_B,
            "mask_type": video_pair.mask_type,
            "mask_ratio": video_pair.mask_ratio,
            "answer_A": video_pair.answer_A,
            "answer_B": video_pair.answer_B,
        }
    return video_pairs_dict


def get_usernames_dict():
    users = User.query.all()

    users_dict = {}
    for user in users:
        users_dict[user.id] = {
            "username": user.username,
            "timestamp": user.timestamp
        }
    return users_dict


######################
# Change data format #
######################
def get_survey_data_dict(survey_data):
    video_pairs = {}
    for i, file_ID in enumerate(survey_data.video_pairs.split(', ')):
        video_pairs[i] = file_ID

    data_dict = {
        "ID": survey_data.id,
        "videoPairs": video_pairs
    }
    return data_dict


def get_video_pair_answer_num(video_pair):
    return video_pair.answer_A + video_pair.answer_B


def get_video_pair_exp_name(video_pair):
    compared_method = video_pair.method_B if video_pair.method_A == 'Ours' else video_pair.method_A
    return f"{video_pair.mask_type}_{video_pair.mask_ratio}_Ours_vs_{compared_method}"


def get_video_pair_result(video_pair):
    ours_win = video_pair.answer_A if video_pair.method_A == 'Ours' else video_pair.answer_B
    ours_lose = video_pair.answer_B if video_pair.method_A == 'Ours' else video_pair.answer_A
    return {
        "ours_win": ours_win,
        "ours_lose": ours_lose
    }
