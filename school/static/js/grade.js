// Get CSRF value from cookie to use it in POST request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
// POST Function to update Grade
async function postData(url='',data={}){
    const response = await fetch(url,{
        method: 'PUT',
        mode: 'cors',
        credentials:'same-origin',
        headers: {
            'content-type':'application/json',
            "X-CSRFToken":csrftoken,
        },
        redirect:'follow',
        referrerPolicy:'no-referrer',
        body: JSON.stringify(data)
    });
    return response.json();
}

// Add eventListens to all grade inputs
const grade = document.querySelectorAll('.grade');
grade.forEach((grade) => {
    grade.addEventListener('change', updateValue);
})

function updateValue(event){
    // get new value
    const newValue = event.target.value;
    // get the parent of value [cell] and get parent of the previous parent --> row
    const parent= event.target.parentNode.parentNode;
    // get first cell of the row
    const grade_pk= parent.cells[0].innerHTML;
    //console.log(newValue,grade_pk)
    url = `http://127.0.0.1:8000/school/update_grade_api/${grade_pk}.json?`;
    postData(url,{value:newValue})//.then(data =>{console.log(data)});
    /* print updated beside this grade or change color*/
    const cell = event.target;
}
