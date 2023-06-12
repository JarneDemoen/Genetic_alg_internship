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
        if (period == "Augustus - December")
        {
            period = "February - June";
            HTMLLeftArrow.style.display = "none";
            HTMLRightArrow.style.display = "block";
        }
        else
        {
            period = "Augustus - December";
            HTMLLeftArrow.style.display = "none";
            HTMLRightArrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
    HTMLRightArrow.addEventListener('click', function(){
        if (period == "Augustus - December")
        {
            period = "February - June";
            HTMLRightArrow.style.display = "none";
            HTMLLeftArrow.style.display = "block";
        }
        else
        {
            period = "Augustus - December";
            HTMLRightArrow.style.display = "none";
            HTMLLeftArrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
}

function filterScheduleData(jsonObject, semesterSelectionValue, classSelectionValue){
    // filter the data according to the selected semester and class
    var filteredJsonObject = [];
    for (let i = 0; i < jsonObject.length; i++) {
        // create an if statement where the semester has to have the same value and the classSelectionValue has to be in the class_groups array
        if (jsonObject[i].class_data.semester == semesterSelectionValue && jsonObject[i].class_data.class_groups.includes(classSelectionValue)){
            filteredJsonObject.push(jsonObject[i]);
        }
    }
    console.log("Filtered object")
    console.log(filteredJsonObject);
}

function getScheduleData(jsonObject){
    console.log(jsonObject);
    var semesterSelection = document.querySelector('.js-semester-selection');
    var classSelection = document.querySelector('.js-class-selection');
    // get the values of the selected options
    var semesterSelectionValue = parseInt(semesterSelection.options[semesterSelection.selectedIndex].value);
    var classSelectionValue = String(classSelection.options[classSelection.selectedIndex].value);
    filterScheduleData(jsonObject, semesterSelectionValue, classSelectionValue);
}

function listenToClickGenerateScheduleButton(){
    HTMLGenerateScheduleButton.addEventListener('click', function(){
        var semester = document.querySelector('.period').innerHTML;
        // handleData(`http://localhost:5000/api/v1/generate_timetable/${semester}`, getScheduleData, 'GET');
        var jsonObject = [
            {
                "class_data": {
                    "class": "AB522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 4
                },
                "professor": 14.525,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Monday"
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
                    ],
                    "semester": 6
                },
                "professor": 14.525,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Monday"
            },
            {
                "class_data": {
                    "class": "RG312",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Tuesday"
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
                    ],
                    "semester": 4
                },
                "professor": 14.472,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": "A",
                    "class_types": "AP",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": "B",
                    "class_types": "AP",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AB322",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 4
                },
                "professor": null,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AC522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP",
                    "semester": 6
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": "A",
                    "class_types": "AP",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Tuesday"
            },
            {
                "class_data": {
                    "class": "RG712",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 4
                },
                "professor": null,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Wednesday"
            },
            {
                "class_data": {
                    "class": "AD522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 8
                },
                "professor": 12.274,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Wednesday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Wednesday"
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
                    ],
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AC622",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 6
                },
                "professor": 13,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "RG312",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "RG712",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 4
                },
                "professor": null,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AC622",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP",
                    "semester": 6
                },
                "professor": null,
                "timeslot": "19:00-20:40",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "FV722",
                    "class_groups": [
                        "A",
                        "B"
                    ],
                    "class_types": "AT",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AC522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AT",
                    "semester": 6
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Thursday"
            },
            {
                "class_data": {
                    "class": "AB522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP",
                    "semester": 4
                },
                "professor": 14.525,
                "timeslot": "17:10-18:50",
                "timeslot_day": "Friday"
            },
            {
                "class_data": {
                    "class": "AB122",
                    "class_groups": "B",
                    "class_types": "AP",
                    "semester": 2
                },
                "professor": 45,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Friday"
            },
            {
                "class_data": {
                    "class": "AD522",
                    "class_groups": [
                        "A"
                    ],
                    "class_types": "AP",
                    "semester": 8
                },
                "professor": 14.642,
                "timeslot": "20:55-22:35",
                "timeslot_day": "Friday"
            }
        ];
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