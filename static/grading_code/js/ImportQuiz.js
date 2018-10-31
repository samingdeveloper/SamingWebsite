class AssignTags extends HTMLElement{
    constructor(){
        super();
        /*const template = document
            .getElementById('element-details-template')
            .content;
        const shadowRoot = this.attachShadow({mode: 'open'})
            .appendChild(template.cloneNode(true));*/
    }
}


class FuncCollector{

    static select(){
        //this.setAttribute('name', 'myselected');
        document.getElementById("selectedList").appendChild(this.cloneNode(true)).addEventListener("dblclick", FuncCollector.deSelect);
        this.remove();
        //let node = document.createElement("li"); // Create a <li> node
        /*let node2 = document.createElement("grader-assignment"); // Create a <grader-assignment> node
        let textnode = document.createTextNode(this.innerText || this.textContent);*/ // Get inner text or inner content
        /*node.appendChild(document.createElement("grader-assignment"))
            .appendChild(document.createTextNode(this.innerText || this.textContent));
        document.getElementById("selectedList").appendChild(node).addEventListener("dblclick", FuncCollector.deSelect); this.remove();*/
        FuncCollector.sortUnorderedList("selectedList");

        //console.log("double clicked!");
    }

    static deSelect(){
        //this.setAttribute('name', 'available');
        document.getElementById("availableList").appendChild(this.cloneNode(true)).addEventListener("dblclick", FuncCollector.select);
        this.remove();
        //let node = document.createElement("li"); // Create a <li> node
        /*let node2 = document.createElement("grader-assignment");
        let textnode = document.createTextNode(this.innerText || this.textContent);*/
        /*node.appendChild(document.createElement("grader-assignment"))
            .appendChild(document.createTextNode(this.innerText || this.textContent));
        document.getElementById("availableList").appendChild(node).addEventListener("dblclick", FuncCollector.select); this.remove();*/
        //FuncCollector.sortList(document.getElementById("selectedList"));
        FuncCollector.sortUnorderedList("availableList");
        //console.log("double clicked!");
    }

    static sortUnorderedList(ul, sortDescending) {
          if(typeof ul == "string")
            ul = document.getElementById(ul);

          /*// Idiot-proof, remove if you want
          if(!ul) {
            alert("The UL object is null!");
            return;
          }*/

          // Get the list items and setup an array for sorting
          var lis = ul.getElementsByTagName("LI");
          var vals = [];

          // Populate the array
          for(var i = 0, l = lis.length; i < l; i++)
            vals.push(lis[i].innerHTML);

          // Sort it
          vals.sort();

          // Sometimes you gotta DESC
          if(sortDescending)
            vals.reverse();

          // Change the list on the page
          for(var i = 0, l = lis.length; i < l; i++)
            lis[i].innerHTML = vals[i];
    }
}


/*function trigger(position) {
    let input, filter, ul, li, a, i;
    target_search = position == "left" ? "availableSearch":"selectedSearch";
    target_element = position == "left" ? "availableList":"selectedList";
    input = document.getElementById(target_search);
    filter = input.value.toUpperCase();
    ul = document.getElementById(target_element);
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("grader-assignment")[0];
        if (a.innerText.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "block";
        } else {
            li[i].style.display = "none";
        }
    }
}

function searchCategory(position){
    let input, filter, ul, li, a, i;
    target_search = position == "left" ? "availableCategorySearch":"selectedCategorySearch";
    target_element = position == "left" ? "availableList":"selectedList";
    input = document.getElementById(target_search);
    filter = input.value.toUpperCase();
    ul = document.getElementById(target_element);
    li = ul.getElementsByTagName("li");
    console.log(filter);
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("grader-assignment")[0];
        console.log(a.getAttribute("data-category"));
        if (a.getAttribute("data-category").toUpperCase() == filter) {//.indexOf(filter) > -1) {
            li[i].style.display = "block";
        } else if (filter == ''){
            for (i = 0; i < li.length; i++){
                li[i].style.display = "block";
            }
        } else {
            li[i].style.display = "none";
        }
    }
}*/

function filter(position){
    let input_search, input_category, filter_search, filter_category, ul, li, graderAssignment, i;
    let target_search_category = position == "left" ? "availableCategorySearch":"selectedCategorySearch";
    let target_search_name = position == "left" ? "availableSearch":"selectedSearch";
    let target_element = position == "left" ? "availableList":"selectedList";
    input_category = document.getElementById(target_search_category);
    input_search = document.getElementById(target_search_name);
    filter_category = input_category.value.toUpperCase();
    filter_search = input_search.value.toUpperCase();
    ul = document.getElementById(target_element);
    li = ul.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        graderAssignment = li[i].getElementsByTagName("grader-assignment")[0];
        if (filter_category == ""){
            if (graderAssignment.innerText.toUpperCase().indexOf(filter_search) > -1){ //.indexOf(filter) > -1) {
                li[i].style.display = "block";
            } else{
                li[i].style.display = "none";
            }
        } else if (graderAssignment.getAttribute("data-category").toUpperCase() == filter_category &&
            graderAssignment.innerText.toUpperCase().indexOf(filter_search) > -1) {//.indexOf(filter) > -1) {
            li[i].style.display = "block";
        } else {
            li[i].style.display = "none";
        }
    }
}

function sendPost(){
    if(document.selected.onsubmit && !document.selected.onsubmit()){
        return;
    } document.selected.submit();
};

document.addEventListener("DOMContentLoaded", function(event) {
    window.customElements.define('grader-assignment', AssignTags);
    var lis = document.getElementById("availableList").childNodes;
    var mx = document.getElementById("selectedList").childNodes;

    for (let li = 0; li < lis.length; li++){
        if (lis[li].nodeName === "LI"){
            lis[li].addEventListener("dblclick", FuncCollector.select);
            console.log(lis[li]);
        }
    };
    for (let i = 0; i < mx.length; i++){
        if (mx[i].nodeName === "LI"){
            mx[i].addEventListener("dblclick", FuncCollector.deSelect);
            console.log(mx[i]);
        }
    }
});


/*function sendPost(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", {% url 'Class_Management:Assign_Management:ImportAssign' %}, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: document.getElementById("selectedList").innerText
    }));
}*/


