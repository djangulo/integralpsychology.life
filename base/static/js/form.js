const emailInput = document.getElementById('id_email');
const emailDiv = document.querySelector('.field-wrapper[for="email"]')
const phoneDiv = document.querySelector('.field-wrapper[for="phone"]')
const phoneInput = document.getElementById('id_phone');
console.log(emailInput);
const emailStyle = document.head.appendChild(document.createElement("style"));
const phoneStyle = document.head.appendChild(document.createElement("style"));

emailInput.onfocus = function() {
  emailStyle.innerHTML = ".field-wrapper[for='email']:before {color: #a4a4a4;}";
  emailStyle.innerHTML += "input[type='email']::placeholder {color: transparent;}"
}
emailInput.onblur = function() {
  if(getValue(emailInput).value === '') {
    emailStyle.innerHTML = '';
  }
}

phoneInput.onfocus = function() {
  phoneStyle.innerHTML = ".field-wrapper[for='phone']:before {color: #a4a4a4;}";
  phoneStyle.innerHTML += "input[type='tel']::placeholder {color: transparent;}"
}
phoneInput.onblur = function() {
  phoneStyle.innerHTML = '';  
}
const getValue = (field) => {
  return {
    value: field.value,
    length: field.value.length
  }
}
const prepend = (str, char) => {
  return char + str;
}
const append = (str, char) => {
  return str + char;
}
const insert = (str, char, pos) => {
  let pre = str.split('').slice(0, pos).join('');
  let post = str.split('').slice(pos).join('');
  return pre + char + post;
}
const delChar = (str, pos) => {
  let pre = str.split('').slice(0, pos-1).join('');
  let post = str.split('').slice(pos).join('');
  return pre + post;
}
/**
 * Returns a string of char of the length of the
 * str1 passed
 * @param {*} str1 
 * @param {*} char 
 */
const ensureLength = (str1, char) => {
  return char.repeat(str1.split('').length);
}

emailInput.onkeyup = function(ev) {
  const key = ev.key;
  const val = getValue(this).value;
  const len = getValue(this).length;
  const s = val.split('');
  let dataDescr = emailDiv.getAttribute('data-descr');
  if (len > 1 && !(s.includes('@'))) {
    dataDescr = prepend(dataDescr, '_');
    emailDiv.setAttribute('data-descr', dataDescr);
  } else if (
      s.includes('@') &&
      s.slice(s.indexOf('@')+1).length >=0
    ) {
    console.log(s.slice(s.indexOf('@')+1));
    dataDescr = insert(dataDescr, '_', s.indexOf('@')+1);
    emailDiv.setAttribute('data-descr', dataDescr);
  }
}