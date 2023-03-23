import pandas as pd
from random import choices, randint, randrange
import random
import time
import itertools

dataset_courses = pd.read_csv('./data/CoursesSem1.csv', sep=';')
courses = [course_id for course_id in dataset_courses['course_id'].unique()]

def get_unique_student_groups(student_groups):
    student_group_string = ""
    for student_group in student_groups.unique():
        student_group_string += str(student_group)
    student_groups_unique = list(set(list(student_group_string)))
    return student_groups_unique

student_groups = get_unique_student_groups(dataset_courses['student_group'])
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def generate_genome(length):
    return choices([0,1], k=length)

