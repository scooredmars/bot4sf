window.onscroll = function () { scrollFunction() };

function scrollFunction() {
    var height = screen.height;
    if (height < 1000) {
        if (document.body.scrollTop > 793 || document.documentElement.scrollTop > 793) {
            document.getElementById("navbar").style.top = "0";
        } else {
            document.getElementById("navbar").style.top = "-150px";
        }
    }

    if (height > 1000) {
        if (document.body.scrollTop > 930 || document.documentElement.scrollTop > 930) {
            document.getElementById("navbar").style.top = "0";
        } else {
            document.getElementById("navbar").style.top = "-150px";
        }
    }
}
