function check() {
    var checkBox = document.getElementById("checbox");
    var text1 = document.getElementsByClassName("currency");
    var text2 = document.getElementsByClassName("plan-shop");
    var footer = document.getElementsByClassName("user-footer");

    for (var i = 0; i < text1.length; i++) {
        if (checkBox.checked == true) {
            text1[i].style.display = "flex";
            text2[i].style.display = "none";
            footer[i].style.position = "relative";
        }
        else if (checkBox.checked == false) {
            text1[i].style.display = "none";
            text2[i].style.display = "block";
            footer[i].style.position = "fixed";
        }
    }
    }
check();