import pandas as pd
from random import choices, randint, randrange
import random
import time
import itertools

dataset_courseSchedule = pd.read_csv('./data/CourseSchedule.csv', sep=';')
dataset_courses = pd.read_csv('./data/Courses.csv', sep=';')
dataset_professors = pd.read_csv('./data/Professors.csv', sep=';')

