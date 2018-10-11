/** Email mask generator */
class EmailMask {
  /**
   * @constructor
   * @param {string} fieldId - ID or name of input field to attach to
   * @param {Object} opts - Options object to pass to class.
   * Rest of the options defined below:
   * @param {string} wrapperAttr - HTML attr on which to select the wrapping
   * element with
   * @default['for']
   * @param {string} wrapperDataAttr - HTML on which to store the non-intrusive
   * placeholder data.
   * @default['data-placeholder']
   * @param {string} fieldAttr - HTML attr on which to select the wrapping
   * element with
   * @default['name']
   * @param {boolean} intrusive - Determines whether the mask will be actual
   * input on the input field or a pseudo-element mask guide.
   * @default[false]
   * @param {string} maskPlaceholder - placeholder character to use in non-
   * intrusive mask
   * @default['_']
   * @param {string} maskColor - Font color for the mask
   * @default['#a4a4a4']
   */
  constructor(
    fieldId,
    opts
  ) {
    this.field =  document.getElementById(fieldId)
               || document.querySelector(`input[name="${fieldId}]`);
    if (opts) {
      this.opts = {
        wrapperClass: opts.wrapperClass || this.defaults.wrapperClass,
        wrapperAttr: opts.wrapperAttr || this.defaults.wrapperAttr,
        wrapperDataAttr: opts.wrapperDataAttr || this.defaults.wrapperDataAttr,
        fieldAttr: opts.fieldAttr || this.defaults.fieldAttr,
        intrusive: opts.intrusive || this.defaults.intrusive,
        maskPlaceholder: opts.maskPlaceholder || this.defaults.maskPlaceholder,
        maskColor: opts.maskColor || this.defaults.maskColor,
        textColor: opts.textColor || this.defaults.textColor
      };
    } else {
      this.opts = this.defaults;
    }
    this.setWrapper();
    this.style = document.head.appendChild(document.createElement("style"));
    this.addKeyupHandler();
    this.addFocusHandler();
    this.addBlurHandler();
  }
  setWrapper() {
    const wc = this.opts.wrapperClass;
    const wa = this.opts.wrapperAttr;
    const fa = this.opts.fieldAttr;
    const getA = this.field.getAttribute(`${fa}`)
    this.wrapper = document.querySelector(`.${wc}[${wa}=${getA}]`)
  }
  get defaults() {
    return {
      wrapperClass: 'field-wrapper',
      wrapperAttr: 'for',
      wrapperDataAttr: 'data-placeholder',
      fieldAttr: 'name',
      intrusive: false,
      maskPlaceholder: '_',
      maskColor: '#a4a4a4',
      textColor: '#444444'
    }
  }
  get value() {
    return this.field.value;
  }
  set value(val) {
    this.field.value = val;
  }
  get user() {
    if (this.value && this.value.includes('@')) {
      return this.value.split('@')[0];
    } else if (this.value) {
      return this.value;
    }
    return ''
  }
  get mailServer() {
    const rex = new RegExp("@((?:[a-z\\d-]+)+)[\\.]?", "i");
    if (rex.test(this.value)) {
      return this.value.match(rex)[1];
    } else {
      return undefined;
    }
  }
  get tld() {
    const rex = new RegExp("@(?:[a-z\\d-]+\\.)+([a-z]{2,10})$", "i");
    if (rex.test(this.value)) {
      return this.value.match(rex)[1];
    } else {
      return undefined;
    }
  }
  get fullMask() {
    return `${this.replaceUser()}${this.replaceServer()}${this.replaceTld()}`;
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
  replaceUser(intrusive=false) {
    if (this.value === '') {
      return this.opts.maskPlaceholder;
    }
    return this.opts.maskPlaceholder.repeat(this.user.length);
  }
  replaceServer(intrusive=false) {
    if (this.mailServer !== undefined) {
      return `@${this.opts.maskPlaceholder.repeat(this.mailServer.length)}.`;
    }
    return `@${this.opts.maskPlaceholder}.`;
  }
  replaceTld(intrusive=false) {
    if (this.tld !== undefined) {
      return this.opts.maskPlaceholder.repeat(this.tld.length);
    }
    return this.opts.maskPlaceholder;
  }
  updateDataPlaceholder() {
    this.wrapper.setAttribute(this.opts.wrapperDataAttr, this.fullMask);
  }
  addKeyupHandler() {
    this.attachListener('keyup', ev => {
      this.updateDataPlaceholder()
    });
  }
  addFocusHandler() {
    this.attachListener('focus', ev => {
      const wc = this.opts.wrapperClass;
      const wa = this.opts.wrapperAttr;
      const fa = this.opts.fieldAttr;
      const mc = this.opts.maskColor;
      const getA = this.field.getAttribute(`${this.opts.fieldAttr}`);
      this.style.innerHTML = `.${wc}[${wa}="${getA}"]:before {
          color: ${mc};
        }`;
      this.style.innerHTML += `\ninput[${fa}="${getA}"]::placeholder {
        color: transparent;
      }`;
    });
  }
  addBlurHandler() {
    this.attachListener('blur', ev => {
      const fa = this.opts.fieldAttr;
      const getA = this.field.getAttribute(`${this.opts.fieldAttr}`);
      if(this.value === '' || this.value === undefined) {
        this.style.innerHTML = '';//`input[${fa}="${getA}"]::placeholder {
        //   color: ${this.opts.textColor};
        // }`;;
      }
    });
  }
}
document.addEventListener('DOMContentLoaded', function() {
  const em = new EmailMask('id_email');
});
