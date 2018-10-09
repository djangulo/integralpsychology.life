var languages = document.getElementById('languages');

for (var i = 0; i < languages.options.length; i++) {
    languages.options[i].addEventListener('click', function(event) {
        event.preventDefault();
        console.log(event.target.innerHTML);
    }, true)
}
