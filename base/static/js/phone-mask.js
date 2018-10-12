/** Email mask generator */
class PhoneMask {
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
        mask: opts.mask || this.defaults.mask,
        maskPlaceholder: opts.maskPlaceholder || this.defaults.maskPlaceholder,
        maskColor: opts.maskColor || this.defaults.maskColor,
        textColor: opts.textColor || this.defaults.textColor
      };
    } else {
      this.opts = this.defaults;
    }
    if (this.opts.maskPlaceholder !== this.defaults.maskPlaceholder) {
      this.opts.mask = this.defaults.mask.replace(
        this.defaults.maskPlaceholder, this.opts.maskPlaceholder);
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
      mask: '(___)___-____',
      maskPlaceholder: '_',
      maskColor: '#a4a4a4',
      textColor: '#444444'
    }
  }
  get value() {
    if (this.field.value) {
      return this.field.value;
    }
    return undefined;
  }
  set value(val) {
    this.field.value = val;
  }
  get code() {
    if (this.value) {
      return this.value.slice(0,3);
    }
    return ''
  }
  get body1() {
    if (this.value.length > 3) {
      return this.value.slice(3,6);
    } 
    return undefined;
  }
  get body2() {
    if (this.value.length > 6) {
      return this.value.slice(6);
    } 
    return undefined;
  }
  get fullMask() {
    return `${this.replaceCode()}${this.replaceBody1()}${this.replaceBody2()}`;
  }
  displaceCaret() {
    const el = this.field;
    if (this.value !== undefined && this.value !== '') {
      this.field.setSelectionRange(this.value.length, this.value);
    }
    // if (this.value === undefined) {
    //   el.selectionStart = el.selectionEnd =  0;
    // } else {
    //   el.selectionStart = el.selectionEnd = this.value.length;
    // }
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
  getMaskPositions() {
    const mp = this.opts.maskPlaceholder;
    return this.mask.map((e,i) => e !== mp ? i : null).filter(e => e !== null);
  }
  replaceCode(intrusive=false) {
    if (this.value && this.value === '' || this.value === '(') {
      return `(${this.opts.maskPlaceholder}`;
    } else if (this.value)
    return this.opts.maskPlaceholder.repeat(this.code.length);
  }
  replaceBody1(intrusive=false) {
    if (this.body1 !== undefined) {
      return `${this.opts.maskPlaceholder.repeat(this.body1.length)}-`;
    }
    return `${this.opts.maskPlaceholder}-`;
  }
  replaceBody2(intrusive=false) {
    if (this.body2 !== undefined) {
      return this.opts.maskPlaceholder.repeat(this.body2.length);
    }
    return this.opts.maskPlaceholder;
  }
  updateDataPlaceholder() {
    this.wrapper.setAttribute(this.opts.wrapperDataAttr, this.fullMask);
  }
  addKeyupHandler() {
    this.attachListener('keyup', ev => {
      this.displaceCaret();
      this.updateDataPlaceholder();
    });
  }
  addClickHandler() {
    this.attachListener('click', ev => {
      const self = this;
      window.setTimeout(self.displaceCaret,1);
    });
  }
  addFocusHandler() {
    this.attachListener('focus', ev => {
      this.displaceCaret();
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
      this.displaceCaret();
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

