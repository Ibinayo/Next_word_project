const menu = document.querySelector('#menu');
const navMenu = document.querySelector('#nav_menu');
const nav = document.querySelector('#nav_ops ul');
const drop = document.querySelector('#drop');
const clear = document.querySelector('#clear');
const input = document.querySelector('#input');
const select = document.querySelector('#select');
const aboutDiv = document.querySelectorAll('#content_about div');
const about = document.querySelector('#content_about');
const text = document.querySelector('#text_box textarea');
const opts = document.querySelector('#opts');

// Path: app/static/js/home.js

if (menu !== null) {
  menu.addEventListener('mouseenter', () => {
    drop.style.display = 'flex';
  });
  menu.addEventListener('mouseleave', () => {
    drop.style.display = 'none';
  });
  menu.addEventListener('click', () => {
    if (drop.style.display === 'flex') {
      drop.style.display = 'none';
    } else {
      drop.style.display = 'flex';
    }
  });

  drop.addEventListener('mouseenter', () => {
    drop.style.display = 'flex';
  });
  drop.addEventListener('mouseleave', () => {
    drop.style.display = 'none';
  });

  clear.addEventListener('click', () => {
    const sentence = input.value;
    const url = 'http://127.0.0.1:5000/input';
    const data = JSON.stringify({ input: sentence });
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: data
    })
      .then(response => response.json())
      .then(data => { console.log('done'); });
    input.value = '';
    const opt = document.querySelectorAll('#opt');
    if (opt.length !== 0) {
      opt.forEach((element) => {
        element.remove();
      });
    }
  });
}

if (select !== null) {
  select.addEventListener('change', () => {
    const option = select.value;
    const currentURL = window.location.href;
    const url = new URL(currentURL);
    url.searchParams.set('act', option);
    const newURL = url.toString();
    window.location.href = newURL;
  });
}

function wait (ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function animate () {
  if (about !== null) {
    for (let i = 0; i < aboutDiv.length; i++) {
      aboutDiv[i].style.display = 'flex';
      aboutDiv[i].style.animation = 'slideInFromLeft 0.25s linear 1';
      await wait(1000);
    }
  }
}

animate();

if (navMenu !== null && navMenu.style.display !== 'none') {
  navMenu.addEventListener('click', () => {
    nav.style.display = 'flex';
    nav.addEventListener('mouseenter', () => {
      nav.style.display = 'flex';
    });
    nav.addEventListener('mouseleave', () => {
      if (navMenu.style.display !== 'none') {
        nav.style.display = 'none';
      }
    });
  });
}

window.addEventListener('resize', () => {
  if (window.innerWidth > 768) {
    nav.style.display = 'flex';
    nav.addEventListener('mouseenter', () => {
      nav.style.display = 'flex';
    });
    nav.addEventListener('mouseleave', () => {
      nav.style.display = 'flex';
    });
  } else {
    nav.style.display = 'none';
  }
});

let i;
let j = 0;

function removeOptions () {
  const opt = document.querySelectorAll('#opt');
  if (opt.length !== 0) {
    opt.forEach((element) => {
      element.remove();
    });
  }
}

function addOptions (extra) {
  let opt = document.querySelectorAll('#opt');
  if (opt.length < 5) {
    opt = document.createElement('div');
    opt.id = 'opt';
    opt.innerHTML = extra;
    opts.appendChild(opt);
  }
}

async function loadOptions (value, num, url) {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Specify that you are sending JSON
      Accept: 'application/json'
    },
    body: JSON.stringify({ inputs: value, num: num })
  });
  const data = await res.json();
  return data.reverse();
}

async function predictWord (value) {
  removeOptions();
  const url = 'http://127.0.0.1:5000/predict';
  const options = await loadOptions(value, 5, url);
  options.forEach((element) => {
    addOptions(element);
  });
}

async function compareletter (data, value) {
  removeOptions();
  let fullWord = false;
  let optionList = [];
  const input = value.trim();
  if (input !== ' ' && input !== '') {
    for (const key of data) {
      const vals = key.split(' ');
      vals.forEach((element) => {
        const word = element.slice(0, input.length);
        let extra = '';
        if (word.toLowerCase() === input.toLowerCase()) {
          if (element.toLowerCase() === input.toLowerCase()) {
            fullWord = true;
            extra = compareWord(vals, element);
          }
          if (optionList.includes(extra) === false && optionList.length < 5) {
            if (extra !== '') {
              optionList.push(extra);
            }
          }
        }
      });
    }
    if (optionList.length < 5) {
      if (fullWord === false && optionList.length === 0) {
        value = input;
      }
      const url = 'http://127.0.0.1:5000/predict';
      const data = await loadOptions(value, 5, url);
      data.forEach((element) => {
        if (optionList.includes(element) === false && optionList.length < 5) {
          optionList.push(element);
        }
      });
    } else {
      optionList = optionList.slice(0, 5);
    }
    optionList.forEach((element) => {
      addOptions(element);
    });
  }
}

function compareWord (data, value) {
  if (data.indexOf(value) !== data.length - 1) {
    const newIndex = data.indexOf(value) + 1;
    const datum = data[newIndex];
    return datum;
  }
  return '';
}

if (text !== null) {
  text.addEventListener('input', () => {
    if (text.value === '') {
      removeOptions();
    }
  });
}

if (text !== null) {
  text.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
      const url = 'http://127.0.0.1:5000/input';
      removeOptions();
      fetch(url)
        .then(response => response.json())
        .then(data => {
          let input = text.value.trim();
          const val = text.value.trim().split(' ');
          const word = val[val.length - 1];
          if (input === '') {
            removeOptions();
          } else if (data.length === 0) {
            if (text.value.endsWith(' ') && input !== '') {
              predictWord(word);
            }
          } else {
            if (val.length > 1 && val[val.length - 1] !== '') {
              input = val[val.length - 1];
            }
            if (input !== '') {
              compareletter(data, input);
            } else {
              removeOptions();
            }
          }
        });
    }
  });
}

function colorOptions (options, index, color, background) {
  options[index - 1].style.color = color;
  options[index - 1].style.backgroundColor = background;
}

if (text !== null) {
  text.addEventListener('keydown', (e) => {
    const options = document.querySelectorAll('#opt');
    if (options.length !== 0) {
      i = 5;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (j === i) {
          colorOptions(options, j, 'rgba(255, 255, 255, 0.4)', '#594e5c');
          j = 0;
        }
        if (j > 0) {
          console.log(`${j - 1} -> prev`);
          colorOptions(options, j, 'rgba(255, 255, 255, 0.4)', '#594e5c');
        }
        colorOptions(options, j + 1, 'white', '#3e2e2e');
        j++;
      }
      if (e.key === 'ArrowUp') {
        j -= 1;
        e.preventDefault();
        if (j === i) {
          j = 1;
        }
        if (j === 0) {
          colorOptions(options, 1, 'rgba(255, 255, 255, 0.4)', '#594e5c');
          j = i;
        }
        if (j < i) {
          colorOptions(options, j + 1, 'rgba(255, 255, 255, 0.4)', '#594e5c');
        }
        colorOptions(options, j, 'white', '#3e2e2e');
      }

      if (e.code === 'Enter') {
        e.preventDefault();
        if (text.value.endsWith(' ')) {
          text.value = text.value + options[j - 1].innerHTML;
          removeOptions();
        } else {
          const vals = text.value.trim().split(' ');
          const val = vals[vals.length - 1];
          text.value = text.value.slice(0, text.value.length - val.length) + options[j - 1].innerHTML;
        }
        j = 0;
      }
      if (e.key === 'Backspace') {
        removeOptions();
        j = 0;
        if (text.value.endsWith(' ') === true) {
          options.forEach((element) => {
            addOptions(element.innerHTML);
          });
        }
      }
      if (e.key === '.' || e.key === ',') {
        removeOptions();
      }
    }
  });
}
