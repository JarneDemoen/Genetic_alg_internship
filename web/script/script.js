'use strict';
var HTMLschedule_grid;
var HTMLleft_arrow;
var HTMLright_arrow;
var HTMLGenerateScheduleButton;

function drawScheduleLines(){
    var content = "";
    for (let i = 0; i < 5; i++) {
        for (let j = 0; j < 17; j++) {
            content += `<div style="grid-column:${i} ; grid-row: ${j};"></div>`
        }
    }
    HTMLschedule_grid.innerHTML = content;
}

function listenToClickArrow(){
    const HTMLperiod = document.querySelector('.period');
    var period = HTMLperiod.innerHTML;
    HTMLleft_arrow.addEventListener('click', function(){
        if (period == "September-January")
        {
            period = "February-June";
            HTMLleft_arrow.style.display = "none";
            HTMLright_arrow.style.display = "block";
        }
        else
        {
            period = "September-January";
            HTMLleft_arrow.style.display = "none";
            HTMLright_arrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
    HTMLright_arrow.addEventListener('click', function(){
        if (period == "September-January")
        {
            period = "February-June";
            HTMLright_arrow.style.display = "none";
            HTMLleft_arrow.style.display = "block";
        }
        else
        {
            period = "September-January";
            HTMLright_arrow.style.display = "none";
            HTMLleft_arrow.style.display = "block";
        }
        HTMLperiod.innerHTML = period;
    });
}

function showTest(jsonObject) {
    console.log(jsonObject);
  };

function showSchedule(jsonObject){
    console.log(jsonObject);
}

function listenToClickGenerateScheduleButton(){
    HTMLGenerateScheduleButton.addEventListener('click', function(){
        handleData(`http://localhost:5000/api/v1/generate_timetable`, showSchedule, 'GET');
    }
)};

function init(){
    console.log("DOM Loaded")
    HTMLschedule_grid = document.querySelector('.schedule-grid');
    HTMLleft_arrow = document.querySelector('.left-arrow');
    HTMLright_arrow = document.querySelector('.right-arrow');
    HTMLGenerateScheduleButton = document.querySelector('.generate-schedule-button');

    listenToClickArrow()
    drawScheduleLines();
    listenToClickGenerateScheduleButton();
}
document.addEventListener('DOMContentLoaded', init);