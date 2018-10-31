// button1

document.addEventListener("DOMContentLoaded", function(event){
    let tooltip = document.getElementById("hiddentooltip");
    tooltip.style.transition = "opacity 1s";
    const FADE_IN = (() => {
        tooltip.style.visibility = "visible";
        tooltip.style.opacity = 1;
    });

    const FADE_OUT = (() => {
        tooltip.style.visibility = "hidden";
        tooltip.style.opacity = 0;
    });
    document.getElementById("qt").addEventListener("mouseover",FADE_IN);
    document.getElementById("qt").addEventListener("mouseout",FADE_OUT);
    document.getElementById("hiddentooltip").addEventListener("mouseover",FADE_IN,true);
    document.getElementById("hiddentooltip").addEventListener("mouseout",FADE_OUT);
});