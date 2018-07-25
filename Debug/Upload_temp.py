{% extends "NavBar.html" %}
{% block content %}
    {% load static %}
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

    <!-- start Section of codemirror -->
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="//codemirror.net/doc/docs.css">
    <link rel="stylesheet" href="//codemirror.net/lib/codemirror.css">
    <link rel="stylesheet" href="//codemirror.net/theme/blackboard.css">
    <script src="//codemirror.net/lib/codemirror.js"></script>
    <script src="//codemirror.net/mode/javascript/javascript.js"></script>
    <script src="//codemirror.net/addon/selection/active-line.js"></script>
    <script src="//codemirror.net/addon/edit/matchbrackets.js"></script>
    <!-- ENd -->
</head>

<table width="99%" border="0">
  <tr>
    <td colspan="5" align="left" valign="top">&nbsp;  </td>
  </tr>
  <tr>
    <td height="465" colspan="2" rowspan="4" valign="top">&nbsp;</td>
    <td width="18%" height="75" valign="top" class="assignment"><strong>Deadline:{{ Deadline }}<br><br>Assignment:{{ quizTitle }}</strong></td>
    <td width="41%" height="465" rowspan="3" valign="top">
        <form class="form-horizontal" role="form" action="" method="post" enctype="multipart/form-data" >
            {% csrf_token %}
            <textarea  class="codemirror-textarea"  name="code-form-comment"  id="code-form-comment" >{{code}}</textarea>
            <br>
            <input type="submit" name="code-form-submit" id="code-form-submit" value="Submit"></input>
            <p>{{display}}</p>
        </form>
    </td>
    <td width="25%" rowspan="3" valign="top" bgcolor="#000000"><p style="color:white;">{{display}}
      </p></td>
  </tr>
  <tr>
    <td height="215" valign="top" class="pro"><p><strong>Detail:{{ quizDetail }}</strong></p></td>
  </tr>
  <tr>
    <td rowspan="2" valign="top" class="pro"><p><strong class="hint">Hint:{{ Hint }}</strong></p></td>
  </tr>
  <tr>
    <td width="41%" height="109" valign="top" bgcolor="#DCDDDC">&nbsp</td>
    <td align="left" valign="middle">
        <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
      <p>
        <input type="file" name="upload" style="display:none"/>
           <input type="text"
                   name="uploadtext"
                   onkeydown="upload.value=uploadtext.value "
                   onchange="document.getElementById('uploadtext_testcase').value = this.value.split('\\').pop().split('/').pop()"

            />
            <input type="button"
                   name="uploadbutton"
                   value="Choose File"
                   onclick="upload.click()"
                   onmouseout="uploadtext.value=upload.value"
            />
         <input type="submit"  name="upload_submit" class="btn btn-warning" value="submit"/>
    </form></td>

  </tr>
</table>



<script>
      var editor = CodeMirror.fromTextArea(document.getElementById("code-form-comment"), {
    theme : "blackboard",
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
  CodeMirror.on(window, "hashchange", function() {
    var theme = location.hash.slice(1);
    if (theme) { input.value = theme; selectTheme(); }
  });
</script>


{% endblock content %}