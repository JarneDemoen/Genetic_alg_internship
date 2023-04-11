# imports
import pandas as pd
from random import choices, randint
import os

# making sure the file is in the same directory as the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Inputs user
semester = "uneven"
timeslots_day = [
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
class_groups = ["A","B"]

# global variables
dataset_courseSchedule = pd.read_csv('../data/CourseSchedule.csv', sep=';')
dataset_courseSchedule = dataset_courseSchedule.sort_values(by=['ET'])
dataset_classesPP = pd.read_csv('../data/ClassesPP.csv', sep=';')
dataset_professors = pd.read_csv('../data/Professors.csv', sep=';')
dataset_courseSchedule_semester_uneven = dataset_courseSchedule[dataset_courseSchedule['ET'] % 2 != 0]
dataset_courseSchedule_semester_even = dataset_courseSchedule[dataset_courseSchedule['ET'] % 2 == 0]
timeslots = [timeslots_day for i in range(len(days))]
class_types = ["AT", "AP", "AV"]

genome_size_even = 0
genome_size_uneven = 0
genome_size = 0

for etapa in range (1, 9):
    if etapa < 4:
        genome_size_even += len(class_groups) * len(dataset_courseSchedule_semester_even[dataset_courseSchedule_semester_even['ET'] == etapa])
        genome_size_uneven += len(class_groups) * len(dataset_courseSchedule_semester_uneven[dataset_courseSchedule_semester_uneven['ET'] == etapa])
    else:
        genome_size_even += len(dataset_courseSchedule_semester_even[dataset_courseSchedule_semester_even['ET'] == etapa])
        genome_size_uneven += len(dataset_courseSchedule_semester_uneven[dataset_courseSchedule_semester_uneven['ET'] == etapa])
    
if semester == "even":
    dataset_courseSchedule_semester = dataset_courseSchedule_semester_even
    genome_size = genome_size_even

elif semester == "uneven":
    dataset_courseSchedule_semester = dataset_courseSchedule_semester_uneven
    genome_size = genome_size_uneven

professor_courses = {}
for professor in dataset_professors['CODE']:
    professor_courses[professor] = []
    for index in range(len(dataset_classesPP)):
        if dataset_classesPP['PROFESSOR CODE'][index] == professor:
            professor_courses[professor].append(dataset_classesPP['DISCIPLINA'][index])

# functions
def generate_bit_length(db_length):
    value = 0
    for i in range(10):
        value += 2**i
        if value >= db_length:
            return i+1
        
def get_hex_value(binary):
    # reverse the encoded_part
    reverse_encoded_part = binary[::-1]
    hex_value = 0
    i = 0
    for bit in reverse_encoded_part:
        hex_value += bit*2**i
        i += 1
    return hex_value
        
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
        
def translate_genome(genome, hex_, string_):
    translation_string = []
    translation_hex = []
    for class_scheduling in genome:
        class_index = get_hex_value(get_class_part(class_scheduling))
        class_type_index = get_hex_value(get_class_type_part(class_scheduling))
        class_group_index = get_hex_value(get_class_group_part(class_scheduling))
        professor_index = get_hex_value(get_professor_part(class_scheduling))
        timeslot_day_index = get_hex_value(get_timeslot_day_part(class_scheduling))
        timeslot_index = get_hex_value(get_timeslot_part(class_scheduling))

        if dataset_courseSchedule_semester['ET'][class_index] >= 4:
            class_type_index = 0

        if hex_:
            translation_hex.append({'class:': class_index, 'class_type': class_type_index, 'class_group': class_group_index, 'professor': professor_index, 'timeslot_day': timeslot_day_index, 'timeslot': timeslot_index, 'et': dataset_courseSchedule_semester['ET'][class_index]})
            translation_hex = sorted(translation_hex, key=lambda k: (k['timeslot_day'], k['timeslot']))

        elif string_:
            class_translation = dataset_courseSchedule_semester['DISCIPLINA'][class_index]
            class_type_translation = class_types[class_type_index]
            class_groups_translation = class_groups[class_group_index]
            professor_translation = dataset_professors['CODE'][professor_index]
            timeslot_day_translation = days[timeslot_day_index]
            timeslot_translation = timeslots_day[timeslot_index]

            translation_string.append({'class': class_translation, 'class_type': class_type_translation, 'class_group': class_groups_translation, 'professor': professor_translation, 'timeslot_day': timeslot_day_translation, 'timeslot': timeslot_translation, 'et': dataset_courseSchedule_semester['ET'][class_index]})
            
            # sort the translation based on timeslot_day and timeslot, timeslot_day has to be sorted based on the days list
            translation_string = sorted(translation_string, key=lambda k: (days.index(k['timeslot_day']), k['timeslot']))
            
    if hex_:
        return translation_hex
    if string_:
        return translation_string

        
dataset_courseSchedule_semester = dataset_courseSchedule_semester.reset_index(drop=True)
len_classes_encoding = generate_bit_length(len(dataset_courseSchedule_semester))
len_class_types_encoding = generate_bit_length(len(class_types))
len_class_groups_encoding = generate_bit_length(len(class_groups))
len_professors_encoding = generate_bit_length(len(dataset_professors))
len_timeslots_day_encoding = generate_bit_length(len(days))
len_timeslots_encoding = generate_bit_length(len(timeslots_day))

def generate_binary(length, db):
    binary_value = 100000
    binary_part = []
    while binary_value >= len(db):
        i = 0
        binary_part = choices([0,1], k=length)
        binary_value = 0
        reverse_binary_part = binary_part[::-1]
        for bit in reverse_binary_part:
            binary_value += bit*2**i
            i += 1
    return binary_part

def create_genome_part():
    binary_class = generate_binary(len_classes_encoding, dataset_courseSchedule_semester)
    binary_class_type = generate_binary(len_class_types_encoding, class_types)
    binary_class_group = generate_binary(len_class_groups_encoding, class_groups)
    binary_professor = generate_binary(len_professors_encoding, dataset_professors)
    binary_timeslot_day = generate_binary(len_timeslots_day_encoding, days)
    binary_timeslot = generate_binary(len_timeslots_encoding, timeslots_day)
    genome = binary_class + binary_class_type + binary_class_group + binary_professor + binary_timeslot_day + binary_timeslot
    return genome

def print_translation(translation):
    for class_scheduling in translation:
        print(class_scheduling)

def generate_genome(size):
    return [create_genome_part() for i in range(size)]

def generate_population(population_size):
    population = []
    for i in range(population_size):
        population.append(generate_genome(genome_size))
    return population

def run_genetic_algorithm(generation_limit, fitness_limit):
    # population = generate_population(20)
    test_genome = generate_genome(genome_size)
    translated_genome_string = translate_genome(test_genome, False, True)
    translated_genome_hex = translate_genome(test_genome, True, False)
    print('Translated genome string:')
    print_translation(translated_genome_string)
    print('Translated genome hex:')
    print_translation(translated_genome_hex)

run_genetic_algorithm(generation_limit=100, fitness_limit=25)