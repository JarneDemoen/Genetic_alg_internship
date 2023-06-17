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
var HTMLContentBlur;
var HTMLLoader;
var HTMLScheduledClasses;
var HTMLPopup;
var HTMLClosePopup;
var HTMLCompleteSchedule;
var HTMLEmptyScheduleText;

var scroll = true;

var scheduleDataEven = [];
var scheduleDataOdd = [];
var scheduleData = [];
var uniqueClasses = []

var debugMode = false;

var timeslots = [
    "07","08","09","10","11","12",
    "13","14","15","16","17","18",
    "19","20","21", "22", "23"]

var days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

function drawScheduleLines(){
    console.log("drawScheduleLines")
    var content = "";
    for (let i = 1; i < 6; i++) {
        for (let j = 1; j < 18; j++) {
            content += `<div style="grid-column:${i} ; grid-row: ${j};"></div>`
        }
    }
    return content;
}

function listenToClickArrow(){
    console.log("listenToClickArrow")
    const HTMLperiod = document.querySelector('.period');
    var period = HTMLperiod.innerHTML;
    // add an event listener to all of the elements with the class .js-period
    HTMLperiodSelection.forEach(element => {
        element.addEventListener('click', function(){
            if (period == "August - December")
            {
                period = "February - June";
                scheduleData = scheduleDataEven;
            }
            else
            {
                period = "August - December";
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

function getPixelsToMoveDown(startMinute){
    startMinute = parseInt(startMinute);
    return (startMinute / 60) * 70;
}

function getStartHourAndMinute_2(startHour_1, startMinute_1){
    startHour_1 = parseInt(startHour_1);
    startMinute_1 = parseInt(startMinute_1);
    var startMinute_2 = startMinute_1 + 50;
    var startHour_2 = startHour_1;
    if (startMinute_2 >= 60)
    {
        startMinute_2 = startMinute_2 - 60;
        startHour_2 = startHour_1 + 1;
    }
    return [String(startHour_2), String(startMinute_2)];
}

function getColorIndex(classCode){
    var index = uniqueClasses.indexOf(classCode);
    return index + 1;
}

function showScheduleData(scheduleData){
    console.log("showScheduleData")
    var content = "";
    content += drawScheduleLines();
    for(let i = 0; i < scheduleData.length; i++){
        var classTypes = scheduleData[i].class_data.class_types;
        var class_code = scheduleData[i].class_data.class;
        var class_name = scheduleData[i].class_data.class_name;
        var professor_name = scheduleData[i].professor_name;
        var class_type_1 = classTypeString(scheduleData[i].class_data.class_types[0]);
        var timeslot = scheduleData[i].timeslot;
        var timeslot_day = scheduleData[i].timeslot_day;
        var timeRange = timeslot;
        var startEndTimes = timeRange.split("-");
        var startTime = startEndTimes[0].trim();
        var startHour_1 = startTime.split(":")[0];
        var startMinute_1 = startTime.split(":")[1];
        
        var index_timeslot_start_1 = timeslots.indexOf(startHour_1);
        var index_timeslot_day = days.indexOf(timeslot_day);
        var pixels_to_move_down_1 = getPixelsToMoveDown(startMinute_1);
        
        if (classTypes.length == 2)
        {
            var startHour_2 = getStartHourAndMinute_2(startHour_1, startMinute_1)[0];
            var startMinute_2 = getStartHourAndMinute_2(startHour_1, startMinute_1)[1];
            var index_timeslot_start_2 = timeslots.indexOf(startHour_2);
            var pixels_to_move_down_2 = getPixelsToMoveDown(startMinute_2);
            var class_type_2 = classTypeString(scheduleData[i].class_data.class_types[1]);

            // startminute 2 has to have 2 digits, add a zero if it only has one digit
            if (startMinute_2.length == 1)
            {
                startMinute_2 = "0" + startMinute_2;
            }

            var timeslot_1 = startHour_1 + ":" + startMinute_1 + " - " + startHour_2 + ":" + startMinute_2;
            var timeslot_2 = startHour_2 + ":" + startMinute_2 + " -" + startEndTimes[1]

            content += `
            <div class="scheduled-class-half js-scheduled-class" style="grid-column: ${index_timeslot_day + 1}; grid-row: ${index_timeslot_start_1 + 1}; border-bottom: None; transform: translateY(${pixels_to_move_down_1}px);">
                <div class="scheduled-class-wrapper">
                    <div class="scheduled-class-color" style="background-color:var(--UNAERP-color-${getColorIndex(class_code)})";></div>
                    <div class="scheduled-class-content-half">
                        <p class="class-code-type">${class_code} - ${class_type_1}</p>
                        <p class="class-name">${class_name}</p>
                        <p class="professor" style="display: none;">${professor_name}</p>
                        <p class="class-time" style="display: none;">${timeslot_1}</p>
                    </div>
                </div>
            </div>`
            content += `
            <div class="scheduled-class-half js-scheduled-class" style="grid-column: ${index_timeslot_day + 1}; grid-row: ${index_timeslot_start_2 + 1}; border-bottom: None; transform: translateY(${pixels_to_move_down_2}px);">
                <div class="scheduled-class-wrapper">
                    <div class="scheduled-class-color" style="background-color:var(--UNAERP-color-${getColorIndex(class_code)})";></div>
                    <div class="scheduled-class-content-half">
                        <p class="class-code-type">${class_code} - ${class_type_2}</p>
                        <p class="class-name">${class_name}</p>
                        <p class="professor" style="display: none;">${professor_name}</p>
                        <p class="class-time" style="display: none;">${timeslot_2}</p>
                    </div>
                </div>
            </div>`
        }
        else
        {
            content += `
            <div class="scheduled-class-full js-scheduled-class" style="grid-column: ${index_timeslot_day + 1}; grid-row: ${index_timeslot_start_1 + 1} / span 2; border-bottom: None; transform: translateY(${pixels_to_move_down_1}px);">
                <div class="scheduled-class-wrapper">
                    <div class="scheduled-class-color" style="background-color:var(--UNAERP-color-${getColorIndex(class_code)})";></div>
            
                        <div class="scheduled-class-content-full">
                            <p class="class-code-type">${class_code} - ${class_type_1}</p>
                            <p class="class-name">${class_name}</p>
                            <p class="professor" style="display: none;">Prof: ${professor_name}</p>
                            <p class="class-time" style="display: none";>${timeslot}</p>
                        </div>
                        <div class="scheduled-class-content-half-time">
                            <p class="class-time" style="display: none";>${timeslot}</p>
                        </div>
                    
                </div>
            </div>`
        }
    }
    HTMLSchedule.innerHTML = content;
    uniqueClasses = [];
    toggleCompleteSchedule();
    listenToClickScheduledClasses();
}

function fillContentPopup(HTMLscheduledClass){
    console.log("Fill content popup")
    console.log("HTMLscheduledClass: ",HTMLscheduledClass)
    const childElements = HTMLscheduledClass.children;
    const childOfChildElements = childElements[0].children;
    const content = childOfChildElements[1].children;
    const classCode = content[0].innerHTML.split(" - ")[0];
    const classType = content[0].innerHTML.split(" - ")[1];
    const className = content[1].innerHTML;
    const professorName = content[2].innerHTML;
    const classTime = content[3].innerHTML;

    console.log("classCode: ",classCode)
    console.log("classType: ",classType)
    console.log("className: ",className)
    console.log("professorName: ",professorName)
    console.log("classTime: ",classTime)
    console.log("HTMLPopup: ",HTMLPopup)

    const HTMLPopupContent = document.querySelector('.js-popup-content');
    var contentString = `
        <p>${classCode}</p>
        <p>${className}</p>
        <p>${classType}</p>
        <p>${professorName}</p>
        <p>${classTime}</p>
        `
    HTMLPopupContent.innerHTML = contentString;
}

function handlePopupClose() {
    console.log("Close popup");
    HTMLPopup.style.display = "none";
    blurContent(HTMLPopup, "block");
    HTMLClosePopup.removeEventListener('click', handlePopupClose);
}

function listenToClickScheduledClasses(){
    console.log("listenToClickScheduledClasses")
    HTMLScheduledClasses = document.querySelectorAll('.js-scheduled-class');
    HTMLScheduledClasses.forEach(element => {
        element.addEventListener('click', function(){
            HTMLPopup.style.display = "block";
            blurContent(HTMLPopup, "block");
            HTMLClosePopup = document.querySelector('.js-close-popup');
            HTMLClosePopup.addEventListener('click', handlePopupClose);
            fillContentPopup(element);
    })});
}

function scrollIntoView(){
    HTMLScheduledClasses = document.querySelectorAll('.js-scheduled-class');
    console.log("scrollIntoView")
    HTMLScheduledClasses[0].scrollIntoView({
        behavior: 'smooth', // Scroll smoothly instead of instantly
        block: 'start',     // Scroll to the top of the element
        inline: 'nearest'   // Scroll horizontally as little as possible
      });
}

function filterScheduleData(scheduleData){
    console.log("filterScheduleData")
    var semesterSelectionValue = parseInt(HTMLsemesterSelection.options[HTMLsemesterSelection.selectedIndex].value);
    var classSelectionValue = String(HTMLclassSelection.options[HTMLclassSelection.selectedIndex].value);
    // filter the data according to the selected semester and class
    var filteredscheduleData = [];
    for (let i = 0; i < scheduleData.length; i++) {
        // create an if statement where the semester has to have the same value and the classSelectionValue has to be in the class_groups array
        if (scheduleData[i].class_data.semester == semesterSelectionValue && scheduleData[i].class_data.class_groups.includes(classSelectionValue)){
            filteredscheduleData.push(scheduleData[i]);
        }
    }
   
    for (let i = 0; i < filteredscheduleData.length; i++) {
        if (!uniqueClasses.includes(filteredscheduleData[i].class_data.class)){
            uniqueClasses.push(filteredscheduleData[i].class_data.class);
        }
    }

    showScheduleData(filteredscheduleData);
}

function getScheduleData(jsonObject){
    console.log("getScheduleData")
    blurContent(HTMLLoader, "flex");
    // get the values of the selected options
    var period = document.querySelector('.period').innerHTML;
    if (period == 'August - December')
    {
        scheduleDataOdd = jsonObject;
    }
    else
    {
        scheduleDataEven = jsonObject;
    }
    setTurmaSelection();
    filterScheduleData(jsonObject);
    setScheduleData();
}

function blurContent(item, display_value){
    console.log("blurContent")
    if (HTMLContentBlur.style.filter == "blur(5px)")
    {
        HTMLContentBlur.style.filter = "blur(0px)";
        item.style.display = "none";
        HTMLGenerateScheduleButton.disabled = false;
    }
    else
    {
        HTMLContentBlur.style.filter = "blur(5px)";
        item.style.display = display_value;
        HTMLGenerateScheduleButton.disabled = true;
    }
}

function listenToClickGenerateScheduleButton(){
    console.log("listenToClickGenerateScheduleButton")
    HTMLGenerateScheduleButton.addEventListener('click', function(){
        blurContent(HTMLLoader, "flex");
        var period = document.querySelector('.period').innerHTML;
        if (debugMode == false)
        {
            console.log("Generating schedule...")
            scroll = true;
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
    console.log("setSelection")
    // in the selection of .js-semester-selection, disable the even options
    var period = document.querySelector('.period').innerHTML;

    if (period == 'August - December')
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
    console.log("setTurmaSelection")
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
    console.log("setScheduleData")
    var period = document.querySelector('.period').innerHTML;
    if (period == 'August - December')
    {
        scheduleData = scheduleDataOdd;
    }
    else
    {
        scheduleData = scheduleDataEven;
    }
    toggleCompleteSchedule();
}

function toggleCompleteSchedule(){
    console.log("toggleCompleteSchedule")
    console.log("scheduleData: ",scheduleData)
    if (scheduleData.length == 0)
    {
        console.log("scheduleData is empty")
        HTMLCompleteSchedule.style.display = "none";
        HTMLEmptyScheduleText.style.display = "block";
    }
    else
    {
        console.log("scheduleData is not empty")
        HTMLCompleteSchedule.style.display = "flex";
        HTMLEmptyScheduleText.style.display = "none";
        if (scroll == true)
        {
            scrollIntoView();
            scroll = false;
        }
    }
}

function init(){
    console.log("DOM Loaded")
    HTMLGenerateScheduleButton = document.querySelector('.generate-schedule-button');
    HTMLsemesterSelection = document.querySelector('.js-semester-selection');
    HTMLclassSelection = document.querySelector('.js-class-selection');
    HTMLperiodSelection = document.querySelectorAll('.js-period');
    HTMLSchedule = document.querySelector('.js-schedule');
    HTMLContentBlur = document.querySelector('.js-content-wrapper-blur');
    HTMLLoader = document.querySelector('.container-loader');
    HTMLPopup = document.querySelector('.js-popup');
    HTMLCompleteSchedule = document.querySelector('.schedule');
    HTMLEmptyScheduleText = document.querySelector('.empty-schedule');

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

    toggleCompleteSchedule();
    listenToClickArrow()
    HTMLSchedule.innerHTML = drawScheduleLines();  
    listenToClickGenerateScheduleButton();
    setSelection();
}

document.addEventListener('DOMContentLoaded', init);