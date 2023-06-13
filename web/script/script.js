'use strict';

var HTMLLeftArrow;
var HTMLRightArrow;
var HTMLGenerateScheduleButton;
var HTMLSemesterSelection;
var HTMLClassSelection;
var HTMLsemesterSelection;
var HTMLperiodSelection;
var HTMLclassSelection;
var HTMLLeftArrow;
var HTMLRightArrow;
var HTMLSchedule;

var scheduleDataEven = [];
var scheduleDataOdd = [];
var scheduleData = [];

var occupiedTimeslotDays = [];
var occupiedTimeslots = [];

var debugMode = true;
// var timeslots = [
//     "07:10","08:00","08:50","09:55","10:45","11:35",
//     "12:45","13:35","14:25","15:30","16:20","17:10",
//     "19:00","19:50","20:55","21:45"]

var timeslots = [
    "07","08","09","10","11","12",
    "13","14","15","16","17","18",
    "19","20","21", "22", "23"]

var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

function drawScheduleLines(occupiedTimeslots){
    console.log("occupiedTimeslots: ",occupiedTimeslots)
    var content = "";
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 17; j++) {
            if(occupiedTimeslots.includes(j) && occupiedTimeslotDays.includes(i))
            {
                continue
            }
            else
            {
                content += `<div style="grid-column:${i} ; grid-row: ${j};"></div>`
            }
        }
    }
    return content;
}

function listenToClickArrow(){
    const HTMLperiod = document.querySelector('.period');
    var period = HTMLperiod.innerHTML;
    // add an event listener to all of the elements with the class .js-period
    HTMLperiodSelection.forEach(element => {
        element.addEventListener('click', function(){
            if (period == "Augustus - December")
            {
                period = "February - June";
                scheduleData = scheduleDataEven;
            }
            else
            {
                period = "Augustus - December";
                scheduleData = scheduleDataOdd;
            }
            HTMLperiod.innerHTML = period;

            if (HTMLRightArrow.style.display != "none")
            {
                HTMLLeftArrow.style.display = "block";
                HTMLRightArrow.style.display = "none";
            }
           
            else if(HTMLLeftArrow.style.display != "none")
            {
                HTMLLeftArrow.style.display = "none";
                HTMLRightArrow.style.display = "block";
            }
            setSelection();
            setTurmaSelection();
            filterScheduleData(scheduleData);
        })
    });
}

function classTypeString(classType){
    if (classType == 'AT'){
        return 'Theory'
    }
    else if (classType == 'AP'){
        return 'Lab'
    }
    else if (classType == 'AV'){
        return 'Virtual'
    }
}

function showScheduleData(scheduleData){
    occupiedTimeslots = [];
    var content = "";
    var colorIndex = 0;
    for(let i = 0; i < scheduleData.length; i++){
        var classTypes = scheduleData[i].class_data.class_types;
        if (Array.isArray(classTypes))
        {
            console.log(scheduleData[i])
            var class_code = scheduleData[i].class_data.class;
            var class_name = scheduleData[i].class_data.class_name;
            var professor_name = scheduleData[i].professor_name;
            var class_type_1 = classTypeString(scheduleData[i].class_data.class_types[0]);
            var class_type_2 = classTypeString(scheduleData[i].class_data.class_types[1]);
            var timeslot = scheduleData[i].timeslot;
            var timeslot_day = scheduleData[i].timeslot_day;
            
            var timeRange = timeslot;
            var startEndTimes = timeRange.split("-");

            var startTime = startEndTimes[0].trim();
            var endTime = startEndTimes[1].trim();

            var startHour = startTime.split(":")[0];
            var endHour = endTime.split(":")[0];

            var startMinute = startTime.split(":")[1];
            var endMinute = endTime.split(":")[1];
            
            var index_timeslot_start = timeslots.indexOf(startHour);
            var index_timeslot_end = timeslots.indexOf(endHour);
            var timeslot_day_index = days.indexOf(timeslot_day);

            console.log("index_timeslot_start: ",index_timeslot_start)
            console.log("index_timeslot_end: ",index_timeslot_end)
            occupiedTimeslots.push(index_timeslot_start);
            occupiedTimeslots.push(index_timeslot_end);
            occupiedTimeslotDays.push(timeslot_day_index);

            content += `
            <div class="scheduled-class-half" style="grid-column: ${timeslot_day_index}; grid-row: ${index_timeslot_start}; border-bottom: None">
                <div class="scheduled-class-wrapper">
                    <div class="scheduled-class-color" style="background-color:var(--UNAERP-color-${colorIndex})";></div>
                    <div class="scheduled-class-content">
                        <div class="scheduled-class-content-half">
                            <p class="class-code-type">${class_code} - ${class_type_1}</p>
                            <p class="class-name">${class_name}</p>
                            <p class="professor">Prof: ${professor_name}</p>
                        </div>
                        <div class="scheduled-class-content-half-time">
                            <p class="class-time">${timeslot}</p>
                        </div>
                    </div>
                </div>
            </div>`
            content += `
            <div class="scheduled-class-half" style="grid-column: ${timeslot_day_index}; grid-row: ${index_timeslot_end}; border-bottom: None">
                <div class="scheduled-class-wrapper">
                    <div class="scheduled-class-color" style="background-color:var(--UNAERP-color-${colorIndex})";></div>
                    <div class="scheduled-class-content">
                        <div class="scheduled-class-content-half">
                            <p class="class-code-type">${class_code} - ${class_type_2}</p>
                            <p class="class-name">${class_name}</p>
                            <p class="professor">Prof: ${professor_name}</p>
                        </div>
                        <div class="scheduled-class-content-half-time">
                            <p class="class-time">${timeslot}</p>
                        </div>
                    </div>
                </div>
            </div>`
        }
        colorIndex++;
    }
    content += drawScheduleLines(occupiedTimeslots);
    HTMLSchedule.innerHTML = content;
}

function filterScheduleData(scheduleData){
    console.log("scheduleData: ",scheduleData)
    var semesterSelectionValue = parseInt(HTMLsemesterSelection.options[HTMLsemesterSelection.selectedIndex].value);
    var classSelectionValue = String(HTMLclassSelection.options[HTMLclassSelection.selectedIndex].value);
    console.log("semesterSelectionValue: ",semesterSelectionValue)
    console.log("classSelectionValue: ",classSelectionValue)
    // filter the data according to the selected semester and class
    var filteredscheduleData = [];
    for (let i = 0; i < scheduleData.length; i++) {
        // create an if statement where the semester has to have the same value and the classSelectionValue has to be in the class_groups array
        if (scheduleData[i].class_data.semester == semesterSelectionValue && scheduleData[i].class_data.class_groups.includes(classSelectionValue)){
            filteredscheduleData.push(scheduleData[i]);
        }
    }
    console.log("Filtered object")
    console.log(filteredscheduleData);
    showScheduleData(filteredscheduleData);
}

function getScheduleData(jsonObject){
    // get the values of the selected options
    var period = document.querySelector('.period').innerHTML;
    if (period == 'Augustus - December')
    {
        scheduleDataOdd = jsonObject;
    }
    else
    {
        scheduleDataEven = jsonObject;
    }
    setTurmaSelection();
    filterScheduleData(jsonObject);
}

function listenToClickGenerateScheduleButton(){
    HTMLGenerateScheduleButton.addEventListener('click', function(){
        var period = document.querySelector('.period').innerHTML;
        if (debugMode == false)
        {
            console.log("Generating schedule...")
            handleData(`http://localhost:5000/api/v1/generate_timetable/${period}`, getScheduleData, 'GET');
        }
        else
        {
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
    }
)};

function setSelection(){
    // in the selection of .js-semester-selection, disable the even options
    var period = document.querySelector('.period').innerHTML;

    if (period == 'Augustus - December')
    {
        // set the selection to the first option
        HTMLsemesterSelection.selectedIndex = 0;
        var semesterSelectionOptions = document.querySelectorAll('.js-semester-selection option');
        for (let i = 0; i < semesterSelectionOptions.length; i++) {
            if (i % 2 == 1)
            {
                semesterSelectionOptions[i].disabled = true;
            }
            else {
                semesterSelectionOptions[i].disabled = false;
            }
        }
    }
    else
    {
        // set the selection to the second option
        HTMLsemesterSelection.selectedIndex = 1;
        var semesterSelectionOptions = document.querySelectorAll('.js-semester-selection option');
        for (let i = 0; i < semesterSelectionOptions.length; i++) {
            if (i % 2 == 0)
            {
                semesterSelectionOptions[i].disabled = true;
            }
            else {
                semesterSelectionOptions[i].disabled = false;
            }
        }
    }
}

function setTurmaSelection(){
    var semesterSelectionValue = parseInt(HTMLsemesterSelection.options[HTMLsemesterSelection.selectedIndex].value);

    if (semesterSelectionValue >= 4)
    {
        // disable the second option
        var classSelectionOptions = document.querySelectorAll('.js-class-selection option');
        // set the selection on the first value
        HTMLclassSelection.selectedIndex = 0;
        for (let i = 0; i < classSelectionOptions.length; i++) {
            if (i % 2 == 0)
            {
                classSelectionOptions[i].disabled = false;
            }
            else {
                classSelectionOptions[i].disabled = true;
            }
        }
    }
    else
    {
        var classSelectionOptions = document.querySelectorAll('.js-class-selection option');
        for (let i = 0; i < classSelectionOptions.length; i++) {
            classSelectionOptions[i].disabled = false;
        }
    }
}

function setScheduleData(){
    var period = document.querySelector('.period').innerHTML;
    if (period == 'Augustus - December')
    {
        scheduleData = scheduleDataOdd;
    }
    else
    {
        scheduleData = scheduleDataEven;
    }
}

function init(){
    console.log("DOM Loaded")
    HTMLGenerateScheduleButton = document.querySelector('.generate-schedule-button');
    HTMLsemesterSelection = document.querySelector('.js-semester-selection');
    HTMLclassSelection = document.querySelector('.js-class-selection');
    HTMLperiodSelection = document.querySelectorAll('.js-period');
    HTMLSchedule = document.querySelector('.js-schedule');

    HTMLLeftArrow = document.querySelector('.left-arrow');
    HTMLRightArrow = document.querySelector('.right-arrow');

    HTMLsemesterSelection.addEventListener('change', function(){
        setScheduleData();
        setTurmaSelection();
        filterScheduleData(scheduleData);
    });
    
    HTMLclassSelection.addEventListener('change', function(){
        setScheduleData();
        filterScheduleData(scheduleData);
    });

    listenToClickArrow()
    HTMLSchedule.innerHTML = drawScheduleLines(occupiedTimeslots);
    listenToClickGenerateScheduleButton();
    setSelection();
}

document.addEventListener('DOMContentLoaded', init);