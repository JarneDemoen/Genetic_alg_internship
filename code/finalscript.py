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
        self.generation_limit = generation_limit
        self.fitness_limit = fitness_limit
        self.mutation_rate = mutation_rate
        self.population_size = population_size
        self.professors = self.dataset_competence_teachers['PROFESSOR CODE'].unique()
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        self.class_types = ['AT', 'AP', 'AV']
        self.class_groups = class_groups
        self.dataset_classes_semester = self.get_classes_semester(self.dataset_classes, self.semester)
        self.timeslots_week = [timeslots_per_day for i in range(len(self.days))]
        self.early_stopping = early_stopping
        self.dataset_classes_organized = self.organize_classes(dataset_classes)
        
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
                    # create a variable class_types, the value is a list of the keys in classes that are not 0
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': self.class_groups})
                else:
                    organized_classes.append({'class': unique_class,'class_types':class_types,'class_groups': ['A']})

            if nr_at_classes == 2:
                for class_type in class_types:
                    if semester < 4:
                        if class_type == "AT":
                            organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': self.class_groups})
                        else:
                            for class_group in self.class_groups:
                                organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': class_group})
                    else:
                        organized_classes.append({'class': unique_class,'class_types':class_type,'class_groups': ['A']})

            if nr_at_classes == 3:
                


        for i in organized_classes:
            print(i)
        return organized_classes
                

# User inputs
input_dataset_classes = pd.read_csv('../data/ClassesNoDuplicates.csv', sep=';')
input_dataset_classes = input_dataset_classes.sort_values(by=['ET'])
input_dataset_competence_teachers = pd.read_csv('../data/ClassesPP.csv', sep=';')

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
input_class_groups = ["A", "B"]

input_generation_limit = 100000
input_fitness_limit = 1
input_mutation_rate = 0.0075
input_population_size = 30
input_early_stopping = 300

start = time.time()

class_schedule = GenerateClassSchedule(dataset_classes=input_dataset_classes, dataset_competence_teachers=input_dataset_competence_teachers,
                                       dataset_professor_availability=None ,semester=input_semester, timeslots_per_day=input_timeslots_per_day,
                                       class_groups = input_class_groups, generation_limit=input_generation_limit, fitness_limit=input_fitness_limit,
                                       mutation_rate=input_mutation_rate,population_size=input_population_size, early_stopping=input_early_stopping)
end = time.time()
