# imports 
import numpy as np
import pandas as pd
import os 
import time

# making sure the current working directory is the same as the file path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class GenerateClassSchedule:
    def __init__(self, dataset_classes, dataset_competence_teachers, dataset_professor_availability, semester, 
                 timeslots_per_day, class_groups):
        self.dataset_classes = dataset_classes
        self.dataset_competence_teachers = dataset_competence_teachers
        self.semester = semester
        self.timeslots_per_day = timeslots_per_day
        self.class_groups = class_groups
        
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday']
        self.dataset_classes_semester = self.get_classes_semester(self.dataset_classes, self.semester)
        self.timeslots_week = [timeslots_per_day for i in range(len(self.days))]
        self.class_types = ["AT", "AP", "AV"]
        self.genome_size = self.get_genome_size(self.dataset_classes_semester)
        self.print_all_class_variables()

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
    
    def print_all_class_variables(self):
        print("dataset_classes: ", self.dataset_classes)
        print("dataset_competence_teachers: ", self.dataset_competence_teachers)
        print("semester: ", self.semester)
        print("timeslots_per_day: ", self.timeslots_per_day)
        print("class_groups: ", self.class_groups)
        print("days: ", self.days)
        print("dataset_classes_semester: ", self.dataset_classes_semester)
        print("timeslots_week: ", self.timeslots_week)
        print("class_types: ", self.class_types)
        print("genome_size: ", self.genome_size)
    

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

class_schedule = GenerateClassSchedule(dataset_classes=dataset_classes, dataset_competence_teachers=dataset_competence_teachers,
                                       dataset_professor_availability=None ,semester=semester, timeslots_per_day=timeslots_per_day, 
                                       class_groups=class_groups)
            