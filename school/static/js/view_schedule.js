function onResponse(response){
    return response.json();
}

function onJsonReady(json){
    const day = parseInt(json['day'])+1;
    const class_number_in_day = json['class_number_in_day'];
    const table = document.getElementById('schedule');
    table.rows[day].cells[class_number_in_day].textContent = json['class_name'].slice(0,-4); // slice to remove classroom number from class name i.e: _101

}

function loadSchedule(){
    hidden_table = document.getElementById('hidden-table');
    length = hidden_table.rows.length;
    for (let i=0; i<length;i++){
        const class_pk = hidden_table.rows[i].cells[0].textContent;
        // fetch class_pk
        fetch(`http://127.0.0.1:8000/school/view_schedule/${class_pk}.json`)
        .then(onResponse)
        .then(onJsonReady)
    }

}

loadSchedule();
