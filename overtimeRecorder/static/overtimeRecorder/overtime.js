function addTime(hour, minute){
    hour = parseInt(hour);
    minute = parseInt(minute);
    starttimeField = document.getElementById("id_startTime").value;
    endtimeField = document.getElementById("id_finishTime");
    const twentyFourH = /(\d+):(\d+)/;
    const twelveH = /(\d+):(\d+) *(\w+)/;
    const twelveHV2 = /(\d+) *(\w+)/;
    
    let output1 = starttimeField.match(twentyFourH);
    let output2 = starttimeField.match(twelveH);
    let output3 = starttimeField.match(twelveHV2);

    let textToOutput="";
    if (output1){
        let hourToprint = parseInt(output1[1])+ hour;
        let minuteToprint = parseInt(output1[2])+ minute;
        if (minuteToprint > 59){
            hourToprint += 1;
            minuteToprint = minuteToprint % 60;
        }
        textToOutput= (hourToprint).toString().padStart(2, "0") + ":" + (minuteToprint).toString().padStart(2, "0");
    } else if (output2){
        let hourToprint = parseInt(output2[1])+ hour;
        let minuteToprint = parseInt(output2[2])+ minute;
        if (minuteToprint > 59){
            hourToprint += 1;
            minuteToprint = minuteToprint % 60;
        }
        let ampm = output2[3];
        if (hourToprint > 12){
            hourToprint = hourToprint % 12;
            if (ampm.toLowerCase()=="pm"){
                ampm = "am";
            } else {
                ampm = "pm";
            }
        }
        textToOutput= (hourToprint).toString().padStart(2, "0") + ":" + (minuteToprint).toString().padStart(2, "0") + ampm;
    } else if (output3){
        let hourToprint = parseInt(output3[1])+ hour;
        let minuteToprint = 0;
        if (minute > 59){
            hourToprint += 1;
            minuteToprint = minute % 60;
        }
        let ampm = output3[2];
        if (hourToprint > 12){
            hourToprint = hourToprint % 12;
            if (ampm.toLowerCase()=="pm"){
                ampm = "am";
            } else {
                ampm = "pm";
            }
        }
        textToOutput= (hourToprint).toString().padStart(2, "0") + ":" + (minuteToprint).toString().padStart(2, "0") + ampm;
    }


    endtimeField.value = textToOutput;
    return false;
}
