# imports 
import numpy as np
import pandas as pd
import os 
import time

# making sure the current working directory is the same as the file path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GenerateClassSchedule:
    def __init__(self, dataset_classes, dataset_competence_teachers, dataset_professor_availability, semester, 
                 timeslots_per_day, class_groups, generation_limit, fitness_limit, mutation_rate, population_size, early_stopping):
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
        self.early_stopping = early_stopping

        self.classes_bit_length = self.get_bit_length(len(self.dataset_classes_semester))
        self.class_types_bit_length = self.get_bit_length(len(self.class_types))
        self.class_groups_bit_length = self.get_bit_length(len(self.class_groups))
        self.professors_bit_length = self.get_bit_length(len(self.professors))
        self.days_bit_length = self.get_bit_length(len(self.days))
        self.timeslots_per_day_bit_length = self.get_bit_length(len(self.timeslots_per_day))
        self.genome_part_bit_length = self.classes_bit_length + self.class_types_bit_length + self.class_groups_bit_length + self.professors_bit_length + self.days_bit_length + self.timeslots_per_day_bit_length

        self.best_fitness_score = 0

        self.population = np.zeros((self.population_size, self.genome_size, self.genome_part_bit_length), dtype=int)

        self.best_solution, self.generations = self.run_genetic_algorithm()
        self.fitness_score = self.calculate_fitness_score(self.best_solution)
        self.translation_best_solution = self.translate_genome(self.best_solution, string_=True, chronological=True)
        self.best_solution_hex = self.translate_genome(self.best_solution, hex_=True, chronological=True)

        self.violation_count_assigning_classes = self.get_violation_count_assigning_classes(self.best_solution_hex)
        self.violation_count_assigning_professor = self.get_violation_count_assigning_professor(self.best_solution_hex)
        self.violation_count_saturday_classes = self.get_violation_count_saturday_classes(self.best_solution_hex)
        self.violation_count_consecutive_classes = self.get_violation_count_consecutive_classes(self.best_solution_hex)
        
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
        elif semester == None:
            return dataset_classes
        
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

    def get_binary_code(self, binary_code, hex_value):
        i = 0
        while hex_value > 0:
            binary_code[i] = hex_value % 2
            hex_value = hex_value // 2
            i += 1
        # flip the binary code
        binary_code = binary_code[::-1]
        return binary_code

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

    def translate_hex_to_binary(self,hex_genome):
        # write a function that converts the hex genome to a binary genome
        translation = np.zeros((len(hex_genome), self.genome_part_bit_length), dtype=int)
        index = 0
        for class_scheduling in hex_genome:
            class_hex_value = class_scheduling['class']
            class_type_hex_value = class_scheduling['class_type']
            class_group_hex_value = class_scheduling['class_group']
            professor_hex_value = class_scheduling['professor']
            day_hex_value = class_scheduling['timeslot_day']
            timeslot_hex_value = class_scheduling['timeslot']
            
            class_binary_code = np.zeros(self.classes_bit_length, dtype=int)
            class_type_binary_code = np.zeros(self.class_types_bit_length, dtype=int)
            class_group_binary_code = np.zeros(self.class_groups_bit_length, dtype=int)
            professor_binary_code = np.zeros(self.professors_bit_length, dtype=int)
            day_binary_code = np.zeros(self.days_bit_length, dtype=int)
            timeslot_binary_code = np.zeros(self.timeslots_per_day_bit_length, dtype=int)

            class_binary_value = self.get_binary_code(class_binary_code, class_hex_value)
            class_type_binary_value = self.get_binary_code(class_type_binary_code, class_type_hex_value)
            class_group_binary_value = self.get_binary_code(class_group_binary_code, class_group_hex_value)
            professor_binary_value = self.get_binary_code(professor_binary_code, professor_hex_value)
            day_binary_value = self.get_binary_code(day_binary_code, day_hex_value)
            timeslot_binary_value = self.get_binary_code(timeslot_binary_code, timeslot_hex_value)

            # put the binary values in a single numpy array
            class_schedule_binary = np.concatenate((class_binary_value, class_type_binary_value, class_group_binary_value, professor_binary_value, day_binary_value, timeslot_binary_value))
            translation[index] = class_schedule_binary
            index += 1

        return translation

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
        self.incorrectly_assigned_professors = []
        violations = 0
        for class_scheduling in genome:
            professor = self.professors[class_scheduling['professor']]
            class_name = self.dataset_classes_semester['DISCIPLINA'][class_scheduling['class']]
            if class_name not in self.dict_competence_teachers[professor]:
                violations += 1
                self.incorrectly_assigned_professors.append({'class': class_name, 'professor': professor})

        return violations
    
    def get_violation_count_saturday_classes(self,genome):
        violations = 0
        for class_scheduling in genome:
            if class_scheduling['timeslot_day'] == 5:
                violations += 0.2
        return violations
    
    def get_violation_count_assigning_classes(self, genome):
        self.incorrectly_assigned_classes = []
        violations = 0
        for index_class in range(len(self.dataset_classes_semester)):
            violations_class = 0
            nr_at = {}
            nr_ap = {}
            nr_av = {}

            if self.dataset_classes_semester['ET'][index_class] >= 4:
                class_groups = ['A']
            else:
                class_groups = self.class_groups

            for class_group in class_groups:
                nr_at[class_group] = self.dataset_classes_semester['AT'][index_class]
                nr_ap[class_group] = self.dataset_classes_semester['AP'][index_class]
                nr_av[class_group] = self.dataset_classes_semester['AV'][index_class]

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
                violations_class += abs(values)
                
            for values in nr_ap.values():
                violations_class += abs(values)

            for values in nr_av.values():
                violations_class += abs(values)

            if violations_class > 0:
                self.incorrectly_assigned_classes.append({'class': self.dataset_classes_semester['DISCIPLINA'][index_class], 'nr_at': nr_at, 'nr_ap': nr_ap, 'nr_av': nr_av})
            
            violations += violations_class

        return violations
    
    def get_violation_count_consecutive_classes(self,genome):
        self.incorrectly_assigned_consecutive_classes = []
        violations = 0
        for i in range(len(genome) - 1):
            current_class = genome[i]
            next_class = genome[i + 1]
            previous_class = genome[i - 1] if i > 0 else None
            nr_at = self.dataset_classes_semester['AT'][current_class['class']]
            # when I'm at the last index, check if the previous class was the same as the current class
            # TODO
            if (
                current_class['class'] == next_class['class'] and
                current_class['class_type'] == next_class['class_type'] and
                current_class['professor'] == next_class['professor'] and
                current_class['class_group'] == next_class['class_group']
            ):
                if (
                    current_class['timeslot_day'] == next_class['timeslot_day'] and
                    current_class['timeslot'] + 1 == next_class['timeslot']
                ):
                    # Same class scheduled for 2 hours straight
                    continue
                # elif (
                #     current_class['timeslot_day'] == next_class['timeslot_day'] and
                #     current_class['timeslot'] + 2 == next_class['timeslot']
                # ):
                #     # Same class scheduled for 4 hours straight
                #     continue

            else:
                # if the previous class was the same as the current class, there is no violation because there are 2 consecutive classes
                if previous_class is not None and current_class['class'] == previous_class['class'] and current_class['class_type'] == previous_class['class_type'] and current_class['professor'] == previous_class['professor'] and current_class['class_group'] == previous_class['class_group'] and current_class['timeslot_day'] == previous_class['timeslot_day'] and current_class['timeslot'] - 1 == previous_class['timeslot']:
                    continue

                if nr_at == 3 and current_class['class'] == next_class['class'] and current_class['professor'] == next_class['professor'] and current_class['class_group'] == next_class['class_group']:
                    if (
                    current_class['timeslot_day'] == next_class['timeslot_day'] and
                    current_class['timeslot'] + 1 == next_class['timeslot']
                    ):
                        continue
                
            # Increment violations count
            violations += 1
            self.incorrectly_assigned_consecutive_classes.append({'class': self.dataset_classes_semester['DISCIPLINA'][current_class['class']], 'class_type': self.class_types[current_class['class_type']], 'professor': self.professors[current_class['professor']], 'class_group': self.class_groups[current_class['class_group']], 'timeslot_day': self.days[current_class['timeslot_day']], 'timeslot': self.timeslots_per_day[current_class['timeslot']]})

        return violations
    
    def calculate_fitness_score(self, genome):
        hex_genome = self.translate_genome(genome, hex_=True, chronological=True)
        violations = 0
        violations += self.get_violation_count_saturday_classes(hex_genome)
        violations += self.get_violation_count_assigning_professor(hex_genome)
        violations += self.get_violation_count_assigning_classes(hex_genome)
        violations += self.get_violation_count_consecutive_classes(hex_genome)
        return 1/(1+violations)
    
    def enhance_assigning_professors(self,best_genome,incorrectly_assigned_professors):
        for incorrectly_assigned_professor in incorrectly_assigned_professors:
            professor = incorrectly_assigned_professor['professor']
            class_name = incorrectly_assigned_professor['class']

            professor_hex = np.where(np.array(self.professors) == professor)[0][0]
            class_name_hex = np.where(self.dataset_classes_semester['DISCIPLINA'] == class_name)[0][0]
            

            for index in range(len(best_genome)):
                if best_genome[index]['professor'] == professor_hex and best_genome[index]['class'] == class_name_hex:
                    competent_teachers = []
                    for prof_code in self.dict_competence_teachers:
                        if class_name in self.dict_competence_teachers[prof_code]:
                            competent_teachers.append(prof_code)
                    new_professor = np.random.choice(competent_teachers)
                    new_professor_hex = np.where(np.array(self.professors) == new_professor)[0][0]
                    best_genome[index]['professor'] = new_professor_hex
                    break

        return best_genome
    
    def enhance_assigning_classes(self,best_genome,incorrectly_assigned_classes):
        to_be_replaced = []
        to_be_scheduled = []
        for incorrectly_assigned_class in incorrectly_assigned_classes:
            class_name = incorrectly_assigned_class['class']
            for class_type in incorrectly_assigned_class:
                if class_type != 'class':
                    for class_group in incorrectly_assigned_class[class_type]:
                        class_value = incorrectly_assigned_class[class_type][class_group]
                        if class_value > 0:
                            for value in range(class_value):
                                to_be_scheduled.append({'class': class_name, 'class_type': class_type[3::].upper(), 'class_group': class_group})
                        elif class_value < 0:
                            for value in range(abs(class_value)):
                                to_be_replaced.append({'class': class_name, 'class_type': class_type[3::].upper(), 'class_group': class_group})

        for index in range(len(to_be_replaced)):
            index_to_be_replaced = 0
            for class_scheduling in best_genome:
                class_name = self.dataset_classes_semester['DISCIPLINA'][class_scheduling['class']]
                class_type = self.class_types[class_scheduling['class_type']]
                class_group = self.class_groups[class_scheduling['class_group']]

                if class_name == to_be_replaced[index]['class'] and class_type == to_be_replaced[index]['class_type'] and class_group == to_be_replaced[index]['class_group']:
                    break
                index_to_be_replaced += 1

            to_be_scheduled_class_name = to_be_scheduled[index]['class']
            to_be_scheduled_class_type = to_be_scheduled[index]['class_type']
            to_be_scheduled_class_group = to_be_scheduled[index]['class_group']

            to_be_scheduled_class_hex = np.where(self.dataset_classes_semester['DISCIPLINA'] == to_be_scheduled_class_name)[0][0]
            to_be_scheduled_class_type_hex = np.where(np.array(self.class_types) == to_be_scheduled_class_type)[0][0]
            to_be_scheduled_class_group_hex = np.where(np.array(self.class_groups) == to_be_scheduled_class_group)[0][0]

            best_genome[index_to_be_replaced]['class'] = to_be_scheduled_class_hex
            best_genome[index_to_be_replaced]['class_type'] = to_be_scheduled_class_type_hex
            best_genome[index_to_be_replaced]['class_group'] = to_be_scheduled_class_group_hex

        return best_genome

    def run_genetic_algorithm(self):
        self.generate_population(self.population_size)
        hex_genome = self.translate_genome(self.population[0], hex_=True, chronological=True)
        binary_genome = self.translate_hex_to_binary(hex_genome)
        fitness_scores = np.zeros(self.generation_limit)
        
        for i in range(self.generation_limit):
            
            # sort the population based on the fitness score of each genome, make us of the numpy arrays
            self.population = self.population[np.argsort([self.calculate_fitness_score(genome) for genome in self.population])][::-1]
            print("Generation: ", i+1)
            if self.calculate_fitness_score(self.population[0]) >= self.fitness_limit:
                break

            self.best_fitness_score = self.calculate_fitness_score(self.population[0])
            # if the best fitness score has not improved after 500 generations, we stop the program
            fitness_scores[i] = self.best_fitness_score
            if i > self.early_stopping:
                if np.all(fitness_scores[i-self.early_stopping:i] == self.best_fitness_score):
                    print("Stuck")
                    best_genome = self.population[0]
                    hex_best_genome = self.translate_genome(best_genome, hex_=True, chronological=True)

                    nr_incorrectly_assigned_classes = self.get_violation_count_assigning_classes(hex_best_genome)
                    nr_incorrectly_assigned_teachers = self.get_violation_count_assigning_professor(hex_best_genome)

                    if nr_incorrectly_assigned_classes > 0:
                        hex_best_genome = self.enhance_assigning_classes(hex_best_genome, self.incorrectly_assigned_classes)

                    # update the incorrect things
                    nr_incorrectly_assigned_classes = self.get_violation_count_assigning_classes(hex_best_genome)
                    nr_incorrectly_assigned_teachers = self.get_violation_count_assigning_professor(hex_best_genome)
                    
                    if nr_incorrectly_assigned_teachers > 0:
                        hex_best_genome = self.enhance_assigning_professors(hex_best_genome, self.incorrectly_assigned_professors)

                    best_genome_binary = self.translate_hex_to_binary(hex_best_genome)
                    
                    return best_genome_binary, i+1

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
# sort input dataset classes base on class name
# input_dataset_classes = input_dataset_classes.sort_values(by=['DISCIPLINA'])

input_semester = "even"
input_timeslots_per_day = [
    "12:45-13:35",
    "13:35-14:25",
    "17:10-18:00",
    "18:00-18:50",
    "19:00-19:50",
    "19:50-20:40",
    "20:55-21:45",
    "21:45-22:35"]

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']

# input_professor_availability = {}
# for professor in input_dataset_competence_teachers['PROFESSOR CODE'].unique():
#     input_professor_availability[professor] = []
#     for day in days:
#         for timeslot in input_timeslots_per_day:
#             if np.random.choice([True, False], p=[0.42, 0.58]):
#                 input_professor_availability[professor].append({'day': day, 'timeslot': timeslot})

# for professor in input_professor_availability:
#     print("Professor: ", professor)
#     for i in input_professor_availability[professor]:
#         print(i)
#     print("------------------")
    

input_class_groups = ["A", "B"]
input_generation_limit = 10000
input_fitness_limit = 1
input_mutation_rate = 0.0075
input_population_size = 10
input_early_stopping = 500

start = time.time()

class_schedule = GenerateClassSchedule(dataset_classes=input_dataset_classes, dataset_competence_teachers=input_dataset_competence_teachers,
                                       dataset_professor_availability=None ,semester=input_semester, timeslots_per_day=input_timeslots_per_day, 
                                       class_groups=input_class_groups, generation_limit=input_generation_limit, fitness_limit=input_fitness_limit,
                                       mutation_rate=input_mutation_rate,population_size=input_population_size, early_stopping=input_early_stopping)
end = time.time()

print("Generations: ", class_schedule.generations)
print("Time: ", end - start)
print("Best solution: ")
class_schedule.print_per_line(class_schedule.translation_best_solution)
print("Fitness score: ", class_schedule.fitness_score)
print("Violation count assigning classes: ", class_schedule.violation_count_assigning_classes)
print("Violation count assigning professor: ", class_schedule.violation_count_assigning_professor)
print("Violation count saturday classes: ", class_schedule.violation_count_saturday_classes)
print("Violation count consecutive classes: ", class_schedule.violation_count_consecutive_classes)
print("Incorrectly assigned consecutive classes: ")
class_schedule.print_per_line(class_schedule.incorrectly_assigned_consecutive_classes)