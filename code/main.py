import pandas as pd
from random import choices, randint
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
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
class_types = ["AT", "AP", "AV"]
class_groups = ["A","B"]

# create a pandas dataframe where you combine the timeslots and days
timeslots = [timeslots_day for i in range(len(days))]

# create a dictionary where all of the courses that a teacher teaches are stored
professor_courses = {}
for professor in dataset_professors['CODE']:
    # professor_code = str(professor)
    # # the lenght of the professor code has to be 6, if not, add 0's to the right
    # while len(professor_code) < 6:
    #     professor_code += "0"
    professor_courses[professor] = []
    for index in range(len(dataset_subjectsPP)):
        if dataset_subjectsPP['PROFESSOR CODE'][index] == professor:
            professor_courses[professor].append(dataset_subjectsPP['DISCIPLINA'][index])


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

def generate_genome():
    # determine here how much classes you want to schedule according to the number of class groups
    size = "?"
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

def get_class_scheduling_count(translated_genome):
    score = 0

    for index_class in range(len(dataset_courseSchedule_semester)):
        nr_at = {}
        nr_ap = {}
        nr_av = {}

        for class_group in class_groups:
            nr_at[class_group] = dataset_courseSchedule_semester['AT'][index_class]
            nr_ap[class_group] = dataset_courseSchedule_semester['AP'][index_class]
            nr_av[class_group] = dataset_courseSchedule_semester['AV'][index_class]

        for class_scheduling in translated_genome:
            if class_scheduling['class'] == dataset_courseSchedule_semester['DISCIPLINA'][index_class] and class_scheduling['class_type'] == "AT":
                nr_at[class_scheduling['class_group']] -= 1

            if class_scheduling['class'] == dataset_courseSchedule_semester['DISCIPLINA'][index_class] and class_scheduling['class_type'] == "AP":
                nr_ap[class_scheduling['class_group']] -= 1

            if class_scheduling['class'] == dataset_courseSchedule_semester['DISCIPLINA'][index_class] and class_scheduling['class_type'] == "AV":
                nr_av[class_scheduling['class_group']] -= 1

        # if the values in the dictionary are all 0, then the class is scheduled correctly
        if all(value == 0 for value in nr_at.values()) and all(value == 0 for value in nr_ap.values()) and all(value == 0 for value in nr_av.values()):
            score += 1
            # print("class: ", dataset_courseSchedule_semester['DISCIPLINA'][index_class])
            # print("nr_at: ", nr_at)
            # print("nr_ap: ", nr_ap)
            # print("nr_av: ", nr_av)
            # print("---------------------")

    return score


def translate_genome(genome):
    translation = []
    for class_scheduling in genome:
        class_part_value = get_binary_value_class_scheduling_part(get_class_part(class_scheduling))
        class_type_part = get_binary_value_class_scheduling_part(get_class_type_part(class_scheduling))
        class_group_part = get_binary_value_class_scheduling_part(get_class_group_part(class_scheduling))
        professor_part_value = get_binary_value_class_scheduling_part(get_professor_part(class_scheduling))
        timeslots_day_part_value = get_binary_value_class_scheduling_part(get_timeslot_day_part(class_scheduling))
        timeslots_part_value = get_binary_value_class_scheduling_part(get_timeslot_part(class_scheduling))

        # if the et value of the class_part_value in the dataset is 4 or more, then the value is always 0
        if dataset_courseSchedule_semester['ET'][class_part_value] >= 4:
            class_group_part = 0

        class_part_translation = dataset_courseSchedule_semester['DISCIPLINA'][class_part_value]
        class_type_translation = class_types[class_type_part]
        class_group_translation = class_groups[class_group_part]
        professor_part_translation = dataset_professors['CODE'][professor_part_value]
        timeslots_day_part_translation = days[timeslots_day_part_value]
        timeslots_part_translation = timeslots_day[timeslots_part_value]

        # return the translated data of the genome in a dictionary
        translation.append({"class": class_part_translation,"class_type":class_type_translation,"class_group":class_group_translation,"professor": professor_part_translation, "timeslot_day": timeslots_day_part_translation, "timeslot": timeslots_part_translation, "et": dataset_courseSchedule_semester['ET'][class_part_value]})
        # sort the translation by timeslot_day and timeslot
        translation = sorted(translation, key=lambda k: (k['timeslot_day'], k['timeslot']))
        
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

        # if the et value of the class_part_value in the dataset is 4 or more, then the value is always 0
        if dataset_courseSchedule_semester['ET'][class_part_value] >= 4:
            class_group_part = 0

        translation.append({"class": class_part_value,"class_type":class_type_part,"class_group":class_group_part,"professor": professor_part_value, "timeslot_day": timeslots_day_part_value, "timeslot": timeslots_part_value, "et": dataset_courseSchedule_semester['ET'][class_part_value]})

    # sort the translation based on the timeslot_day and timeslot
    translation = sorted(translation, key=lambda k: (k['timeslot_day'], k['timeslot']))
    return translation

def emergency_saturday_class(hex_genome):
    # sort the dictionary of the hex_genome based on the timeslot_day and timeslot
    hex_genome_sorted = sorted(hex_genome, key=lambda k: (k['timeslot_day'], k['timeslot']))
    score = 0
    # check if there are classes on saturday
    classes_day = [x for x in hex_genome_sorted if x['timeslot_day'] == 5]

    if len(classes_day) == 0:
        score += 3

    return score

def check_100_rule(hex_genome):
    # sort the dictionary of the hex_genome based on the timeslot_day and timeslot
    hex_genome_sorted = sorted(hex_genome, key=lambda k: (k['timeslot_day'], k['timeslot']))
    score = 0
    # check if there are classes on 2 following timeslots
    for index_day in range(len(days)):
        # return a dictionary with the classes of the day
        classes_day = [x for x in hex_genome_sorted if x['timeslot_day'] == index_day]
        # print("classes_day: ", classes_day)
        # print("------------------")
        # check if there are classes that day, if not, continue, it could be that there are no classes on that day, score stays 0
        if len(classes_day) == 0:
            continue

        for i in range(len(classes_day) - 1): # index to compare to 2 courses being taught on the same day
            for index_timeslot in range(len(timeslots_day)):
                if classes_day[i]['timeslot'] == index_timeslot and classes_day[i+1]['timeslot'] == index_timeslot + 1:
                    if classes_day[i]['class'] == classes_day[i+1]['class'] and classes_day[i]['class_type'] == classes_day[i+1]['class_type'] and classes_day[i]['class_group'] == classes_day[i+1]['class_group'] and classes_day[i]['professor'] == classes_day[i+1]['professor']:
                        # print("Great! 2 of the same classes are being taught on successive timeslots!")
                        # print("classes_day[i]: ", classes_day[i])
                        # print("classes_day[i+1]: ", classes_day[i+1])
                        # print("------------------")
                        score += 1
    return score

def check_professor_scheduling(translated_genome):
    score = 0
    for class_scheduling in translated_genome:
        for professor in professor_courses:
            class_name = class_scheduling['class'][:5]
            if class_name in professor_courses[professor]:
                if class_scheduling['professor'] == professor:
                    score += 1
                    # print("Great! The professor is teaching the class!")
                    # print("class_scheduling: ", class_scheduling)
                    # print("------------------")
    return score
                    

def schedule_at(hex_genome):
    score = 0
    
    for index_day in range(len(days)):
        for index_timeslot in range(len(timeslots_day)):
            classes_day_timeslot = [x for x in hex_genome if x['timeslot_day'] == index_day and x['timeslot'] == index_timeslot]
            if len(classes_day_timeslot) > 1:
                # compare all of the classes with each other, if the classes are the same, the score is deducted by one
                for i in range(len(classes_day_timeslot) - 1):
                    for j in range(i + 1, len(classes_day_timeslot)):
                        if classes_day_timeslot[i]['class'] == classes_day_timeslot[j]['class']:
                            if classes_day_timeslot[i]['class_type'] == classes_day_timeslot[j]['class_type'] and classes_day_timeslot[i]['class_type'] == 0 and classes_day_timeslot[i]['class_group'] != classes_day_timeslot[j]['class_group'] and classes_day_timeslot[i]['professor'] == classes_day_timeslot[j]['professor']:
                                # print("Correctly scheduled AT class")
                                # print(classes_day_timeslot[i])
                                # print(classes_day_timeslot[j])
                                # print("------------------")
                                score += 1
    return score

def print_translation(translation):
    for class_scheduling in translation:
        print(class_scheduling)

def fitness(genome):
    hex_genome = translate_genome_to_hex(genome)
    translation = translate_genome(genome)

    score_100_rule = check_100_rule(hex_genome)
    score_schedule_at = schedule_at(hex_genome)
    score_emergency_saturday_class = emergency_saturday_class(hex_genome)
    score_class_scheduling_count = get_class_scheduling_count(translation)
    score_professor_scheduling = check_professor_scheduling(translation)

    total_score = score_100_rule + score_schedule_at + score_emergency_saturday_class + score_class_scheduling_count + score_professor_scheduling
    # return {"total_score": total_score, "score_100_rule": score_100_rule, "score_schedule_at": score_schedule_at, "score_emergency_saturday_class": score_emergency_saturday_class, "score_class_scheduling_count": score_class_scheduling_count, "score_professor_scheduling": score_professor_scheduling}
    return total_score

dataset_courseSchedule_semester = dataset_courseSchedule_semester_even
# reindex the database
dataset_courseSchedule_semester = dataset_courseSchedule_semester.reset_index(drop=True)
len_classes_encoding = generate_bit_length(len(dataset_courseSchedule_semester))
len_class_types_encoding = generate_bit_length(len(class_types))
len_class_groups_encoding = generate_bit_length(len(class_groups))
len_professors_encoding = generate_bit_length(len(dataset_professors))
len_timeslots_day_encoding = generate_bit_length(len(days))
len_timeslots_encoding = generate_bit_length(len(timeslots_day))

def generate_population(population_size):
    population = []
    for i in range(population_size):
        population.append(generate_genome())
    return population

def select_parents(population, fitness):
    return choices(
        population=population,
        weights=[fitness(genome) for genome in population],
        k=2
    )

def crossover(parent_a, parent_b):
    # for the crossover function we use a single-point crossover
    # we pick a random index in the genome and split the genome into two parts
    # the first part is from the first parent and the second part is from the second parent
    # we then combine the two parts to get the two children
    # we use the same index for both parents to ensure that the children are the same length as the parents
    if len(parent_a) != len(parent_b):
        raise ValueError("Genomes must be the same length")
    
    length = len(parent_a)
    if length < 2:
        raise ValueError("Genomes must be at least 2 bits long")
    
    split = randint(1, length - 1)
    return parent_a[0:split] + parent_b[split:], parent_b[0:split] + parent_a[split:]

def mutate(genome):
    pass

def check_validity(genome):
    if translate_genome(genome):
        return True
    return False

def run_genetic_algorithm(generation_limit, fitness_limit):
    population = generate_population(20)
    
    for i in range(generation_limit):
        population = sorted(
            population,
            key=lambda genome: fitness(genome),
            reverse=True
        )

        if fitness(population[0]) >= fitness_limit:
            break

        # elitisim
        next_generation = population[0:2]

        # we pick 2 parents and generate 2 children so we loop for half the length of a generation to get as many
        # solutions in our next generation as before, we apply -1 because we saved our top 2 genomes

        for j in range(int(len(population)/2) - 1):
            parents = select_parents(population, fitness)
            valid_children = False
            while not valid_children:
                offspring_a, offspring_b = crossover(parents[0], parents[1])
                # offspring_a = mutate(offspring_a)
                # offspring_b = mutate(offspring_b)
                valid_children = check_validity(offspring_a) and check_validity(offspring_b)
            print("Parent A: ")
            print_translation(translate_genome(parents[0]))
            print("------------------")
            print("Parent B: ")
            print_translation(translate_genome(parents[1]))
            print("------------------")
            print("Offspring A: ")
            print_translation(translate_genome(offspring_a))
            print("------------------")
            print("Offspring B: ")
            print_translation(translate_genome(offspring_b))
            


    
run_genetic_algorithm(generation_limit=100, fitness_limit=25)