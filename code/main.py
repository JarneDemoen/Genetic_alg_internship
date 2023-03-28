import pandas as pd
from random import choices

dataset_courseSchedule = pd.read_csv('../data/CourseSchedule.csv', sep=';')
# sort the dataset_courseSchedule by ET
dataset_courseSchedule = dataset_courseSchedule.sort_values(by=['ET'])

dataset_subjectsPP = pd.read_csv('../data/Courses.csv', sep=';')
dataset_professors = pd.read_csv('../data/Professors.csv', sep=';')

semester = 1

dataset_courseSchedule_semester = dataset_courseSchedule[dataset_courseSchedule['ET'] == semester]

timeslots_day = [
    "7:10-8:00",
    "8:00-8:50",
    "8:50-9:40",
    "9:55-10:45",
    "10:45-11:35",
    "11:35-12:25",
    "12:45-13:35",
    "13:35-14:25",
    "14:25-15:15",
    "15:30-16:20",
    "16:20-17:10",
    "17:10-18:00",
    "18:00-18:50",
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

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

len_classes_encoding = generate_bit_length(len(dataset_courseSchedule_semester))
len_professors_encoding = generate_bit_length(len(dataset_professors))
len_timeslots_day_encoding = generate_bit_length(len(days))
len_timeslots_encoding = generate_bit_length(len(timeslots_day))

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

def generate_genome():
    genome_class_binary = generate_genome_part(len_classes_encoding, dataset_courseSchedule_semester)
    genome_professor_binary = generate_genome_part(len_professors_encoding, dataset_professors)
    genome_timeslot_day_binary = generate_genome_part(len_timeslots_day_encoding, days)
    genome_timeslot_binary = generate_genome_part(len_timeslots_encoding, timeslots_day)
    genome = genome_class_binary + genome_professor_binary + genome_timeslot_day_binary + genome_timeslot_binary
    return genome

print(generate_genome())