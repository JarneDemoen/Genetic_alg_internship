'use strict';
var HTMLScheduleGrid;
var HTMLLeftArrow;
var HTMLRightArrow;
var HTMLGenerateScheduleButton;
var HTMLSemesterSelection;
var HTMLClassSelection;

function drawScheduleLines(){
    var content = "";
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 17; j++) {
            content += `<div style="grid-column:${i} ; grid-row: ${j};"></div>`
        }
    }
    HTMLScheduleGrid.innerHTML = content;
}

function listenToClickArrow(){
    const HTMLperiod = document.querySelector('.period');
    var period = HTMLperiod.innerHTML;
    HTMLLeftArrow.addEventListener('click', function(){
        if (period == "September - January")
        {
            period = "February - June";
            HTMLLeftArrow.style.display = "none";
            HTMLRightArrow.style.display = "block";
        }
        else
        {
            period = "September - January";
            HTMLLeftArrow.style.display = "none";
            HTMLRightArrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
    HTMLRightArrow.addEventListener('click', function(){
        if (period == "September - January")
        {
            period = "February - June";
            HTMLRightArrow.style.display = "none";
            HTMLLeftArrow.style.display = "block";
        }
        else
        {
            period = "September - January";
            HTMLRightArrow.style.display = "none";
            HTMLLeftArrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
}

function getScheduleData(jsonObject){
    console.log(jsonObject);
    var semesterSelection = document.querySelector('.js-semester-selection');
    var classSelection = document.querySelector('.js-class-selection');
    // get the values of the selected options
    var semesterSelectionValue = semesterSelection.options[semesterSelection.selectedIndex].value;
    var classSelectionValue = classSelection.options[classSelection.selectedIndex].value;
    console.log(semesterSelectionValue);
    console.log(classSelectionValue);
}

function listenToClickGenerateScheduleButton(){
    HTMLGenerateScheduleButton.addEventListener('click', function(){
        var semester = document.querySelector('.period').innerHTML;
        console.log(semester);
        // handleData(`http://localhost:5000/api/v1/generate_timetable/${semester}`, getScheduleData, 'GET');
        var jsonObject = [
            {
                "class_data": {
                    "class": "AD522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": null,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Monday"
            },
            {
                "class_data": {
                    "class": "RG312",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT"
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Monday"
            },
            {
                "class_data": {
                    "class": "RG712",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": 14.642,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": "A",
                    "class_types": "AP"
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": "B",
                    "class_types": "AP"
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "RG712",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": 14.642,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AC622",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP"
                },
                "professor": 13,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": "B",
                    "class_types": "AP"
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AC522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT"
                },
                "professor": 45,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Wednesday"
            },
            {
                "class_data": {
                    "class": "AB522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": 14.525,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Wednesday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT"
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Wednesday"
            },
            {
                "class_data": {
                    "class": "RG312",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT"
                },
                "professor": 45,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AC822",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": [
                        "AT",
                        "AP"
                    ]
                },
                "professor": 14.525,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AD522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP"
                },
                "professor": 14.642,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": "A",
                    "class_types": "AP"
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AB322",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": null,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AB522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP"
                },
                "professor": 14.525,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AC522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP"
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AB422",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": [
                        "AT",
                        "AP"
                    ]
                },
                "professor": 13.034,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Friday"
            },
            {
                "class_data": {
                    "class": "AC622",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT"
                },
                "professor": 13,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Friday"
            },
            {
                "class_data": {
                    "class": "FU422",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": [
                        "AT",
                        "AV"
                    ]
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Friday"
            }
        ]
        getScheduleData(jsonObject);
    }
)};

function init(){
    console.log("DOM Loaded")
    HTMLScheduleGrid = document.querySelector('.schedule-grid');
    HTMLLeftArrow = document.querySelector('.left-arrow');
    HTMLRightArrow = document.querySelector('.right-arrow');
    HTMLGenerateScheduleButton = document.querySelector('.generate-schedule-button');

    listenToClickArrow()
    drawScheduleLines();
    listenToClickGenerateScheduleButton();
}
document.addEventListener('DOMContentLoaded', init);