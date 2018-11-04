/*** Copyright 2013 Teun Duynstee Licensed under the Apache License, Version 2.0 ***/
!function(n,t){"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?module.exports=t():n.firstBy=t()}(this,function(){var n=function(){function n(n){return n}function t(n){return"string"==typeof n?n.toLowerCase():n}function r(r,e){if(e="number"==typeof e?{direction:e}:e||{},"function"!=typeof r){var i=r;r=function(n){return n[i]?n[i]:""}}if(1===r.length){var o=r,f=e.ignoreCase?t:n,u=e.cmp||function(n,t){return n<t?-1:n>t?1:0};r=function(n,t){return u(f(o(n)),f(o(t)))}}return e.direction===-1?function(n,t){return-r(n,t)}:r}function e(n,t){var i="function"==typeof this&&!this.firstBy&&this,o=r(n,t),f=i?function(n,t){return i(n,t)||o(n,t)}:o;return f.thenBy=e,f}return e.firstBy=e,e}();return n});


class FuncCollector{

    static idStartsWith(node,target){
        return node.startsWith(target);
    }
    static sortDiv(columnMiddle,target){
        let sortedArray=[];
        for(let i=0; i < columnMiddle.length; i++){
            if (columnMiddle[i].nodeName === "DIV" &&
                    FuncCollector.idStartsWith(columnMiddle[i].id,"main")){
                    //console.log(...columnMiddle);
                    //console.log(columnMiddle[i].id+'\n'+target);
                if (columnMiddle[i].id === target) {
                    //console.log("here1");
                    target = columnMiddle[i]; console.log(`${target.id}`);
                    try{
                        for(let j=0; j < target.childNodes.length; j++){
                            console.log(j);
                            console.log(target.childNodes.length);
                            if (target.childNodes[j].nodeName === "DIV"){

                                console.log(columnMiddle[i].childNodes[j]);
                                //console.log(columnMiddle[i].childNodes[j].dataset.active);
                                try {
                                    console.log(target.childNodes[j]);
                                    sortedArray.push(target.childNodes[j])
                                } catch(error){
                                    console.log(error);
                                }
                            }
                        }
                    } catch(error){
                        console.log(error);
                    }
                }
            }
        }
        //console.log(target+target.id+`${typeof target}`);
        console.log(sortedArray);
        if (target.id=="main-quiz-div"){
            try{
                sortedArray.sort(firstBy(function(node1,node2)
                    { return node2.dataset.active - node1.dataset.active; }
                ).thenBy(function(node1,node2){
                    { return node1.dataset.category.localeCompare(node2.dataset.category); }
                }).thenBy(function(node1,node2){
                    { return node1.dataset.name.localeCompare(node2.dataset.name); }
                }));
            } catch(error){
                console.log(error);
            }
        } else if (target.id=="main-exam-div"){
            try{
                sortedArray.sort(firstBy(function(node1,node2)
                    { return node2.dataset.active - node1.dataset.active; }
                ).thenBy(function(node1,node2){
                    { return node1.dataset.name.localeCompare(node2.dataset.name); }
                }));
            } catch(error){
                console.log(error);
            }
        } else {
            try{
                //console.log("here");
                sortedArray.sort(firstBy(function(node1,node2){
                    { return node1.dataset.category.localeCompare(node2.dataset.category); }
                }).thenBy(function(node1,node2){
                    { return node1.dataset.name.localeCompare(node2.dataset.name); }
                }));
            } catch(error){
                console.log(error);
            }
        }
        //console.log(sortedArray);
        //target.innerHTML = '';
        //console.log('empty: ' +target.id+ ` ${typeof target}`);
        console.log(sortedArray);
        for(let i in sortedArray){
            console.log(sortedArray+'\n'+`${typeof sortedArray}`+'\n'+sortedArray[i]);
            target.appendChild(sortedArray[i]);
            //console.log('appended: '+sortedArray[i].id);
        }
        //target.replaceWith(...sortedArray);
    }
}

document.addEventListener("DOMContentLoaded",function(event){
    let columnMiddle = document.getElementById("column-middle").childNodes;
    let targetDiv = ["quiz-div","exam-div","exam-quiz","exam-quiz-pool","quiz-pool"];
    let prefixes = {"main":"main"}
    for (var target in targetDiv){
        FuncCollector.sortDiv(columnMiddle, prefixes.main+'-'+targetDiv[target]);
    }
    //FuncCollector.sortDiv(columnMiddle, prefixes.main+'-'+"quiz-pool");
});