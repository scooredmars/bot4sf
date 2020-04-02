window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    if (document.body.scrollTop > 930 || document.documentElement.scrollTop > 930) {
        document.getElementById("navbar").style.top = "0";
    } else {
        document.getElementById("navbar").style.top = "-150px";
    }
}
