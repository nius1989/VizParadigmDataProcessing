import csv
import os
import json
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from global_config import *


def process(csv_file):
    load_questionnaire(csv_file, "questionnaire_difficult", "difficult", "Difficult")
    # load_questionnaire(csv_file, "questionnaire_effort", "effort", "Effort")
    # load_questionnaire(csv_file, "questionnaire_check_frequency", "check frequency", "Check frequency")
    # load_questionnaire(csv_file, "questionnaire_track_talk_partner", "talk to partner", "track work_1")
    # load_questionnaire(csv_file, "questionnaire_track_observe_card", "observe card", "track work_2")
    # load_questionnaire(csv_file, "questionnaire_track_visualization", "use visualization", "track work_3")
    # load_questionnaire(csv_file, "questionnaire_viz_find_largest", "find largest items", "Viz usefulness_5")
    # load_questionnaire(csv_file, "questionnaire_viz_identify_categories", "identify categories", "Viz usefulness_9")
    load_questionnaire(csv_file, "questionnaire_viz_relate_specific", "relate to a specific item", "Viz usefulness_7")
    load_questionnaire(csv_file, "questionnaire_viz_common_feature", "items share common feature", "Viz usefulness_8")
    load_questionnaire(csv_file, "questionnaire_find_partner", "find items from partner", "find partner side")
    load_questionnaire(csv_file, "questionnaire_support_discussion", "support discussion", "discuss and look")
    # load_questionnaire(csv_file, "questionnaire_need_adjustment", "need adjustment", "adjust placement")
    # load_questionnaire(csv_file, "questionnaire_support_plan", "support plan", "plan")
    # load_questionnaire(csv_file, "questionnaire_support_help", "support help others", "help other")
    # load_questionnaire(csv_file, "questionnaire_seek_help", "support seek help", "other help")
    load_questionnaire(csv_file, "questionnaire_concentrate", "affect concentration", "conecntrate")
    # load_questionnaire(csv_file, "questionnaire_track_doing", "track doing", "track")
    load_questionnaire(csv_file, "questionnaire_alter", "feel work altered", "alter")
    # load_layout_pattern(csv_file, "questionnaire_manage_card", "card management")


def load_questionnaire(csv_file, save_file_name, column_name, column_id):
    work_sheet = csv.DictReader(open(csv_file))
    with open(final_result_dir + save_file_name + '.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "id", column_name])
        for row in work_sheet:
            print(row)
            group_code = row["C2"]
            if len(group_code) == 1:
                group_code = "0" + group_code
            group_code = row["C1"] + group_code
            overhead_writer.writerow([switcher(row["C1"]), group_code, row[column_id]])


def load_layout_pattern(csv_file, save_file_name, column_name):
    work_sheet = csv.DictReader(open(csv_file))
    manage_code = ["by similarity", "random", "sort feature", "searching order"]
    with open(final_result_dir + save_file_name + '.csv', mode='w', newline='') as overhead_data:
        overhead_writer = csv.writer(overhead_data, lineterminator='\n')
        overhead_writer.writerow(["paradigm", "id", column_name])
        for row in work_sheet:
            group_code = row["C2"]
            if len(group_code) == 1:
                group_code = "0" + group_code
            group_code = row["C1"] + group_code
            overhead_writer.writerow([switcher(row["C1"]), group_code, manage_code[int(row["Ways to manage"]) - 1]])


def switcher(text_code):
    if text_code is '1':
        return "PRL"
    elif text_code is '2':
        return "CON"
    elif text_code is '3':
        return "MEG"


if __name__ == '__main__':
    process(analysis_result + "post_study_questionnaire.csv")
    # save_csv(result)
