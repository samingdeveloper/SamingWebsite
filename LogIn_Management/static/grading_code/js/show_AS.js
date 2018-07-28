function openCity(evt1, cityName1) {
    var a, tabcontent1, tablinks1;
    tabcontent1 = document.getElementsByClassName("tabcontent1");
    for (a = 0; a < tabcontent1.length; a++) {
        tabcontent1[a].style.display = "none";
    }
    tablinks1 = document.getElementsByClassName("tablinks1");
    for (a = 0; a < tablinks.length; a++) {
        tablinks1[a].className = tablinks1[a].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}
// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();
