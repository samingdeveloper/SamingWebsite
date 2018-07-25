    function openCity(evt, cityName) {
      var a, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tabcontent");
      for (a = 0; a < tabcontent.length; a++) {
        tabcontent[a].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tablinks");
      for (a = 0; a < tablinks.length; a++) {
        tablinks[a].className = tablinks[a].className.replace(" active", "");
      }
      document.getElementById(cityName).style.display = "block";
      evt.currentTarget.className += " active";
    }
