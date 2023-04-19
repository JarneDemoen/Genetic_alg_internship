# imports
import random
import pandas as pd
from random import choices, randint
import os

# making sure the file is in the same directory as the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Inputs user
semester = "uneven"
timeslots_per_day = [
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
timeslots = [timeslots_per_day for i in range(len(days))]
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

professor_classes = {}
for professor in dataset_professors['CODE']:
    professor_classes[professor] = []
    for index in range(len(dataset_classesPP)):
        if dataset_classesPP['PROFESSOR CODE'][index] == professor:
            professor_classes[professor].append(dataset_classesPP['DISCIPLINA'][index])

professor_availability = {}
for professor in dataset_professors['CODE']:
    professor_availability[professor] = []
    for day in days:
        for timeslot in timeslots_per_day:
            # with a probability of 0.5 the professor is available
            if choices([True, False], weights=[0.5, 0.5], k=1)[0]:
                professor_availability[professor].append(day + "-" + timeslot)

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
        
def translate_genome(genome, hex_= False, string_= False, chronological = False):
    
    translation_string = []
    translation_hex = []
    for class_scheduling in genome:
        class_index = get_hex_value(get_class_part(class_scheduling))
        class_type_index = get_hex_value(get_class_type_part(class_scheduling))
        class_group_index = get_hex_value(get_class_group_part(class_scheduling))
        professor_index = get_hex_value(get_professor_part(class_scheduling))
        timeslot_day_index = get_hex_value(get_timeslot_day_part(class_scheduling))
        timeslot_index = get_hex_value(get_timeslot_part(class_scheduling))

        if class_index >= len(dataset_courseSchedule_semester) or class_type_index >= len(class_types) or class_group_index >= len(class_groups) or professor_index >= len(dataset_professors) or timeslot_day_index >= len(days) or timeslot_index >= len(timeslots_per_day):
            return False

        if dataset_courseSchedule_semester['ET'][class_index] >= 4:
            class_group_index = 0

        if hex_:
            translation_hex.append({'class': class_index, 'class_type': class_type_index, 'class_group': class_group_index, 'professor': professor_index, 'timeslot_day': timeslot_day_index, 'timeslot': timeslot_index, 'et': dataset_courseSchedule_semester['ET'][class_index]})
            if chronological:
                translation_hex = sorted(translation_hex, key=lambda k: (k['timeslot_day'], k['timeslot']))

        elif string_:
            class_translation = dataset_courseSchedule_semester['DISCIPLINA'][class_index]
            class_type_translation = class_types[class_type_index]
            class_groups_translation = class_groups[class_group_index]
            professor_translation = dataset_professors['CODE'][professor_index]
            timeslot_day_translation = days[timeslot_day_index]
            timeslot_translation = timeslots_per_day[timeslot_index]

            translation_string.append({'class': class_translation, 'class_type': class_type_translation, 'class_group': class_groups_translation, 'professor': professor_translation, 'timeslot_day': timeslot_day_translation, 'timeslot': timeslot_translation, 'et': dataset_courseSchedule_semester['ET'][class_index]})
            
            if chronological:
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
len_timeslots_encoding = generate_bit_length(len(timeslots_per_day))

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
    binary_timeslot = generate_binary(len_timeslots_encoding, timeslots_per_day)
    genome = binary_class + binary_class_type + binary_class_group + binary_professor + binary_timeslot_day + binary_timeslot
    return genome

def print_per_line(translation):
    for class_scheduling in translation:
        print(class_scheduling)

def generate_genome(size):
    return [create_genome_part() for i in range(size)]

def generate_population(population_size):
    population = []
    for i in range(population_size):
        population.append(generate_genome(genome_size))
    return population

# functions to determine the fitness of a genome

def get_violation_count_assigning_professor(genome):
    # print("Professor classes")
    # print(professor_classes)
    # print("------------------")
    violations = 0
    for class_scheduling in genome:
        professor = class_scheduling['professor']
        class_name = class_scheduling['class'][:5]
        if class_name not in professor_classes[professor]:
            violations += 1
            # print(f"The professor {professor} is not competent of teaching {class_name}")

    return violations

def get_violation_count_class_scheduling(genome):
    violations = 0
    for index_class in range(len(dataset_courseSchedule_semester)):
        nr_at = {}
        nr_ap = {}
        nr_av = {}

        if dataset_courseSchedule_semester['ET'][index_class] >= 4:
            class_groups_copy = ['A']
        else:
            class_groups_copy = class_groups

        for class_group in class_groups_copy:
            nr_at[class_group] = dataset_courseSchedule_semester['AT'][index_class]
            nr_ap[class_group] = dataset_courseSchedule_semester['AP'][index_class]
            nr_av[class_group] = dataset_courseSchedule_semester['AV'][index_class]

        for class_scheduling in genome:
            if class_scheduling['class'] == dataset_courseSchedule_semester['DISCIPLINA'][index_class]:
                if class_scheduling['class_type'] == "AT":
                    nr_at[class_scheduling['class_group']] -= 1
                elif class_scheduling['class_type'] == "AP":
                    nr_ap[class_scheduling['class_group']] -= 1
                elif class_scheduling['class_type'] == "AV":
                    nr_av[class_scheduling['class_group']] -= 1
        
        # the number of the violations is equal to the sum of all of the absolute values in the dictionaries
        for values in nr_at.values():
            violations += abs(values)

        for values in nr_ap.values():
            violations += abs(values)

        for values in nr_av.values():
            violations += abs(values)
       
        # print("Class: ", dataset_courseSchedule_semester['DISCIPLINA'][index_class])
        # print("nr_at: ", nr_at)
        # print("nr_ap: ", nr_ap)
        # print("nr_av: ", nr_av)
        # print("Violations: ", violations)
        # print("")
    return violations

def get_violation_count_saturday_classes(genome):
    violations = 0
    for class_scheduling in genome:
        if class_scheduling['timeslot_day'] == "Saturday":
            violations += 1
    return violations

def get_violation_count_consecutive_classes(genome):
    violations = 0
    for index_day in range(len(days)):
        classes_day = [x for x in genome if x['timeslot_day'] == index_day]

        if len(classes_day) == 0:
            continue

        for i in range(len(classes_day) - 1):
            current_timeslot = classes_day[i]['timeslot']
            next_timeslot = classes_day[i+1]['timeslot']
            
            current_class = classes_day[i]['class']
            next_class = classes_day[i+1]['class']

            current_class_type = classes_day[i]['class_type']
            next_class_type = classes_day[i+1]['class_type']

            current_class_group = classes_day[i]['class_group']
            next_class_group = classes_day[i+1]['class_group']

            current_professor = classes_day[i]['professor']
            next_professor = classes_day[i+1]['professor']

            if current_timeslot == next_timeslot:
                if current_class != next_class:
                    violations += 1

                if current_class_type != next_class_type:
                    violations += 1
                else:
                    if current_class_type == "AP":
                        violations += 1

                if current_class_group == next_class_group and dataset_courseSchedule_semester.iloc[current_class]['ET'] < 4 and dataset_courseSchedule_semester.iloc[next_class]['ET'] < 4:
                    violations += 1

                if current_professor != next_professor:
                    violations += 1

                continue

            if current_timeslot != next_timeslot - 1:
                violations += 1
            
            if current_class != next_class:
                violations += 1

            if current_class_type != next_class_type:
                violations += 1

            if current_class_group != next_class_group:
                violations += 1

            if current_professor != next_professor:
                violations += 1

    return violations

def get_violation_count_professor_availability(genome):
    violations = 0
    for class_scheduling in genome:
        professor = class_scheduling['professor']
        timeslot_day = class_scheduling['timeslot_day']
        timeslot = class_scheduling['timeslot']
        check_string = timeslot_day + "-" + timeslot
        if check_string not in professor_availability[professor]:
            violations += 1

    return violations
            

def calculate_fitness_score(genome):
    translated_genome = translate_genome(genome, string_=True, chronological=True)
    hex_genome = translate_genome(genome, hex_=True, chronological=True)

    violations_assingning_professor = get_violation_count_assigning_professor(translated_genome)
    violations_class_scheduling_count = get_violation_count_class_scheduling(translated_genome)
    violations_saturday_classes = get_violation_count_saturday_classes(translated_genome)
    # violations_consecutive_classes = get_violation_count_consecutive_classes(hex_genome)
    violations_availability_professor = get_violation_count_professor_availability(translated_genome)

    # print("Violations assingning professor: ", violations_assingning_professor)
    # print("Violation class scheduling count: ", violations_class_scheduling_count)
    # print("Violation saturday classes: ", violations_saturday_classes)
    # print("Violation consecutive classes: ", violations_consecutive_classes)
    # print("Violation professor availability: ", violations_availability_professor)

    total_violations = violations_assingning_professor + violations_class_scheduling_count + violations_saturday_classes + violations_availability_professor
    return 1/(1+total_violations)

def select_parents(population, fitness):
    return choices(
        population=population,
        weights=[fitness(genome) for genome in population],
        k=2
    )

def crossover(parent_a, parent_b):
    # for the crossover function we use a single-point crossover
    # we choose a random index in the genome and we swap the genes after that index
    if len(parent_a) != len(parent_b):
        raise Exception("The parents must have the same length")
    
    length = len(parent_a)
    if length < 2:
        raise ValueError("Genome must be at least 2 bits long")
    
    split_index = randint(1, length - 1)
   
    offspring_a = parent_a[0:split_index] + parent_b[split_index:]
    offspring_b = parent_b[0:split_index] + parent_a[split_index:]
    
    return offspring_a, offspring_b

def validate_genome(genome):
    translation = translate_genome(genome, string_=True)
    if translation == False:
        return False
    return True

    
def mutate(genome):
    
                    
    return genome

def run_genetic_algorithm(generation_limit, fitness_limit):
    population = generate_population(20)
    # genome = population[0]
    # translation = translate_genome(genome, string_=True)
    # print_per_line(translation)
    # fitness = calculate_fitness_score(genome)
    # print("Fitness: ", fitness)

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: calculate_fitness_score(genome), reverse=True)

        if calculate_fitness_score(population[0]) >= fitness_limit:
            break

        # elitism
        next_generation = population[0:2]

        # we pick 2 parent and generate 2 children so we loop for half the length of the generation to get as many
        # solutions in our next generation as before, we apply -1 because we saved our top 2 genomes

        for j in range(int(len(population)/2) - 1):
            parents = select_parents(population, calculate_fitness_score)
            offspring_a, offspring_b = crossover(parents[0], parents[1])
            mutated_offspring_a = mutate(offspring_a) 
            mutated_offspring_b = mutate(offspring_b)    
           
            print("Offspring_a: ")
            print_per_line(translate_genome(offspring_a, string_=True))
            print("Mutation offspring_a:")
            print_per_line(translate_genome(mutated_offspring_a, string_=True))
            print("Offspring_b: ")
            print_per_line(translate_genome(offspring_b, string_=True))
            print("Mutation offspring_b:")
            print_per_line(translate_genome(mutated_offspring_b, string_=True))
            break
        break
                
                


run_genetic_algorithm(generation_limit=100, fitness_limit=25)