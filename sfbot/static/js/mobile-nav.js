function burger() {
    var burger = document.getElementById('burger');
    var links = document.getElementById('links');
    var quit = document.getElementById('quit');
    burger.style.padding = '16px 31px 200vw 200vw';
    links.style.display = 'flex';
    quit.style.display = 'inline';
}

function quit() {
    var burger = document.getElementById('burger');
    var links = document.getElementById('links');
    var quit = document.getElementById('quit');
    burger.style.padding = '16px 31px 36px 20px';
    links.style.display = 'none';
    quit.style.display = 'none';
}