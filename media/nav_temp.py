<link rel="stylesheet" type="text/css" href="{% static 'grading_code/css/forgot.css' %}">
<link rel="stylesheet" type="text/css" href="{% static 'grading_code/css/style_Assignment.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'grading_code/css/createassignment.css' %}">
    <link rel="stylesheet" type="text/css" href="{% static 'grading_code/css/assignment_testcase.css' %}">
<script src="{% static 'grading_code/js/navbar_Assignment.js' %}"></script>
    <script src="{% static 'grading_code/js/pupupbtn.js' %}"></script>
    <script src="{% static 'grading_code/js/forgotpassword.js' %}"></script>
    <script src="{% static 'grading_code/js/assignment.js' %}"></script>
    <script src="{% static 'grading_code/js/animation.js' %}"></script>

form action="{% url 'Class_Management:Assign_Management:GenerateAssign' %}" method="post" enctype="multipart/form-data"
              > {% csrf_token %}

              <input type="text" id="ldeadline" name="deadline" placeholder="ex.12/12/60,23:59">

#############################################################################################################################################

<<!DOCTYPE html>
    {% load static %}
<html lang="en">
{% block content %}
<head>
    <meta charset="utf-8">
    <link rel="icon" type="png" href="{% static 'grading_code/images/logo.png' %}" />
    <title>Saming</title>

    <link rel="stylesheet" type="text/css" href="{% static 'grading_code/css/style_Assignment.css' %}">
    <script src="{% static 'grading_code/js/navbar_Assignment.js' %}"></script>


    <link href='https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700|Lato:400,100,300,700,900' rel='stylesheet'
        type='text/css'>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>
    <div class="navbar">
        <div class="logo">
            <button class="logo1" onclick="openNav()">
                <img src="{% static 'grading_code/images/Tap.png' %}" width="auto" height="30"> </button>
            <span style="margin-left: 20px;">
                <img src="{% static 'grading_code/images/saming.png' %}" width="auto" height="30"> </span>
        </div>
        <div class="dropdown">
            <button class="dropbtn">{{ request.user.first_name }} {{ request.user.last_name }}
                <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-content">
                <a href="/Change_Password">
                    <i class="fa fa-cog" style="font-size:18px; color: grey"></i> Change password</a>
                <a href="/LogOut">
                    <i class="fa fa-power-off" style="font-size:18px; color: grey"></i> Log out</a>
            </div>
        </div>
    </div>
    <!-- input assignment -->
    <div id="mySidenav" class="sidenav">
        <a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
        <a href="{% url 'Class_Management:Home' %}">Home</a>
        <a href="{% url 'Class_Management:Assign_Management:GenerateAssign' %}">CreateAssignment</a>
        {%  for i in quiz %}
            <a href={% url 'Class_Management:Assign_Management:Uploadfile' i.id %}>{{ i.quizTitle }}</a>
        {% endfor %}
    </div>
    <!-- input data in main ex. text or etc -->
<div id="main">
        <div class="row">
            <div class="column side">
                <div class="scroll">
                    <h1> {{ quizTitle }} </h1>
                    <div class="p">
                        <p>{{ quizDetail }}
                        </p>
                        <p>{{ Hint }}</p>
                    </div>
                </div>
            </div>
            <div class="column middle">
                <form>
                    <textarea> <!-- sometimes --> </textarea>
                    <!--<option>blackboard</optionselected> //// back end -->

                    <div class="textarea1">
                        Showtime
                    </div>
                    <button class="button button1">RUN</button>
                </form>
            </div>
            <div class="column side">
                <div class="result">

                </div>
                <div class="result1">

                </div>
                <!-- I don't know solotion in modified Browse file. You try it. -->

                <button type="file" id="myFile" class="button button1">UPLOAD</button>
                <button class="button button1" onclick="myFunction()">SUBMIT</button>
            </div>
        </div>

        <script>
            var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
                theme: "blackboard",
                lineNumbers: true,
                styleActiveLine: true,
                matchBrackets: true,

            });
            var input = document.getElementById("select");
            function selectTheme() {
                var theme = input.options[input.selectedIndex].textContent;
                editor.setOption("theme", theme);
                location.hash = "#" + theme;
            }
            var choice = (location.hash && location.hash.slice(1)) ||
                (document.location.search &&
                    decodeURIComponent(document.location.search.slice(1)));
            if (choice) {
                input.value = choice;
                editor.setOption("theme", choice);
            }
            CodeMirror.on(window, "hashchange", function () {
                var theme = location.hash.slice(1);
                if (theme) { input.value = theme; selectTheme(); }
            });
        </script>
</body>
</html>
{% endblock %}