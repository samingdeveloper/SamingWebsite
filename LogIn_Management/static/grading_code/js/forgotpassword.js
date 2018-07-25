function myFunction() {
    var x = document.createElement("INPUT");
    x.setAttribute("type", "hidden");
    document.body.appendChild(x);
    document.getElementById("demo").innerHTML = "Saming has sent a backup password to email. When logging in, please change your backup password with resubmit. If you do not have an email, please press reset password button again.";
}