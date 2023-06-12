# imports 
import numpy as np
import pandas as pd
import os 

# making sure the current working directory is the same as the file path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GenerateClassSchedule:
    def __init__(self, dataset_classes, dataset_competence_teachers, dataset_professor_availability, semester, 
                 timeslots_per_day, class_groups, generation_limit, fitness_limit, mutation_rate, population_size, iterations):
        self.dataset_classes = dataset_classes
        self.dataset_competence_teachers = dataset_competence_teachers
        self.dict_competence_teachers = self.get_competence_teachers(self.dataset_competence_teachers)
        self.dataset_professor_availability = dataset_professor_availability
        self.semester = semester
        self.timeslots_per_day = timeslots_per_day
        self.generation_limit = generation_limit
        self.fitness_limit = fitness_limit
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.professors = self.dataset_competence_teachers['PROFESSOR CODE'].unique()
        # self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.class_types = ['AT', 'AP', 'AV']
        self.class_groups = class_groups
        self.dataset_classes_semester = self.get_classes_semester(self.dataset_classes, self.semester)
        self.timeslots_week = [timeslots_per_day for i in range(len(self.days))]
        self.iterations = iterations
        self.dataset_classes_organized = self.organize_classes(self.dataset_classes_semester)

        self.genome_size = len(self.dataset_classes_organized)
    
        self.classes_bit_length = self.get_bit_length(len(self.dataset_classes_organized))
        self.days_bit_length = self.get_bit_length(len(self.days))
        self.timeslots_per_day_bit_length = self.get_bit_length(len(self.timeslots_per_day))
        self.genome_part_bit_length = self.classes_bit_length + self.days_bit_length + self.timeslots_per_day_bit_length
        self.genomes = []
        self.violations = []

        for p in range(self.iterations):
            print("")
            print("Iteration: ", p)
            self.class_hex_value = -1
            self.best_fitness_score = 0

            self.population = np.zeros((self.population_size, self.genome_size, self.genome_part_bit_length), dtype=int)
            
            self.best_solution, self.generations = self.run_genetic_algorithm()
            self.fitness_score = self.calculate_fitness_score(self.best_solution)
            self.translation_best_solution = self.translate_genome(self.best_solution, string_=True, chronological=True)
            
            self.schedule, none_professors = self.assign_professors(self.translation_best_solution)
            self.violations.append(none_professors)
            self.genomes.append(self.schedule)
            self.dataset_professor_availability = dataset_professor_availability

        # get the minimum value of the violations
        self.min_violations = min(self.violations)
        # get the index of the minimum value of the violations
        self.min_violations_index = self.violations.index(self.min_violations)
        # get the best genome based on the minimum violations
        self.best_genome = self.genomes[self.min_violations_index]
        
    def transform_availability_dict(self, availability_dict, timeslots_per_day, days):
        availability = {}
        for professor, availability_per_day in availability_dict.items():
            availability[professor] = {}
            for day, timeslots in availability_per_day.items():
                availability[professor][days[day]] = {}
                for timeslot, is_available in timeslots.items():
                    availability[professor][days[day]][timeslots_per_day[timeslot]] = is_available
        return availability

    def assign_professors(self, genome):
        none_professors = 0
        professor_availability = self.transform_availability_dict(self.dataset_professor_availability, self.timeslots_per_day, self.days)
        for class_scheduling in genome:
            class_name = class_scheduling['class_data']['class']
            etapa = self.dataset_classes_semester[self.dataset_classes_semester['DISCIPLINA'] == class_name]['ET'].max()
            if etapa == 2:
                class_scheduling['professor'] = 45.0
            else:
                for professor, availability in professor_availability.items():
                    for day, timeslots in availability.items():
                        for timeslot, is_available in timeslots.items():
                            if class_scheduling["timeslot_day"] == day and class_scheduling["timeslot"] == timeslot and is_available and class_scheduling["class_data"]["class"] in self.dict_competence_teachers[professor]:
                                class_scheduling["professor"] = professor
                                professor_availability[professor][day][timeslot] = False
                        
                if "professor" not in class_scheduling.keys():
                    class_scheduling["professor"] = None
                    none_professors += 1

        return genome, none_professors
    
    def print_per_line(self, genome):
        for i in genome:
            print(i)
        
    def get_competence_teachers(self, dataset_competence_teachers):
        competence_teachers_dict = {}
        for professor in dataset_competence_teachers['PROFESSOR CODE'].unique():
            competence_teachers_dict[professor] = []
            for index in range(len(dataset_competence_teachers)):
                if dataset_competence_teachers['PROFESSOR CODE'][index] == professor:
                    competence_teachers_dict[professor].append(dataset_competence_teachers['DISCIPLINA'][index])
        return competence_teachers_dict
    
    def get_classes_semester(self, dataset_classes, semester):
        if semester == "even":
            return dataset_classes[dataset_classes["ET"] % 2 == 0].reset_index(drop=True)
        
        elif semester == "odd":
            return dataset_classes[dataset_classes["ET"] % 2 != 0].reset_index(drop=True)
        elif semester == None:
            return dataset_classes

    def get_hex_value(self,binary_code):
        # reverse the encoded_part
        reverse_encoded_part = binary_code[::-1]
        hex_value = 0
        i = 0
        for bit in reverse_encoded_part:
            hex_value += bit*2**i
            i += 1
        return hex_value

    def organize_classes(self, dataset_classes):
        organized_classes = []
        unique_classes = dataset_classes['DISCIPLINA'].unique()

        for unique_class in unique_classes:
            nr_at_classes = dataset_classes[dataset_classes['DISCIPLINA'] == unique_class]['AT'].max()
            nr_ap_classes = dataset_classes[dataset_classes['DISCIPLINA'] == unique_class]['AP'].max()
            nr_av_classes = dataset_classes[dataset_classes['DISCIPLINA'] == unique_class]['AV'].max()
            classes = {'AT': nr_at_classes, 'AP': nr_ap_classes, 'AV': nr_av_classes}
            semester = dataset_classes[dataset_classes['DISCIPLINA'] == unique_class]['ET'].max()
            class_types = [key for key, value in classes.items() if value != 0]

            if nr_at_classes == 1:
                if semester < 4:
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': self.class_groups})
                else:
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': ['A']})

            if nr_at_classes in [2,4]:
                for class_type in class_types:
                    if semester < 4:
                        if class_type == "AT":
                            for i in range(int(nr_at_classes/2)):
                                organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': self.class_groups})
                        else:
                            for class_group in self.class_groups:
                                organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': class_group})
                    else:
                        for i in range(int(nr_at_classes/2)):
                            organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': ['A']})

            if nr_at_classes == 3:
                if semester < 4:
                    organized_classes.append({'class': unique_class,'class_types':['AT'],'class_groups': self.class_groups})
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': self.class_groups})
                else:
                    organized_classes.append({'class': unique_class,'class_types':['AT'],'class_groups': ['A']})
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': ['A']})
        
        return organized_classes
    
    def get_binary_code(self, binary_code, hex_value):
        i = 0
        while hex_value > 0:
            binary_code[i] = hex_value % 2
            hex_value = hex_value // 2
            i += 1
        # flip the binary code
        binary_code = binary_code[::-1]
        return binary_code

    def get_bit_length(self, db_size):
        value = 0
        for i in range(10):
            value += 2**i
            if value >= db_size:
                return i+1     

    def get_class_part(self, class_scheduling):
        return class_scheduling[:self.classes_bit_length]
    
    def get_day_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length:self.classes_bit_length+self.days_bit_length]
    
    def get_timeslot_part(self, class_scheduling):
        return class_scheduling[self.classes_bit_length+self.days_bit_length:self.classes_bit_length+self.days_bit_length+self.timeslots_per_day_bit_length]       

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
    
    def generate_population(self, population_size):
        for i in range(population_size):
            self.population[i] = self.generate_genome(self.genome_size)
    
    def generate_genome(self, genome_size):
        genome = np.zeros((genome_size, self.genome_part_bit_length), dtype=int)
        self.class_hex_value = -1
        for i in range(genome_size):
            genome[i] = self.generate_genome_part()
        return genome
    
    def generate_genome_part(self):
        self.class_hex_value += 1
        binary_class = self.get_binary_code(np.zeros(self.classes_bit_length, dtype=int), self.class_hex_value)
        
        binary_day = self.generate_binary_code(self.days_bit_length, len(self.days))
        binary_timeslot = self.generate_binary_code(self.timeslots_per_day_bit_length, len(self.timeslots_per_day))

        genome_part = np.concatenate((binary_class, binary_day, binary_timeslot))
        return genome_part

    def translate_genome(self, genome, hex_= False, string_= False, chronological= False):
        translation_string = []
        translation_hex = []
        for class_scheduling in genome:
            class_index = self.get_hex_value(self.get_class_part(class_scheduling))
            day_index = self.get_hex_value(self.get_day_part(class_scheduling))
            timeslot_index = self.get_hex_value(self.get_timeslot_part(class_scheduling))

            if class_index >= len(self.dataset_classes_organized) or day_index >= len(self.days) or timeslot_index >= len(self.timeslots_per_day):
                return False
            
            if hex_:
                translation_hex.append({'class_data': class_index, 'timeslot_day': day_index, 'timeslot': timeslot_index})
                if chronological:
                    translation_hex = sorted(translation_hex, key=lambda k: (k['timeslot_day'], k['timeslot']))

            elif string_:
                class_translation = self.dataset_classes_organized[class_index]
                timeslot_day_translation = self.days[day_index]
                timeslot_translation = self.timeslots_per_day[timeslot_index]

                translation_string.append({'class_data': class_translation, 'timeslot_day': timeslot_day_translation, 'timeslot': timeslot_translation})
                
                if chronological:
                    translation_string = sorted(translation_string, key=lambda k: (self.days.index(k['timeslot_day']), k['timeslot']))
            
        if hex_:
            return translation_hex
        if string_:
            return translation_string

    def translate_hex_to_binary(self,hex_genome):
        # write a function that converts the hex genome to a binary genome
        translation = np.zeros((len(hex_genome), self.genome_part_bit_length), dtype=int)
        index = 0
        for class_scheduling in hex_genome:
            class_hex_value = class_scheduling['class_data']
            day_hex_value = class_scheduling['timeslot_day']
            timeslot_hex_value = class_scheduling['timeslot']
            
            class_binary_code = np.zeros(self.classes_bit_length, dtype=int)
            day_binary_code = np.zeros(self.days_bit_length, dtype=int)
            timeslot_binary_code = np.zeros(self.timeslots_per_day_bit_length, dtype=int)

            class_binary_value = self.get_binary_code(class_binary_code, class_hex_value)
            day_binary_value = self.get_binary_code(day_binary_code, day_hex_value)
            timeslot_binary_value = self.get_binary_code(timeslot_binary_code, timeslot_hex_value)

            # put the binary values in a single numpy array
            class_schedule_binary = np.concatenate((class_binary_value, day_binary_value, timeslot_binary_value))
            translation[index] = class_schedule_binary
            index += 1

        return translation

    # def get_violation_count_saturday_classes(self, genome):
    #     self.incorrectly_assigned_saturday_classes = []
    #     violations = 0
    #     for class_scheduling in genome:
    #         if class_scheduling['timeslot_day'] == 5:
    #             violations += 1
    #             self.incorrectly_assigned_saturday_classes.append(class_scheduling)
    #     return violations
    
    def get_available_timeslots(self, genome):
        available_timeslots = {}
        for day_index in range(len(self.days) - 1):
            available_timeslots[day_index] = []
            for timeslot_index in range(len(self.timeslots_per_day)):
                classes_on_timeslots = [class_ for class_ in genome if class_['timeslot_day'] == day_index and class_['timeslot'] == timeslot_index]
                if classes_on_timeslots == []:
                    available_timeslots[day_index].append(timeslot_index)

        # delete the keys that have an empty value
        available_timeslots = {key: value for key, value in available_timeslots.items() if value != []}

        return available_timeslots
    
    def schedule_class_on_timeslot(self, genome, available_timeslots, index_genome):
        class_types = self.dataset_classes_organized[genome[index_genome]['class_data']]['class_types']
        if 'AV' in class_types:
                timeslot_day = np.random.choice(available_timeslots.keys())
                timeslot
                timeslot = np.random.choice(available_timeslots[timeslot_day])
        else:
            timeslot_day = np.random.choice(list(available_timeslots.keys()))
            local_available_timeslots = available_timeslots[timeslot_day][1::]
            if local_available_timeslots == []:
                return genome[index_genome]['timeslot_day'], genome[index_genome]['timeslot']
            timeslot = np.random.choice(list(available_timeslots[timeslot_day][1::]))

        return timeslot_day, timeslot
    
    def get_violation_count_conflicting_classes(self, genome):
        self.incorrectly_assigned_conflicting_classes = []
        # check if there are no classes scheduled on the same day with the same timeslot
        violations = 0
        for day in range(len(self.days)):
            for timeslot in range(len(self.timeslots_per_day)):
                classes = [class_ for class_ in genome if class_['timeslot_day'] == day and class_['timeslot'] == timeslot]
                classes_translated = [self.dataset_classes_organized[class_['class_data']] for class_ in classes]
                if len(classes) > 1:
                    for i in range(len(classes)-1):
                        class_name_1 = classes_translated[i]['class']
                        class_name_2 = classes_translated[i+1]['class']
                        etapa_1 = self.dataset_classes_semester[self.dataset_classes_semester['DISCIPLINA'] == class_name_1]['ET'].max()
                        etapa_2 = self.dataset_classes_semester[self.dataset_classes_semester['DISCIPLINA'] == class_name_2]['ET'].max()
                        class_group_1 = classes_translated[i]['class_groups']
                        class_group_2 = classes_translated[i+1]['class_groups']
                        common_class_groups = [class_group for class_group in class_group_1 if class_group in class_group_2]

                        if (etapa_1 == etapa_2 and
                            common_class_groups != []):
                            violations += 1
                            self.incorrectly_assigned_conflicting_classes.append(classes[i])
                
        return violations
        
    def get_violation_count_assigning_classes(self, genome):
        self.incorrectly_assigned_classes_to_be_replaced = []
        self.incorrectly_assigned_classes_to_be_scheduled = []

        binary_genome = self.translate_hex_to_binary(genome)
        translated_genome = self.translate_genome(binary_genome, string_=True)
        copy_organized_classes = self.dataset_classes_organized.copy()
        violations = 0

        for class_scheduling in translated_genome:
            if class_scheduling['class_data'] in copy_organized_classes:
                copy_organized_classes.remove(class_scheduling['class_data'])
            else:
                violations += 2
                self.incorrectly_assigned_classes_to_be_replaced.append(class_scheduling)

        # get the classes that are in the organized classes but not in the genome
        for class_ in copy_organized_classes:
            violations += 1
            self.incorrectly_assigned_classes_to_be_scheduled.append(class_)

        return violations
    
    def get_violation_count_timeslot_virtual_classes(self, genome):
        self.incorrectly_assigned_virtual_classes = []
        violations = 0
        for class_scheduling in genome:
            class_type = self.dataset_classes_organized[class_scheduling['class_data']]['class_types']
            if class_scheduling['timeslot'] == 0 and class_type != ['AV']:
                violations += 1
                self.incorrectly_assigned_virtual_classes.append(class_scheduling)
        return violations
    
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
            genome_parts = [self.get_class_part,self.get_day_part, self.get_timeslot_part]

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
    
    def calculate_fitness_score(self, genome):
        hex_genome = self.translate_genome(genome, hex_=True, chronological=True)
        violations = 0

        # violations += self.get_violation_count_saturday_classes(hex_genome)
        # violations += self.get_violation_count_assigning_professor(hex_genome)
        # violations += self.get_violation_count_consecutive_classes(hex_genome)
        violations += self.get_violation_count_conflicting_classes(hex_genome)
        violations += self.get_violation_count_assigning_classes(hex_genome)
        # violations += self.get_violation_count_professor_conflict(hex_genome)
        violations += self.get_violation_count_timeslot_virtual_classes(hex_genome)

        return 1/(1+violations)
    
    def run_genetic_algorithm(self):
        self.generate_population(self.population_size)
        # best_fitness_scores = np.zeros(self.generation_limit)
        
        for i in range(self.generation_limit):
            # sort the population based on the fitness score of each genome, make us of the numpy arrays
            self.population = self.population[np.argsort([self.calculate_fitness_score(genome) for genome in self.population])][::-1]
            print("Generation: ", i+1)
            if self.calculate_fitness_score(self.population[0]) >= self.fitness_limit:
                break

            self.best_fitness_score = self.calculate_fitness_score(self.population[0])
           
            print("Best fitness score: ", self.best_fitness_score)
            
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

        return self.population[0], i+1,

def add_semester(data, input_dataset_classes):
    for class_scheduling in data:
        class_name = class_scheduling['class_data']['class']
        etapa = input_dataset_classes[input_dataset_classes['DISCIPLINA'] == class_name]['ET'].max()
        class_scheduling['class_data']['semester'] = etapa
    return data

from flask import Flask, jsonify, request
from flask_cors import CORS

# Start app
app = Flask(__name__)
CORS(app)

endpoint = '/api/v1'
    
@app.route(endpoint + '/generate_timetable/<semester>', methods=['GET'])
def generate_schedule(semester):
    # User inputs
    input_dataset_classes = pd.read_csv('../data/ClassesNoDuplicates.csv', sep=';')
    input_dataset_classes = input_dataset_classes.sort_values(by=['ET'])
    input_dataset_competence_teachers = pd.read_csv('../data/ClassesPP.csv', sep=';')

    if semester == 'February - June':
        input_semester = 'even'
    elif semester == 'Augustus - December':
        input_semester = 'odd'

    input_iterations = 10

    input_timeslots_per_day = [
        "12:45-14:25",
        "17:10-18:50",
        "19:00-20:40",
        "20:55-22:35"]

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    input_class_groups = ["A", "B"]

    input_generation_limit = 5000
    input_fitness_limit = 1
    input_mutation_rate = 0.01
    input_population_size = 6

    input_professor_availability = {}
    for professor in input_dataset_competence_teachers['PROFESSOR CODE'].unique():
        input_professor_availability[professor] = {}
        for day_index in range(len(days)):
            input_professor_availability[professor][day_index] = {}
            for timeslot_index in range(len(input_timeslots_per_day)):
                input_professor_availability[professor][day_index][timeslot_index] = False
                if np.random.rand() < 0.7:
                    input_professor_availability[professor][day_index][timeslot_index] = True

    class_schedule = GenerateClassSchedule(dataset_classes=input_dataset_classes, dataset_competence_teachers=input_dataset_competence_teachers,
                                        dataset_professor_availability=input_professor_availability ,semester=input_semester, timeslots_per_day=input_timeslots_per_day,
                                        class_groups = input_class_groups, generation_limit=input_generation_limit, fitness_limit=input_fitness_limit,
                                        mutation_rate=input_mutation_rate,population_size=input_population_size, iterations=input_iterations)
    
    data = add_semester(class_schedule.best_genome, input_dataset_classes)
    return jsonify(data),200

if __name__ == '__main__':
    app.run()

