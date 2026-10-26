"use strict";

window.addEventListener('DOMContentLoaded', function () {
    var dropDownMenu = this.document.getElementById('dropdown-menu');
    var dropDownContent = this.document.getElementById('dropdown-content');
    var submissionForm = document.getElementById('submission-form');

    //Safe the last 
    var savedReciever = localStorage.getItem('lastReciever');
    if (savedReciever) {
        submissionForm.action = `/submit?to=${encodeURIComponent(savedReciever)}`;
        document.getElementById('message-input').placeholder = `--->${savedReciever} `;
    }


    dropDownMenu.addEventListener('click', () => {
        dropDownContent.classList.toggle('show');
    });

    var onlineUsers = dropDownContent.querySelectorAll('p');
    onlineUsers.forEach(function (element) {
        element.addEventListener('click', function () {
            document.getElementById('message-input').placeholder = `--->${element.textContent} `;

            var submissionForm = document.getElementById('submission-form');
            var reciever = `${element.textContent}`;
            
            submissionForm.action = `/submit?to=${encodeURIComponent(reciever)}`;
            
            localStorage.setItem('lastReciever', reciever)
            dropDownContent.classList.toggle('show');
        });
    });
});