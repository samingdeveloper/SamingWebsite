class TempFuncCollector{

    static triggerFilter(rGlass,target){
        rGlass.addEventListener("click",function(){
            target.style.display = "block";
            //target.style.visibility = "visible";
            rGlass.removeEventListener("click", TempFuncCollector.triggerFilter(rGlass,target));
            rGlass.addEventListener("click", TempFuncCollector.unTriggerFilter(rGlass,target));
        });
    }

    static unTriggerFilter(rGlass,target){
        rGlass.addEventListener("click",function(){
            target.style.display = "none";
            //target.style.visibility = "hidden";
            rGlass.removeEventListener("click", TempFuncCollector.unTriggerFilter(rGlass,target));
            rGlass.addEventListener("click", TempFuncCollector.triggerFilter(rGlass,target));
        });
    }

    static filter(type){
        let input, filter, ul, li, a, i;
        target_search = type == "category" ? "category-filter":"name-filter";
        target_elements = ["main-quiz-div", "main-exam-div", "main-exam-quiz", "main-exam-quiz-pool", "main-quiz-pool"]; //pool for teacher and ta.
        input = document.getElementById(target_search);
        filter = input.value.toUpperCase();
        ul = document.getElementById(target_element);
        li = ul.getElementsByTagName("li");
        for (i = 0; i < li.length; i++) {
            a = li[i].getElementsByTagName("my-element")[0];
            if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "block";
            } else {
                li[i].style.display = "none";
            }
        }
    }

}

document.addEventListener("DOMContentLoaded",function(event){
    let rGlass = document.getElementById("r-sidebar-glass");
    let target = document.getElementById("l-sidebar-wrapper");
    rGlass.addEventListener("click", TempFuncCollector.triggerFilter(rGlass,target));
    console.log("loaded");
});