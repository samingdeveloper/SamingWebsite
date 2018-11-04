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
        let input, filter, ul, li, a, i, j, k;
        //let target_search = type == "category" ? "category-filter":"name-filter";
        let target_elements = ["main-quiz-div", "main-exam-div", "main-exam-quiz", "main-exam-quiz-pool", "main-quiz-pool"]; //pool for teacher and ta.
        //input = document.getElementById(target_search);
        //filter = input.value.toUpperCase();
        for (j in target_elements){
            ul = document.getElementById(target_elements[j]);
            //console.log(document.getElementById("column-middle").childNodes);
            //console.log(target_elements[j]);
            //console.log(ul);
            try {
                li = ul.getElementsByTagName("DIV");
                console.log(typeof li);
                for (i = 0; i < li.length; i++) {
                    if (li[i].dataset.name){
                        console.log(li[i]);
                        a = li[i];//.getElementsByTagName("my-element")[0];
                        //console.log(a.value);

                        k = document.getElementById("category-filter").value === ''
                        ? true && a.dataset.name.toUpperCase().indexOf(document.getElementById("name-filter").value.toUpperCase()) > -1
                            : a.dataset.category.toUpperCase() === document.getElementById("category-filter").value.toUpperCase() &&
                                a.dataset.name.toUpperCase().indexOf(document.getElementById("name-filter").value.toUpperCase()) > -1;
                        if (k) {
                            a.style.display = "block";
                        } else {
                            a.style.display = "none";
                        }
                        console.log(a.style.display);
                     }
                }
            } catch(error){
                console.log(error+'\n'+target_elements[j]);
            }
        }
    }

    static filterGroup(type){
        let targetDisplay, target;
        target = ["main-quiz-div", "main-exam-div", "main-exam-quiz-pool", "main-quiz-pool"];
        for(let i in target){
            console.log(target[i]);
            targetDisplay = document.getElementById(target[i]);
            if (type === target[i]) { targetDisplay.style.display = "block"; console.log(targetDisplay.style.display);}
            else { targetDisplay.style.display = "none"; console.log(targetDisplay.style.display); }
        }
    }

}

document.addEventListener("DOMContentLoaded",function(event){
    let rGlass = document.getElementById("r-sidebar-glass");
    let target = document.getElementById("l-sidebar-wrapper");
    let target2 = {
                        "icon": {"show-quiz-icon":"main-quiz-div",
                                    "show-exam":"main-exam-div",
                                    "show-exam-quiz-pool":"main-exam-quiz-pool",
                                    "show-quiz-pool":"main-quiz-pool"
                                },
                  };
    rGlass.addEventListener("click", TempFuncCollector.triggerFilter(rGlass,target));
    for(let i in target2["icon"]){
        console.log(i);
        console.log(target2["icon"][i]);
        document.getElementById(i).addEventListener("click", function(){ TempFuncCollector.filterGroup(target2["icon"][i]) });
    }
    console.log("loaded");
});