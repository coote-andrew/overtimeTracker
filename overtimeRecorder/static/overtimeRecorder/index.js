window.addEventListener("load", function() {
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    function sendData(form, url, functionToCall) {
        const FD = new FormData(form)

        let dataManual = []
        FD.forEach((value, key) => {
            dataManual.push([key, value]);
            })

        sendFormAjax(url, dataManual, functionToCall)
    }

    const forms = document.getElementsByClassName("overtimeForm");

    for (let form of forms){

        form.addEventListener("submit", function(event) {
            event.preventDefault();
            sendData(form, "post/ajax/overtime/", "addOvertimeSpan");
        })
    }
    const deleteforms = document.getElementsByClassName("deleteOvertimeForm");

    for (let form of deleteforms){

        form.addEventListener("submit", function(event) {
            event.preventDefault();
            sendData(form, "post/ajax/overtimeDelete/","deleteThisRow");
        })
    }
    
    const createCalendarButton = document.getElementById('createCalendar');
    createCalendarButton.onclick = function(event){
        fetch("post/ajax/createCalendar", {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'post_data':'createCalendar'}) //JavaScript object of data to POST
        })
        .then(response => {
            return response.json(); //Convert response to JSON
        })
        .then(data => {
            let real_json = JSON.parse(data);
            console.log(real_json);
            if(real_json != "failed"){
                window.location = real_json;
            }
        })
    }


    function sendFormAjax(url, content, functionToCall){
        fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'post_data':content}) //JavaScript object of data to POST
        })
        .then(response => {
            return response.json(); //Convert response to JSON
        })
        .then(data => {
            let real_json = JSON.parse(data);
            if(functionToCall=="addOvertimeSpan"){
                addOvertimeSpan(real_json);
            } else if (functionToCall=="deleteThisRow") {
                deleteThisRow(real_json);
            }
        })
    }

    function addOvertimeSpan(jsonData){
        // console.log("we got here")
        let overtime_section = document.getElementById(jsonData[0].date).getElementsByClassName('firstrow');
        let overtimeText = document.createElement('span');
        overtimeText.classList.add("currentOvertimeRequests");
        let patientURNText = ""
        if(jsonData[0].patientURN){
            patientURNText = ":#" + jsonData[0].patientURN
        }
        let makeText = jsonData[0].startTime.replace("AM", "a.m.").replace("PM", "p.m.") + "-" + jsonData[0].finishTime.replace("AM", "a.m.").replace("PM", "p.m.") + "(" + jsonData[0].reason + patientURNText +")";
        overtimeText.innerHTML = makeText;
        overtime_section[0].appendChild(overtimeText)
    }
    function deleteThisRow(jsonData){
        console.log(jsonData)
        if (jsonData){
            
            let overtime_section = document.getElementById(jsonData.id);
            overtime_section.remove()
        }
    }
});