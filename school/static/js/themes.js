// 1- on every page check the applied theme
// 2- get applied theme and apply it
// 3- on every theme change localStorage value , so all pages can be the same

const navbar = document.querySelector('.navbar'); //navbar
const optimal = document.getElementById('optimal');
optimal.addEventListener('click',optimalTheme);

function checkTheme(){
    const theme = localStorage.getItem('theme');

    if (theme == 'optimal'){
        optimalTheme();
    }

}
checkTheme();

function optimalTheme(){
    localStorage.setItem('theme','optimal')

}