import numpy as np
incorrectly_assigned_classes = [
{'class': 'GB922', 'nr_at': {'A': 0, 'B': 0}, 'nr_ap': {'A': 0, 'B': 0}, 'nr_av': {'A': 0, 'B': 1}}, 
{'class': 'AC222', 'nr_at': {'A': 0}, 'nr_ap': {'A': 0}, 'nr_av': {'A': -1}}
]

genome = np.array([
{'class': 'AC222', 'class_type': 'AT', 'class_group': 'A', 'professor': 12.274, 'timeslot_day': 'Monday', 'timeslot': '13:35-14:25', 'et': 5},
{'class': 'R0812', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Monday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'AC322', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Monday', 'timeslot': '13:35-14:25', 'et': 5},
{'class': 'GM722', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Monday', 'timeslot': '13:35-14:25', 'et': 7},
{'class': 'GB922', 'class_type': 'AV', 'class_group': 'B', 'professor': 12.203, 'timeslot_day': 'Monday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'R8512', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.642, 'timeslot_day': 'Monday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.472, 'timeslot_day': 'Monday', 'timeslot': '18:00-18:50', 'et': 3},
{'class': 'AD422', 'class_type': 'AP', 'class_group': 'A', 'professor': 12.274, 'timeslot_day': 'Monday', 'timeslot': '18:00-18:50', 'et': 7},
{'class': 'GB922', 'class_type': 'AV', 'class_group': 'A', 'professor': 12.203, 'timeslot_day': 'Monday', 'timeslot': '18:00-18:50', 'et': 3},
{'class': 'GJ922', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.776, 'timeslot_day': 'Monday', 'timeslot': '19:00-19:50', 'et': 3},
{'class': 'HE622', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.07, 'timeslot_day': 'Monday', 'timeslot': '19:00-19:50', 'et': 1},
{'class': 'HE722', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.776, 'timeslot_day': 'Monday', 'timeslot': '19:00-19:50', 'et': 1},
{'class': 'GK622', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Monday', 'timeslot': '19:50-20:40', 'et': 5},
{'class': 'AD122', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Monday', 'timeslot': '19:50-20:40', 'et': 7},
{'class': 'AD322', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Monday', 'timeslot': '20:55-21:45', 'et': 7},
{'class': 'AC222', 'class_type': 'AT', 'class_group': 'A', 'professor': 12.274, 'timeslot_day': 'Monday', 'timeslot': '20:55-21:45', 'et': 5},
{'class': 'HE722', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.034, 'timeslot_day': 'Monday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'B', 'professor': 11.792, 'timeslot_day': 'Monday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'HF222', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Tuesday', 'timeslot': '12:45-13:35', 'et': 1},
{'class': 'R8512', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '12:45-13:35', 'et': 3},
{'class': 'GM722', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Tuesday', 'timeslot': '12:45-13:35', 'et': 7},
{'class': 'AC122', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '12:45-13:35', 'et': 5},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.472, 'timeslot_day': 'Tuesday', 'timeslot': '12:45-13:35', 'et': 3},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Tuesday', 'timeslot': '13:35-14:25', 'et': 1},
{'class': 'AD322', 'class_type': 'AP', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Tuesday', 'timeslot': '13:35-14:25', 'et': 7},
{'class': 'R8512', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Tuesday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'AC222', 'class_type': 'AV', 'class_group': 'A', 'professor': 12.274, 'timeslot_day': 'Tuesday', 'timeslot': '17:10-18:00', 'et': 5},
{'class': 'AE422', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.091, 'timeslot_day': 'Tuesday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'AC122', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '18:00-18:50', 'et': 5},
{'class': 'AE422', 'class_type': 'AV', 'class_group': 'B', 'professor': 14.091, 'timeslot_day': 'Tuesday', 'timeslot': '18:00-18:50', 'et': 3},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.776, 'timeslot_day': 'Tuesday', 'timeslot': '18:00-18:50', 'et': 3},
{'class': 'AC122', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '18:00-18:50', 'et': 5},
{'class': 'GB922', 'class_type': 'AT', 'class_group': 'A', 'professor': 12.203, 'timeslot_day': 'Tuesday', 'timeslot': '19:00-19:50', 'et': 3},
{'class': 'GL822', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.472, 'timeslot_day': 'Tuesday', 'timeslot': '19:50-20:40', 'et': 5},
{'class': 'GB922', 'class_type': 'AT', 'class_group': 'A', 'professor': 12.203, 'timeslot_day': 'Tuesday', 'timeslot': '19:50-20:40', 'et': 3},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'AC422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.525, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 5},
{'class': 'HF222', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.034, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 3},
{'class': 'R8512', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 3},
{'class': 'AD222', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.616, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 7},
{'class': 'HE722', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.525, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'R0812', 'class_type': 'AP', 'class_group': 'B', 'professor': 13.034, 'timeslot_day': 'Tuesday', 'timeslot': '20:55-21:45', 'et': 3},
{'class': 'AE422', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.091, 'timeslot_day': 'Tuesday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'AD222', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.616, 'timeslot_day': 'Tuesday', 'timeslot': '21:45-22:35', 'et': 7},
{'class': 'AC322', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Wednesday', 'timeslot': '12:45-13:35', 'et': 5},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'B', 'professor': 11.792, 'timeslot_day': 'Wednesday', 'timeslot': '12:45-13:35', 'et': 1},
{'class': 'HE622', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Wednesday', 'timeslot': '12:45-13:35', 'et': 1},
{'class': 'AE422', 'class_type': 'AV', 'class_group': 'A', 'professor': 14.091, 'timeslot_day': 'Wednesday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'GB922', 'class_type': 'AT', 'class_group': 'B', 'professor': 12.203, 'timeslot_day': 'Wednesday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'HE722', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.776, 'timeslot_day': 'Wednesday', 'timeslot': '13:35-14:25', 'et': 1},
{'class': 'AD322', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Wednesday', 'timeslot': '17:10-18:00', 'et': 7},
{'class': 'AD222', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.616, 'timeslot_day': 'Wednesday', 'timeslot': '17:10-18:00', 'et': 7},
{'class': 'AC922', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Wednesday', 'timeslot': '17:10-18:00', 'et': 7},
{'class': 'HE622', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Wednesday', 'timeslot': '18:00-18:50', 'et': 1},
{'class': 'GM722', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Wednesday', 'timeslot': '18:00-18:50', 'et': 7},
{'class': 'R0812', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.472, 'timeslot_day': 'Wednesday', 'timeslot': '19:50-20:40', 'et': 3},
{'class': 'R8512', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.875, 'timeslot_day': 'Wednesday', 'timeslot': '19:50-20:40', 'et': 3},
{'class': 'HE722', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.034, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'R0812', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.472, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 3},
{'class': 'AD422', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 7},
{'class': 'AC122', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 5},
{'class': 'HF222', 'class_type': 'AV', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'AC322', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Wednesday', 'timeslot': '20:55-21:45', 'et': 5},
{'class': 'HF222', 'class_type': 'AV', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Wednesday', 'timeslot': '21:45-22:35', 'et': 1},
{'class': 'GB922', 'class_type': 'AT', 'class_group': 'B', 'professor': 12.203, 'timeslot_day': 'Wednesday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'AE422', 'class_type': 'AV', 'class_group': 'A', 'professor': 14.091, 'timeslot_day': 'Wednesday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'GB922', 'class_type': 'AV', 'class_group': 'A', 'professor': 12.203, 'timeslot_day': 'Thursday', 'timeslot': '12:45-13:35', 'et': 3},
{'class': 'HE622', 'class_type': 'AP', 'class_group': 'B', 'professor': 13.07, 'timeslot_day': 'Thursday', 'timeslot': '12:45-13:35', 'et': 1},
{'class': 'R8512', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.642, 'timeslot_day': 'Thursday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'HE722', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.785, 'timeslot_day': 'Thursday', 'timeslot': '13:35-14:25', 'et': 1},
{'class': 'HF222', 'class_type': 'AV', 'class_group': 'B', 'professor': 13.0, 'timeslot_day': 'Thursday', 'timeslot': '13:35-14:25', 'et': 1},
{'class': 'AE422', 'class_type': 'AV', 'class_group': 'B', 'professor': 14.091, 'timeslot_day': 'Thursday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Thursday', 'timeslot': '18:00-18:50', 'et': 1},
{'class': 'AD122', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Thursday', 'timeslot': '18:00-18:50', 'et': 7},
{'class': 'GK622', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.776, 'timeslot_day': 'Thursday', 'timeslot': '18:00-18:50', 'et': 5},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'B', 'professor': 11.792, 'timeslot_day': 'Thursday', 'timeslot': '18:00-18:50', 'et': 1},
{'class': 'GJ922', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.472, 'timeslot_day': 'Thursday', 'timeslot': '18:00-18:50', 'et': 3},
{'class': 'HE722', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.525, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 1},
{'class': 'GM722', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 7},
{'class': 'AD322', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 7},
{'class': 'AC422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.525, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 5},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'B', 'professor': 11.792, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 1},
{'class': 'AD422', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 7},
{'class': 'AE422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.091, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 3},
{'class': 'R0812', 'class_type': 'AP', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Thursday', 'timeslot': '19:00-19:50', 'et': 3},
{'class': 'HE622', 'class_type': 'AP', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Thursday', 'timeslot': '19:50-20:40', 'et': 1},
{'class': 'AD422', 'class_type': 'AP', 'class_group': 'A', 'professor': 12.274, 'timeslot_day': 'Thursday', 'timeslot': '19:50-20:40', 'et': 7},
{'class': 'AC422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.525, 'timeslot_day': 'Thursday', 'timeslot': '20:55-21:45', 'et': 5},
{'class': 'HF222', 'class_type': 'AV', 'class_group': 'B', 'professor': 13.0, 'timeslot_day': 'Thursday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'HE822', 'class_type': 'AT', 'class_group': 'A', 'professor': 11.792, 'timeslot_day': 'Thursday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'HF222', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.034, 'timeslot_day': 'Thursday', 'timeslot': '21:45-22:35', 'et': 1},
{'class': 'R8512', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.472, 'timeslot_day': 'Thursday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'AC322', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.875, 'timeslot_day': 'Thursday', 'timeslot': '21:45-22:35', 'et': 5},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.642, 'timeslot_day': 'Thursday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'R0812', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.472, 'timeslot_day': 'Friday', 'timeslot': '13:35-14:25', 'et': 3},
{'class': 'AC922', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.642, 'timeslot_day': 'Friday', 'timeslot': '13:35-14:25', 'et': 7},
{'class': 'HF222', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.0, 'timeslot_day': 'Friday', 'timeslot': '17:10-18:00', 'et': 1},
{'class': 'GJ922', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.776, 'timeslot_day': 'Friday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'GL822', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Friday', 'timeslot': '17:10-18:00', 'et': 5},
{'class': 'R0812', 'class_type': 'AT', 'class_group': 'B', 'professor': 14.472, 'timeslot_day': 'Friday', 'timeslot': '17:10-18:00', 'et': 3},
{'class': 'HE622', 'class_type': 'AP', 'class_group': 'A', 'professor': 13.07, 'timeslot_day': 'Friday', 'timeslot': '18:00-18:50', 'et': 1},
{'class': 'HE622', 'class_type': 'AP', 'class_group': 'B', 'professor': 13.07, 'timeslot_day': 'Friday', 'timeslot': '18:00-18:50', 'et': 1},
{'class': 'AD222', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.616, 'timeslot_day': 'Friday', 'timeslot': '18:00-18:50', 'et': 7},
{'class': 'R8512', 'class_type': 'AP', 'class_group': 'B', 'professor': 14.642, 'timeslot_day': 'Friday', 'timeslot': '19:00-19:50', 'et': 3},
{'class': 'GL822', 'class_type': 'AP', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Friday', 'timeslot': '19:50-20:40', 'et': 5},
{'class': 'AC422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.525, 'timeslot_day': 'Friday', 'timeslot': '19:50-20:40', 'et': 5},
{'class': 'R0812', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Friday', 'timeslot': '19:50-20:40', 'et': 3},
{'class': 'HE722', 'class_type': 'AP', 'class_group': 'A', 'professor': 14.525, 'timeslot_day': 'Friday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'HE622', 'class_type': 'AT', 'class_group': 'B', 'professor': 13.07, 'timeslot_day': 'Friday', 'timeslot': '20:55-21:45', 'et': 1},
{'class': 'AE422', 'class_type': 'AT', 'class_group': 'A', 'professor': 14.091, 'timeslot_day': 'Friday', 'timeslot': '21:45-22:35', 'et': 3},
{'class': 'GL822', 'class_type': 'AT', 'class_group': 'A', 'professor': 13.034, 'timeslot_day': 'Friday', 'timeslot': '21:45-22:35', 'et': 5}
])

for i in genome:
    print(i)

to_be_replaced = []
to_be_scheduled = []
for incorrectly_assigned_class in incorrectly_assigned_classes:
    class_name = incorrectly_assigned_class['class']
    for class_type in incorrectly_assigned_class:
        if class_type != 'class':

            # loop over the values of the class_type
            for class_group in incorrectly_assigned_class[class_type]:

                # get the value of the class_group
                class_value = incorrectly_assigned_class[class_type][class_group]
                if class_value > 0:
                    for value in range(class_value):
                        to_be_scheduled.append({'class': class_name, 'class_type': class_type[3::].upper(), 'class_group': class_group})
                elif class_value < 0:
                    for value in range(abs(class_value)):
                        to_be_replaced.append({'class': class_name, 'class_type': class_type[3::].upper(), 'class_group': class_group})
# to_be_replaced = [{'class': {'class': 'GJ922', 'nr_at': {'A': 0, 'B': 0}, 'nr_ap': {'A': -1, 'B': 0}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AP', 'class_group': 'A'}, {'class': {'class': 'GK622', 'nr_at': {'A': 0}, 'nr_ap': {'A': -2}, 'nr_av': {'A': -1}}, 'class_type': 'AP', 'class_group': 'A'}, {'class': {'class': 'GK622', 'nr_at': {'A': 0}, 'nr_ap': {'A': -2}, 'nr_av': {'A': -1}}, 'class_type': 'AP', 'class_group': 'A'}, {'class': {'class': 'GK622', 'nr_at': {'A': 0}, 'nr_ap': {'A': -2}, 'nr_av': {'A': -1}}, 'class_type': 'AV', 'class_group': 'A'}, {'class': {'class': 'AC922', 'nr_at': {'A': 1}, 'nr_ap': {'A': -1}, 'nr_av': {'A': 0}}, 'class_type': 'AP', 'class_group': 'A'}, {'class': {'class': 'AD422', 'nr_at': {'A': 0}, 'nr_ap': {'A': 0}, 'nr_av': {'A': -2}}, 'class_type': 'AV', 'class_group': 'A'}, {'class': {'class': 'AD422', 'nr_at': {'A': 0}, 'nr_ap': {'A': 0}, 'nr_av': {'A': -2}}, 'class_type': 'AV', 'class_group': 'A'}]
# to_be_scheduled = [{'class': {'class': 'HE822', 'nr_at': {'A': 3, 'B': 0}, 'nr_ap': {'A': 0, 'B': 0}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AT', 'class_group': 'A'}, {'class': {'class': 'HE822', 'nr_at': {'A': 3, 'B': 0}, 'nr_ap': {'A': 0, 'B': 0}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AT', 'class_group': 'A'}, {'class': {'class': 'HE822', 'nr_at': {'A': 3, 'B': 0}, 'nr_ap': {'A': 0, 'B': 0}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AT', 'class_group': 'A'}, {'class': {'class': 'HE622', 'nr_at': {'A': 0, 'B': 0}, 'nr_ap': {'A': 0, 'B': 1}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AP', 'class_group': 'B'}, {'class': {'class': 'AE422', 'nr_at': {'A': 0, 'B': 1}, 'nr_ap': {'A': 0, 'B': 0}, 'nr_av': {'A': 0, 'B': 0}}, 'class_type': 'AT', 'class_group': 'B'}, {'class': {'class': 'AD322', 'nr_at': {'A': 1}, 'nr_ap': {'A': 0}, 'nr_av': {'A': 0}}, 'class_type': 'AT', 'class_group': 'A'}, {'class': {'class': 'AC922', 'nr_at': {'A': 1}, 'nr_ap': {'A': -1}, 'nr_av': {'A': 0}}, 'class_type': 'AT', 'class_group': 'A'}]

for index in range(len(to_be_replaced)):
    print("To be replaced: ", to_be_replaced[index])
    print("To be scheduled: ", to_be_scheduled[index])

    # keys_to_check = ['class', 'class_type', 'class_group']

    # index_to_be_replaced = np.where([all(item[key] == value for key, value in zip(keys_to_check, to_be_replaced[index].values())) for item in genome])[0][0]
    # print("Index to be replaced: ", index_to_be_replaced)
    for class_scheduling in genome:
        class_name = class_scheduling['class']
        class_type = class_scheduling['class_type']
        class_group = class_scheduling['class_group']
        if class_name == to_be_replaced[index]['class']['class'] and class_type == to_be_replaced[index]['class_type'] and class_group == to_be_replaced[index]['class_group']:
            index_to_be_replaced = np.where(genome == class_scheduling)[0][0]
            print("Index to be replaced: ", index_to_be_replaced)
            break
    # print(genome[index_to_be_replaced])
    genome[index_to_be_replaced]['class'] = to_be_scheduled[index]['class']
    genome[index_to_be_replaced]['class_type'] = to_be_scheduled[index]['class_type']
    genome[index_to_be_replaced]['class_group'] = to_be_scheduled[index]['class_group']

# for i in genome:
#     print(i)
                