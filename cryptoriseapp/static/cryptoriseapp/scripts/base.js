
"use strict"

function $(c) {
    return document.getElementById(c);
}

// side bar program

let sidebody = $('side_body');
var is_open = false;
let mianchat = $('chat_holder');
let chatbutton = document.getElementsByClassName('chat_bar')[0];
let mission = $('mission_act');
let invests = $('plans'), about_action = $('actions');


function sidebar(param) {
   let elem = param;
    if (is_open==false) {
        sidebody.style.transform = 'translateX(0%)';
        is_open = true;
        elem.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentcolor"><path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>`
    }
    else{
        sidebody.style.transform = 'translateX(100%)';
        is_open = false;
        elem.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentcolor"><path d="M120-240v-80h720v80H120Zm0-200v-80h720v80H120Zm0-200v-80h720v80H120Z"/></svg>`
    }
}

function openchat(param){
    let chatbar = param
    chatbar.style.display = 'none';
    mianchat.style.display = 'block';
}

function closechat() {
    mianchat.style.display = 'none';
    chatbutton.style.display = 'flex';
}


// intersection onserver

const observer = new IntersectionObserver(
    callbackfucntion,
    option,
)

function callbackfucntion(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.id == 'mission_act') {
                mission.classList.add('fade_in');
            }
            if (entry.target.id=='plans') {
                invests.classList.add('popin')
            }
            if(entry.target.id=='actions') {
                about_action.classList.add('scroll_to');
            }
        }
    });
}

var option = {
    rootMargin: "0px",
    threshold: 1,
}

observer.observe(mission);
observer.observe(invests);

