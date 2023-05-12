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
        self.dict_competence_teachers = self.get_competence_teachers(self.dataset_competence_teachers)
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
        self.best_solution, self.generations = self.run_genetic_algorithm()

    def get_competence_teachers(self, dataset_competence_teachers):
        competence_teachers_dict = {}
        for professor in dataset_competence_teachers['PROFESSOR CODE'].unique():
            competence_teachers_dict[professor] = []
            for index in range(len(dataset_competence_teachers)):
                if dataset_competence_teachers['PROFESSOR CODE'][index] == professor:
                    competence_teachers_dict[professor].append(dataset_competence_teachers['DISCIPLINA'][index])
        return competence_teachers_dict
    
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
        
        return int(genome_size/2)
    
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
            professor = self.professors[class_scheduling['professor']]
            class_name = self.dataset_classes_semester['DISCIPLINA'][class_scheduling['class']]
            if class_name not in self.dict_competence_teachers[professor]:
                violations += 1

        return violations
    
    def get_violation_count_saturday_classes(self,genome):
        violations = 0
        for class_scheduling in genome:
            if class_scheduling['timeslot_day'] == 5:
                violations += 0.2
        return violations
    
    def get_violation_count_assigning_classes(self, genome):
        violations = 0
        for index_class in range(len(self.dataset_classes_semester)):
            nr_at = {}
            nr_ap = {}
            nr_av = {}
            class_name = self.dataset_classes_semester['DISCIPLINA'][index_class]

            if self.dataset_classes_semester['ET'][index_class] >= 4:
                class_groups = ['A']
            else:
                class_groups = self.class_groups

            for class_group in class_groups:
                nr_at[class_group] = int(self.dataset_classes_semester['AT'][index_class]/2)
                nr_ap[class_group] = int(self.dataset_classes_semester['AP'][index_class]/2)
                nr_av[class_group] = int(self.dataset_classes_semester['AV'][index_class]/2)

            for class_scheduling in genome:
                for i in range(len(class_groups)):
                    if class_scheduling['class_group'] == i:
                        class_group = class_groups[i]
                        break
                if class_scheduling['class'] == index_class:
                    if class_scheduling['class_type'] == 0:
                        nr_at[class_group] -= 1
                    elif class_scheduling['class_type'] == 1:
                        nr_ap[class_group] -= 1
                    elif class_scheduling['class_type'] == 2:
                        nr_av[class_group] -= 1

            for values in nr_at.values():
                violations += abs(values)

            for values in nr_ap.values():
                violations += abs(values)

            for values in nr_av.values():
                violations += abs(values)

        return violations
    
    def calculate_fitness_score(self, genome):
        hex_genome = self.translate_genome(genome, hex_=True, chronological=True)
        self.translated_genome = self.translate_genome(genome, string_=True, chronological=True)
        violations = 0
        violations += self.get_violation_count_saturday_classes(hex_genome)
        violations += self.get_violation_count_assigning_professor(hex_genome)
        violations += self.get_violation_count_assigning_classes(hex_genome)
        return 1/(1+violations)

    def run_genetic_algorithm(self):
        self.generate_population(self.population_size)
        
        for i in range(self.generation_limit):
            # sort the population based on the fitness score of each genome, make us of the numpy arrays
            self.population = self.population[np.argsort([self.calculate_fitness_score(genome) for genome in self.population])][::-1]
            print("Generation: ", i+1)
            if self.calculate_fitness_score(self.population[0]) >= self.fitness_limit:
                break
            print("Best fitness score: ", self.calculate_fitness_score(self.population[0]))

            next_generation = np.empty((self.population_size, self.genome_size, self.genome_part_bit_length), dtype=object)

            index_generation = 0

            # elitism
            next_generation[index_generation] = self.population[0]
            index_generation += 1
            next_generation[index_generation] = self.population[1]
            index_generation += 1

            # we pick 2 parent and generate 2 children so we loop for half the length of the generation to get as many
            # solutions in our next generation as before, we apply -1 because we saved our top 2 genomes

            for j in range(int(len(self.population)/2)-1):
                parents = self.select_parents(self.population, self.calculate_fitness_score)
                offspring_a, offspring_b = self.crossover(parents[0], parents[1])
                
                mutated_offspring_a = self.mutate(offspring_a, self.mutation_rate)
                mutated_offspring_b = self.mutate(offspring_b, self.mutation_rate)

                next_generation[index_generation] = mutated_offspring_a
                index_generation += 1
                next_generation[index_generation] = mutated_offspring_b
                index_generation += 1
            
            self.population = next_generation

        self.population = self.population[np.argsort([self.calculate_fitness_score(genome) for genome in self.population])][::-1]

        return self.population[0], i+1
    
    def select_parents_old(self, population, fitness_function):
        # calculate the fitness values for each genome in the population
        fitness_values = np.array([fitness_function(genome) for genome in population])
        
        # select two parents using the fitness values as weights
        parents_indices = np.random.choice(len(population), size=2, replace=True, p=fitness_values/fitness_values.sum())
        
        # return the selected parents
        return population[parents_indices[0]], population[parents_indices[1]]
    
    def select_parents(self, population, fitness_function):
        # Only choose out of the top half ranked on fitness values
        fitness_values = np.array([fitness_function(genome) for genome in population[:int(self.population_size/2)]])

        # select two parents using the fitness values as weights
        parents_indices = np.random.choice(int(self.population_size/2), size=2, replace=True, p=fitness_values/fitness_values.sum())

        # return the selected parents
        return population[parents_indices[0]], population[parents_indices[1]]
    
    def crossover(self, parent_a, parent_b):
        offspring_a = np.empty((self.genome_size, self.genome_part_bit_length), dtype=object)
        offspring_b = np.empty((self.genome_size, self.genome_part_bit_length), dtype=object)

        for index_class_scheduling in range(len(parent_a)):
            genome_parts = [self.get_class_part, self.get_class_type_part, self.get_class_group_part, self.get_professor_part, self.get_day_part, self.get_timeslot_part]

            offspring_class_a = np.empty(len(genome_parts), dtype=object)
            offspring_class_b = np.empty(len(genome_parts), dtype=object)
            split_index = np.random.randint(0, len(genome_parts) - 2)

            for i in range(split_index + 1):
                offspring_class_a[i] = genome_parts[i](parent_a[index_class_scheduling])
                offspring_class_b[i] = genome_parts[i](parent_b[index_class_scheduling])

            for i in range(split_index + 1, len(genome_parts)):
                offspring_class_a[i] = genome_parts[i](parent_b[index_class_scheduling])
                offspring_class_b[i] = genome_parts[i](parent_a[index_class_scheduling])

            offspring_class_a = np.concatenate(offspring_class_a)
            offspring_class_b = np.concatenate(offspring_class_b)
            
            offspring_a[index_class_scheduling] = offspring_class_a
            offspring_b[index_class_scheduling] = offspring_class_b

        return offspring_a, offspring_b
    
    def validate_genome(self, genome):
        translation = self.translate_genome(genome, string_=True)
        if translation == False:
            return False
        return True
    
    def mutate(self,genome,mutation_rate):
        # calculate the fitness score of the genome
        fitness_score = self.calculate_fitness_score(genome)
        for i in range(genome.shape[0]):
            for j in range(genome.shape[1]):
                if np.random.rand() < mutation_rate:
                    genome[i][j] = 1 - genome[i][j]
                    valid_mutation = self.validate_genome(genome)
                    if not valid_mutation:
                        genome[i][j] = 1 - genome[i][j]
                    else:
                        fitness_score_mutated = self.calculate_fitness_score(genome)
                        if fitness_score_mutated < fitness_score:
                            genome[i][j] = 1 - genome[i][j]
        return genome
    
    def print_per_line(self,genome):
        for i in genome:
            print(i)
                
# User inputs
input_dataset_classes = pd.read_csv('../data/ClassesNoDuplicates.csv', sep=';')
input_dataset_classes = input_dataset_classes.sort_values(by=['ET'])
input_dataset_competence_teachers = pd.read_csv('../data/ClassesPP.csv', sep=';')

input_semester = "odd"
# input_timeslots_per_day = [
#     "19:00-19:50",
#     "19:50-20:40",
#     "20:55-21:45",
#     "21:45-22:35"]

input_timeslots_per_day = [
    "19:00-20:40",
    "20:55-22:35",]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']

input_professor_availability = {}
for professor in input_dataset_competence_teachers['PROFESSOR CODE'].unique():
    input_professor_availability[professor] = []
    for day in days:
        for timeslot in input_timeslots_per_day:
            if np.random.choice([True, False], p=[0.42, 0.58]):
                input_professor_availability[professor].append({'day': day, 'timeslot': timeslot})

# for professor in input_professor_availability:
#     print("Professor: ", professor)
#     for i in input_professor_availability[professor]:
#         print(i)
#     print("------------------")
    

input_class_groups = ["A", "B"]
input_generation_limit = 100000
input_fitness_limit = 1
input_mutation_rate = 0.0075
input_population_size = 10

start = time.time()

class_schedule = GenerateClassSchedule(dataset_classes=input_dataset_classes, dataset_competence_teachers=input_dataset_competence_teachers,
                                       dataset_professor_availability=None ,semester=input_semester, timeslots_per_day=input_timeslots_per_day, 
                                       class_groups=input_class_groups, generation_limit=input_generation_limit, fitness_limit=input_fitness_limit,
                                       mutation_rate=input_mutation_rate,population_size=input_population_size)
end = time.time()

print("Generations: ", class_schedule.generations)
print("Time: ", end - start)
print("Best solution: ")
class_schedule.print_per_line(class_schedule.translate_genome(class_schedule.best_solution, string_=True, chronological=True))