// Search with form
// http://127.0.0.1:8000/school/search_student/?format=json&search=

// Get elements
const searchButton = document.getElementById("search-button");
const searchInput  = document.getElementById('search-input');
const container = document.getElementById('container');
const h3 = document.createElement('h3');

// Add eventlisteners
searchButton.addEventListener('click', searchB);
searchInput.addEventListener('change',searchB);
searchInput.addEventListener('input',searchB);

function searchB(event){
    const searchInput = document.getElementById('search-input');
    const query = searchInput.value;
    // if query == ' ' don't make a request
    fetch(`http://127.0.0.1:8000/school/search_student/?format=json&search=${query}`).then(onResponse).then(onJsonReady)
}


function onJsonReady(json){
    if (json.length > 0){
        tableBody = document.getElementById('students-table-body');
        tableBody.innerHTML=' ';
        json.forEach((student)=>{
            row = document.createElement('tr');
            tableBody.appendChild(row);
            a = document.createElement('a');
            a.href = `http://127.0.0.1:8000/school/students/${student['pk']}`;
            a.text = student['first_name'] + ' ' + student['last_name'];
            row.insertCell(0).appendChild(a);
            classroom = document.createElement('a');
            classroom.href= `http://127.0.0.1:8000/school/classrooms/${student['classroom_pk']}`;
            classroom.text = student['classroom_number'];
            row.insertCell(1).appendChild(classroom);
            row.insertCell(2).textContent = student['level'];
            row.cells[0].classList.add('student-name');
            row.cells[1].classList.add('classroom');

            h3.style.display = 'none';        })
    
    }
    else {
        let table = document.getElementById('students-table');
        tableBody.innerHTML=' ';
        container.appendChild(h3);
        h3.textContent = 'No Results';
        h3.style.display = 'block';

    }
}

function onResponse(response){
    return response.json();
}

