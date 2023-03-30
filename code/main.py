import pandas as pd
from random import choices
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

dataset_courseSchedule = pd.read_csv('../data/CourseSchedule.csv', sep=';')
# sort the dataset_courseSchedule by ET
dataset_courseSchedule = dataset_courseSchedule.sort_values(by=['ET'])

dataset_subjectsPP = pd.read_csv('../data/Courses.csv', sep=';')
dataset_professors = pd.read_csv('../data/Professors.csv', sep=';')

# create a dataset where the semesters are uneven
dataset_courseSchedule_semester_uneven = dataset_courseSchedule[dataset_courseSchedule['ET'] % 2 != 0]

# create a dataset where the semesters are even
dataset_courseSchedule_semester_even = dataset_courseSchedule[dataset_courseSchedule['ET'] % 2 == 0]

timeslots_day = [
    "18:00-18:50",
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
class_types = ["AT", "AP"]
class_groups = ["A","B"]

# create a pandas dataframe where you combine the timeslots and days
timeslots = [timeslots_day for i in range(len(days))]

# create a dictionary where all of the courses that a teacher teaches are stored
professor_courses = {}
for professor in dataset_professors['CODE']:
    professor_code = str(professor)
    # the lenght of the professor code has to be 6, if not, add 0's to the right
    while len(professor_code) < 6:
        professor_code += "0"
    professor_courses[professor_code] = []
    for index in range(len(dataset_subjectsPP)):
        if dataset_subjectsPP['PROFESSOR CODE'][index] == professor:
            professor_courses[professor_code].append(dataset_subjectsPP['DISCIPLINA'][index])

def generate_bit_length(db_length):
    value = 0
    for i in range(10):
        value += 2**i
        if value >= db_length:
            return i+1

def generate_genome_part(length, database):
    binary_value = 100000
    genome = []
    while binary_value >= len(database):
        i = 0
        genome = choices([0,1], k=length)
        binary_value = 0
        reverse_genome = genome[::-1]
        for bit in reverse_genome:
            binary_value += bit*2**i
            i += 1
    return genome

def encode_class_scheduling():
    genome_class_binary = generate_genome_part(len_classes_encoding, dataset_courseSchedule_semester)
    genome_class_type_binary = generate_genome_part(len_class_types_encoding, class_types)
    genome_class_group_binary = generate_genome_part(len_class_groups_encoding, class_groups)
    genome_professor_binary = generate_genome_part(len_professors_encoding, dataset_professors)
    genome_timeslot_day_binary = generate_genome_part(len_timeslots_day_encoding, days)
    genome_timeslot_binary = generate_genome_part(len_timeslots_encoding, timeslots_day)
    genome = genome_class_binary + genome_class_type_binary + genome_class_group_binary + genome_professor_binary + genome_timeslot_day_binary + genome_timeslot_binary
    return genome

def generate_genome(size):
    return [encode_class_scheduling() for i in range(size)]

def get_binary_value_class_scheduling_part(encoded_part):
    # reverse the encoded_part
    reverse_encoded_part = encoded_part[::-1]
    binary_value = 0
    i = 0
    for bit in reverse_encoded_part:
        binary_value += bit*2**i
        i += 1
    return binary_value

def get_class_part(class_scheduling):
    return class_scheduling[:len_classes_encoding]

def get_class_type_part(class_scheduling):
    return class_scheduling[len_classes_encoding: len_classes_encoding+len_class_types_encoding]

def get_class_group_part(class_scheduling):
    return class_scheduling[len_classes_encoding+len_class_types_encoding: len_classes_encoding+len_class_types_encoding+len_class_groups_encoding]

def get_professor_part(class_scheduling):
    return class_scheduling[len_classes_encoding+len_class_types_encoding+len_class_groups_encoding:len_classes_encoding+len_class_types_encoding+len_class_groups_encoding+len_professors_encoding]

def get_timeslot_day_part(class_scheduling):
    return class_scheduling[len_classes_encoding+len_class_types_encoding+len_class_groups_encoding+len_professors_encoding:len_classes_encoding+len_class_types_encoding+len_class_groups_encoding+len_professors_encoding+len_timeslots_day_encoding]

def get_timeslot_part(class_scheduling):
    return class_scheduling[len_classes_encoding+len_class_types_encoding+len_class_groups_encoding+len_professors_encoding+len_timeslots_day_encoding:]

def translate_genome(genome):
    translation = []
    for class_scheduling in genome:
        class_part_value = get_binary_value_class_scheduling_part(get_class_part(class_scheduling))
        class_type_part = get_binary_value_class_scheduling_part(get_class_type_part(class_scheduling))
        class_group_part = get_binary_value_class_scheduling_part(get_class_group_part(class_scheduling))
        professor_part_value = get_binary_value_class_scheduling_part(get_professor_part(class_scheduling))
        timeslots_day_part_value = get_binary_value_class_scheduling_part(get_timeslot_day_part(class_scheduling))
        timeslots_part_value = get_binary_value_class_scheduling_part(get_timeslot_part(class_scheduling))

        class_part_translation = dataset_courseSchedule_semester['DISCIPLINA'][class_part_value]
        class_type_translation = class_types[class_type_part]
        class_group_translation = class_groups[class_group_part]
        professor_part_translation = dataset_professors['CODE'][professor_part_value]
        timeslots_day_part_translation = days[timeslots_day_part_value]
        timeslots_part_translation = timeslots_day[timeslots_part_value]

        # return the translated data of the genome in a dictionary
        translation.append({"class": class_part_translation,"class_type":class_type_translation,"class_group":class_group_translation,"professor": professor_part_translation, "timeslot_day": timeslots_day_part_translation, "timeslot": timeslots_part_translation})
    
    return translation

def translate_genome_to_hex(genome):
    translation = []
    for class_scheduling in genome:
        class_part_value = get_binary_value_class_scheduling_part(get_class_part(class_scheduling))
        class_type_part = get_binary_value_class_scheduling_part(get_class_type_part(class_scheduling))
        class_group_part = get_binary_value_class_scheduling_part(get_class_group_part(class_scheduling))
        professor_part_value = get_binary_value_class_scheduling_part(get_professor_part(class_scheduling))
        timeslots_day_part_value = get_binary_value_class_scheduling_part(get_timeslot_day_part(class_scheduling))
        timeslots_part_value = get_binary_value_class_scheduling_part(get_timeslot_part(class_scheduling))

        translation.append({"class": class_part_value,"class_type":class_type_part,"class_group":class_group_part,"professor": professor_part_value, "timeslot_day": timeslots_day_part_value, "timeslot": timeslots_part_value})

    # sort the translation based on the timeslot_day and timeslot
    translation = sorted(translation, key=lambda k: (k['timeslot_day'], k['timeslot']))
    return translation

def check_100_rule(hex_genome):
    # sort the dictionary of the hex_genome based on the timeslot_day and timeslot
    hex_genome_sorted = sorted(hex_genome, key=lambda k: (k['timeslot_day'], k['timeslot']))
    score = 0
    # check if there are classes on 2 following timeslots
    for index_day in range(len(days)):
        # return a dictionary with the classes of the day
        classes_day = [x for x in hex_genome_sorted if x['timeslot_day'] == index_day]
        # check if there are classes that day, if not, continue, it could be that there are no classes on that day, score stays 0
        if len(classes_day) == 0:
            continue

        for i in range(len(classes_day) - 1): # index to compare to 2 courses being taught on the same day
            for index_timeslot in range(len(timeslots_day)):
                if classes_day[i]['timeslot'] == index_timeslot and classes_day[i+1]['timeslot'] == index_timeslot + 1:
                    if classes_day[i]['class'] == classes_day[i+1]['class']:
                        score += 1
    return score

def check_conflict_rule(hex_genome):
    score = 3
    
    for index_day in range(len(days)):
        for index_timeslot in range(len(timeslots_day)):
            classes_day_timeslot = [x for x in hex_genome if x['timeslot_day'] == index_day and x['timeslot'] == index_timeslot]
            if len(classes_day_timeslot) > 1:
                score -= 1
                break

    score = score if score > 0 else 0
    return score

def fitness(hex_genome):
    score_100_rule = check_100_rule(hex_genome)
    score_conflict_rule = check_conflict_rule(hex_genome)
    # print("100 rule score: ", score_100_rule)
    # print("Conflict rule score: ", score_conflict_rule)

dataset_courseSchedule_semester = dataset_courseSchedule_semester_uneven
# reindex the database
dataset_courseSchedule_semester = dataset_courseSchedule_semester.reset_index(drop=True)
len_classes_encoding = generate_bit_length(len(dataset_courseSchedule_semester))
len_class_types_encoding = generate_bit_length(len(class_types))
len_class_groups_encoding = generate_bit_length(len(class_groups))
len_professors_encoding = generate_bit_length(len(dataset_professors))
len_timeslots_day_encoding = generate_bit_length(len(days))
len_timeslots_encoding = generate_bit_length(len(timeslots_day))

genome = generate_genome(len(dataset_courseSchedule_semester))
translation = translate_genome(genome)
binary_translation = translate_genome_to_hex(genome)
fitness(binary_translation)