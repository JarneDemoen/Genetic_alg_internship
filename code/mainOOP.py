# imports 
import numpy as np
import pandas as pd
import os 
import time

# making sure the current working directory is the same as the file path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GenerateClassSchedule:
    def __init__(self, dataset_classes, dataset_competence_teachers, dataset_professor_availability, semester, 
                 timeslots_per_day, class_groups, generation_limit, fitness_limit, mutation_rate, population_size):
        self.dataset_classes = dataset_classes
        self.dataset_competence_teachers = dataset_competence_teachers
        self.dataset_professor_availability = dataset_professor_availability
        self.semester = semester
        self.timeslots_per_day = timeslots_per_day
        self.class_groups = class_groups
        self.generation_limit = generation_limit
        self.fitness_limit = fitness_limit
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.professors = self.dataset_competence_teachers['PROFESSOR CODE'].unique()
        
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        self.dataset_classes_semester = self.get_classes_semester(self.dataset_classes, self.semester)
        self.timeslots_week = [timeslots_per_day for i in range(len(self.days))]
        self.class_types = ["AT", "AP", "AV"]
        self.genome_size = self.get_genome_size(self.dataset_classes_semester)

        self.classes_bit_length = self.get_bit_length(len(self.dataset_classes_semester))
        self.class_types_bit_length = self.get_bit_length(len(self.class_types))
        self.class_groups_bit_length = self.get_bit_length(len(self.class_groups))
        self.professors_bit_length = self.get_bit_length(len(self.professors))
        self.days_bit_length = self.get_bit_length(len(self.days))
        self.timeslots_per_day_bit_length = self.get_bit_length(len(self.timeslots_per_day))
        self.genome_part_bit_length = self.classes_bit_length + self.class_types_bit_length + self.class_groups_bit_length + self.professors_bit_length + self.days_bit_length + self.timeslots_per_day_bit_length

        self.population = np.zeros((self.population_size, self.genome_size, self.genome_part_bit_length), dtype=int)

        self.run_genetic_algorithm()

    def get_bit_length(self, db_size):
        value = 0
        for i in range(10):
            value += 2**i
            if value >= db_size:
                return i+1

    def get_classes_semester(self, dataset_classes, semester):
        if semester == "even":
            return dataset_classes[dataset_classes["ET"] % 2 == 0].reset_index(drop=True)
        
        elif semester == "odd":
            return dataset_classes[dataset_classes["ET"] % 2 != 0].reset_index(drop=True)
        
    def get_genome_size(self, dataset_classes_semester):
        genome_size = 0
        for class_ in dataset_classes_semester['DISCIPLINA']:
            etapa = dataset_classes_semester[dataset_classes_semester['DISCIPLINA'] == class_]['ET'].values[0]
            nr_at = dataset_classes_semester[dataset_classes_semester['DISCIPLINA'] == class_]['AT'].values[0]
            nr_ap = dataset_classes_semester[dataset_classes_semester['DISCIPLINA'] == class_]['AP'].values[0]
            nr_av = dataset_classes_semester[dataset_classes_semester['DISCIPLINA'] == class_]['AV'].values[0]
        
            if etapa < 4:
                genome_size += len(self.class_groups) * (nr_at + nr_ap + nr_av)
            else:
                genome_size += nr_at + nr_ap + nr_av
        
        return genome_size
    
    def get_hex_value(self,binary_code):
        # reverse the encoded_part
        reverse_encoded_part = binary_code[::-1]
        hex_value = 0
        i = 0
        for bit in reverse_encoded_part:
            hex_value += bit*2**i
            i += 1
        return hex_value
    
    def get_class_part(self, class_scheduling):
        return class_scheduling[:self.classes_bit_length]
    
    def get_class_type_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length:self.classes_bit_length+self.class_types_bit_length]
    
    def get_class_group_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length+self.class_types_bit_length:self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length]
    
    def get_professor_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length:self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length+self.professors_bit_length]
    
    def get_day_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length+self.professors_bit_length:self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length+self.professors_bit_length+self.days_bit_length]
    
    def get_timeslot_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length+self.professors_bit_length+self.days_bit_length:self.classes_bit_length+self.class_types_bit_length+self.class_groups_bit_length+self.professors_bit_length+self.days_bit_length+self.timeslots_per_day_bit_length]

    def generate_binary_code(self, bit_length, db_length):
        binary_value = 100000
        binary_code = np.zeros(bit_length, dtype=int)
        while binary_value >= db_length:
            i = 0
            binary_code = np.random.choice([0, 1], size=bit_length)
            binary_value = 0
            reverse_binary_code = binary_code[::-1]
            for bit in reverse_binary_code:
                binary_value += bit*2**i
                i += 1
        return binary_code
    
    def generate_genome_part(self):
        binary_class = self.generate_binary_code(self.classes_bit_length, len(self.dataset_classes_semester))
        binary_class_type = self.generate_binary_code(self.class_types_bit_length, len(self.class_types))
        binary_class_group = self.generate_binary_code(self.class_groups_bit_length, len(self.class_groups))
        binary_professor = self.generate_binary_code(self.professors_bit_length, len(self.professors))
        binary_day = self.generate_binary_code(self.days_bit_length, len(self.days))
        binary_timeslot = self.generate_binary_code(self.timeslots_per_day_bit_length, len(self.timeslots_per_day))

        genome_part = np.concatenate((binary_class, binary_class_type, binary_class_group, binary_professor, binary_day, binary_timeslot))
        return genome_part
    
    def generate_genome(self, genome_size):
        genome = np.zeros((genome_size, self.genome_part_bit_length), dtype=int)
        for i in range(genome_size):
            genome[i] = self.generate_genome_part()
        return genome
    
    def generate_population(self, population_size):
        for i in range(population_size):
            self.population[i] = self.generate_genome(self.genome_size)

    def translate_genome(self, genome, hex_= False, string_= False, chronological= False):
        translation_string = []
        translation_hex = []
        for class_scheduling in genome:
            class_index = self.get_hex_value(self.get_class_part(class_scheduling))
            class_type_index = self.get_hex_value(self.get_class_type_part(class_scheduling))
            class_group_index = self.get_hex_value(self.get_class_group_part(class_scheduling))
            professor_index = self.get_hex_value(self.get_professor_part(class_scheduling))
            day_index = self.get_hex_value(self.get_day_part(class_scheduling))
            timeslot_index = self.get_hex_value(self.get_timeslot_part(class_scheduling))

            if class_index >= len(self.dataset_classes_semester) or class_type_index >= len(self.class_types) or class_group_index >= len(self.class_groups) or professor_index >= len(self.professors) or day_index >= len(self.days) or timeslot_index >= len(self.timeslots_per_day):
                return False
            
            if self.dataset_classes_semester['ET'][class_index] >= 4:
                class_group_index = 0

            if hex_:
                translation_hex.append({'class': class_index, 'class_type': class_type_index, 'class_group': class_group_index, 'professor': professor_index, 'timeslot_day': day_index, 'timeslot': timeslot_index, 'et': self.dataset_classes_semester['ET'][class_index]})
                if chronological:
                    translation_hex = sorted(translation_hex, key=lambda k: (k['timeslot_day'], k['timeslot']))

            elif string_:
                class_translation = self.dataset_classes_semester['DISCIPLINA'][class_index]
                class_type_translation = self.class_types[class_type_index]
                class_groups_translation = self.class_groups[class_group_index]
                professor_translation = self.professors[professor_index]
                timeslot_day_translation = self.days[day_index]
                timeslot_translation = self.timeslots_per_day[timeslot_index]

                translation_string.append({'class': class_translation, 'class_type': class_type_translation, 'class_group': class_groups_translation, 'professor': professor_translation, 'timeslot_day': timeslot_day_translation, 'timeslot': timeslot_translation, 'et': self.dataset_classes_semester['ET'][class_index]})
                
                if chronological:
                    translation_string = sorted(translation_string, key=lambda k: (self.days.index(k['timeslot_day']), k['timeslot']))
            
        if hex_:
            return translation_hex
        if string_:
            return translation_string
        
    def get_violation_count_assigning_professor(self, genome):
        violations = 0
        for class_scheduling in genome:
            professor = class_scheduling['professor']
            class_name = class_scheduling['class'][:5]
            if class_name not in self.dataset_competence_teachers[self.dataset_competence_teachers['PROFESSOR CODE'] == professor]['DISCIPLINA'].values:
                violations += 1

        return violations

    def calculate_fitness_score(self, genome):
        translated_genome = self.translate_genome(genome, string_=True, chronological=True)
        hex_genome = self.translate_genome(genome, hex_=True, chronological=True)

        violations = self.get_violation_count_assigning_professor(translated_genome)
        return 1/(1+violations)
    
    
    def select_parents(self, population, fitness_function):
        # calculate the fitness values for each genome in the population
        fitness_values = np.array([fitness_function(genome) for genome in population])
        
        # select two parents using the fitness values as weights
        parents_indices = np.random.choice(len(population), size=2, replace=True, p=fitness_values/fitness_values.sum())
        
        # return the selected parents
        return population[parents_indices[0]], population[parents_indices[1]]
    
    def crossover(self, parent_a, parent_b):
        offspring_a = np.zeros((self.genome_size, self.genome_part_bit_length), dtype=int)
        offspring_b = np.zeros((self.genome_size, self.genome_part_bit_length), dtype=int)
        
        for index_class_scheduling in range(len(parent_a)):
            offspring_class_a = np.empty([self.genome_part_bit_length], dtype=int)
            offspring_class_b = np.empty([self.genome_part_bit_length], dtype=int)

            genome_parts = [self.get_class_part, self.get_class_type_part, self.get_class_group_part, self.get_professor_part, self.get_day_part, self.get_timeslot_part]
            split_index = np.random.randint(0, len(genome_parts) - 2)

            for i in range(split_index + 1):
                offspring_class_a = np.vstack((offspring_class_a, genome_parts[i](parent_a[index_class_scheduling])))
                offspring_class_b = np.vstack((offspring_class_b, genome_parts[i](parent_b[index_class_scheduling])))

            for i in range(split_index + 1, len(genome_parts)):
                offspring_class_a = np.vstack((offspring_class_a, genome_parts[i](parent_b[index_class_scheduling])))
                offspring_class_b = np.vstack((offspring_class_b, genome_parts[i](parent_a[index_class_scheduling])))

            offspring_a[index_class_scheduling] = offspring_class_a
            offspring_b[index_class_scheduling] = offspring_class_b

        return offspring_a, offspring_b
    
    def run_genetic_algorithm(self):
        self.generate_population(self.population_size)
        
        for i in range(self.generation_limit):
            self.population = sorted(self.population, key=lambda genome: self.calculate_fitness_score(genome), reverse=True)
            print("Generation: ", i+1)
            if self.calculate_fitness_score(self.population[0]) >= self.fitness_limit:
                break
            print("Best fitness score: ", self.calculate_fitness_score(self.population[0]))

            # elitism
            next_generation = self.population[0:2]

            # we pick 2 parent and generate 2 children so we loop for half the length of the generation to get as many
            # solutions in our next generation as before, we apply -1 because we saved our top 2 genomes

            for j in range(int(len(self.population)/2)-1):
                parents = self.select_parents(self.population, self.calculate_fitness_score)
                offspring_a, offspring_b = self.crossover(parents[0], parents[1])

# User inputs
dataset_classes = pd.read_csv('../data/ClassesNoDuplicates.csv', sep=';')
dataset_classes = dataset_classes.sort_values(by=['ET'])
dataset_competence_teachers = pd.read_csv('../data/ClassesPP.csv', sep=';')
semester = "odd"
timeslots_per_day = [
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]
class_groups = ["A", "B"]
generation_limit = 100
fitness_limit = 1
mutation_rate = 0.005
population_size = 30

class_schedule = GenerateClassSchedule(dataset_classes=dataset_classes, dataset_competence_teachers=dataset_competence_teachers,
                                       dataset_professor_availability=None ,semester=semester, timeslots_per_day=timeslots_per_day, 
                                       class_groups=class_groups, generation_limit=generation_limit, fitness_limit=fitness_limit,
                                       mutation_rate=mutation_rate,population_size=population_size)
            