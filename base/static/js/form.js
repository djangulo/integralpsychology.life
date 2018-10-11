class EmailMask {
  constructor(fieldId) {
    this.field = document.getElementById(fieldId);
    this.curVal = this.field.value;
    this.div = document.querySelector('.field-wrapper[for="email"]')
    this.style = document.head.appendChild(document.createElement("style"));
  }
  prepend(str, char) {
    return char + str;
  }
  append(str, char) {
    return str + char;
  }
  insert(str, char, pos) {
    let pre = str.slice(0, pos);
    let post = str.slice(pos);
    return pre + char + post;
  }
  delChar(str, pos) {
    let pre = str.slice(0, pos-1);
    let post = str.slice(pos);
    return pre + post;
  }
  get value() {
    this.field.value;
  }
  get user() {
    if (this.curVal.includes('@')) {
      return this.curVal.split('@')[0];
    } else {
      return this.curVal;
    }
  }
  get mailServer() {
    const rex = new RegExp("@((?:[a-z\\d-]+)+)[\\.]?", "i");
    if (rex.test(this.curVal)) {
      return this.curVal.match(rex)[1];
    } else {
      return undefined;
    }
  }
  get tdl() {
    const rex = new RegExp("^([a-z\\d._%-]+)@((?:[a-z\\d-]+\\.)+)([a-z]{2,6})$", "i");
    if (this.curVal.split('').includes('@')) {
      return this.curVal.match(rex)[3];
    } else {
      return undefined;
    }
  }
  attachListener(event, fn, el=null) {
    if (el === null) {
      this.field.addEventListener(event, fn);
    } else {
      el.addEventListener(event, fn);
    }
  }
  detachListener(event, fn, el=null) {
    if (el === null) {
      this.field.removeEventListener(event);
    } else {
      el.removeEventListener(event);
    }
  }
  updateVal(val) {
    this.curVal = val;
  }
  replaceUserName() {
    if (this.curVal === '') {
      return '_';
    }
    const str = '_'.repeat(this.user.length);
    const dataDescr = this.div.getAttribute('data-descr');
    return str;
  }
  replaceMailSever() {
    // const rex = new RegExp("@((?:[_]+)+)\\.", "i");
    // let dataDescr = this.div.getAttribute('data-descr');
    if (this.mailServer !== undefined) {
      const str = '_'.repeat(this.mailServer.length);
      // dataDescr = dataDescr.replace(dataDescr.match(rex)[0], '@'+str+'.')
      return '@' + str + '.';
      // return dataDescr.replace(this.mailServer, str);
    }
    return '@_.';
  }
  updateDataDescr() {
    this.div.setAttribute('data-descr', this.replaceUserName() + this.replaceMailSever());
  }
}
(document.addEventListener('DOMContentLoaded', function() {
  // const phoneDiv = document.querySelector('.field-wrapper[for="phone"]')
  // const phoneInput = document.getElementById('id_phone');
  // const phoneStyle = document.head.appendChild(document.createElement("style"));
  const em = new EmailMask('id_email');
  em.attachListener('keyup', (ev) => {
    em.updateVal(em.field.value);
    // em.replaceUserName();
    em.updateDataDescr();
    // console.log(em.mailServer);
  });
  em.attachListener('focus', function() {
    em.style.innerHTML = ".field-wrapper[for='email']:before {color: #a4a4a4;}";
    em.style.innerHTML += "input[type='email']::placeholder {color: transparent;}";
  });
  em.attachListener('blur', function() {
    if(em.curVal === '') {
      em.style.innerHTML = '';
    }
  });
}))();

// emailInput.onkeyup = function(ev) {
//   const key = ev.key;
//   const val = getValue(this).value;
//   const len = getValue(this).length;
//   const s = val.split('');
//   let dataDescr = emailDiv.getAttribute('data-descr');
//   if (len > 1 && !(s.includes('@'))) {
//     dataDescr = prepend(dataDescr, '_');
//     emailDiv.setAttribute('data-descr', dataDescr);
//   } else if (
//       s.includes('@') &&
//       s.slice(s.indexOf('@')+1).length >=0
//     ) {
//     console.log(s.slice(s.indexOf('@')+1));
//     dataDescr = insert(dataDescr, '_', s.indexOf('@')+1);
//     emailDiv.setAttribute('data-descr', dataDescr);
//   }
// }