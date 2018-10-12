const toggleClass = (el, cls) => {
  el.classList.toggle(cls);
}
let buttons = document.querySelectorAll('button[role="collapse"]');
for (let b of buttons) {
  b.addEventListener('click', ev => {
    group = document.getElementById(b.getAttribute('data-group'));
    toggleClass(group, 'visible--false');
    toggleClass(b, 'chevron--right');
    toggleClass(b, 'chevron--bottom');
  })
}