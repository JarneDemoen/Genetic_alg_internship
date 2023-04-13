def get_violation_count_scheduling(genome):
    violations = 0
    for day in days:
        classes_day = [class_scheduling for class_scheduling in genome if class_scheduling['timeslot_day'] == day]

        if len(classes_day) == 0:
            print("No classes on ", day)
            continue

        print("Classes day")
        print_per_line(classes_day)

        if day == 'Saturday':
            print(f"{len(classes_day)} classes scheduled on Saturday")
            violations += len(classes_day)

        for i in range(len(classes_day) - 1):
            current_class = classes_day[i]
            next_class = classes_day[i+1]

            print("Current class: ", current_class)
            print("Next class: ", next_class)

            index_timeslot_current_class = timeslots_per_day.index(current_class['timeslot'])
            index_timeslot_next_class = timeslots_per_day.index(next_class['timeslot'])

            print("Timeslot current class: ", index_timeslot_current_class)
            print("Timeslot next class: ", index_timeslot_next_class)

            if index_timeslot_current_class + 1 == index_timeslot_next_class:
                print("There are two classes in a row")
                
                if current_class['class'] != next_class['class']:
                    violations += 1
                    print("The classes are not the same")
                
                if current_class['class_type'] != next_class['class_type']:
                    violations += 1
                    print("The class type is not the same")

                if current_class['professor'] != next_class['professor']:
                    violations += 1
                    print("The professor is not the same")
                
                if current_class['class_group'] != next_class['class_group']:
                    violations += 1
                    print("The class group is not the same")

            elif index_timeslot_current_class == index_timeslot_next_class:
                print("There are two classes at the same time")
                
                if current_class['class'] != next_class['class']:
                    violations += 1
                    print("The classes are not the same")
                
                if current_class['class_type'] != next_class['class_type']:
                    violations += 1
                    print("The class type is not the same")

                if current_class['professor'] != next_class['professor']:
                    violations += 1
                    print("The professor is not the same")

                if current_class['class_group'] == next_class['class_group']:
                    violations += 1
                    print("The class group is the same")
                elif current_class['class_type'] != next_class['class_type']:
                    violations += 1
                    print("Class group is different but the class type is also different")
                elif current_class['class_type'] == next_class['class_type'] and current_class['class_type'] == 'AP':
                    violations += 1
                    print("The class group is different and the class type is the same but it's AP")

            else:
                # no class this timeslot or on the next timeslot
                if index_timeslot_current_class == 0:
                    print(f"The class {current_class} is scheduled on the first timeslot of the day and there is no class on the next timeslot")
                    violations += 4

                elif index_timeslot_next_class == len(timeslots_per_day) - 1:
                    print(f"The class {next_class} is scheduled on the last timeslot of the day and there is no class on the previous timeslot")
                    violations += 4

                else:
                    print("There is no class on the next timeslot")
                    print("There is no class on the previous timeslot")
                    violations += 4

    return violations