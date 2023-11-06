const menu = document.querySelector('#menu')
const nav_menu = document.querySelector('#nav_menu')
const nav = document.querySelector('#nav_ops ul')
const drop = document.querySelector('#drop')
const clear = document.querySelector('#clear')
const input = document.querySelector('#input')
const select = document.querySelector('#select')
const message = document.querySelector('.message')
const about_div = document.querySelectorAll('#content_about div')
const about = document.querySelector('#content_about')
const text = document.querySelector('#text_box textarea')
const opts = document.querySelector('#opts')

// Path: app/static/js/home.js

if (menu !== null) {
    menu.addEventListener('mouseenter', () => {
        drop.style.display = 'flex'
    })
    menu.addEventListener('mouseleave', () => {
        drop.style.display = 'none'
    })
    menu.addEventListener('click', () => {
        if (drop.style.display === 'flex') {
            drop.style.display = 'none'
        } else { 
            drop.style.display = 'flex'
        }
    })

    drop.addEventListener('mouseenter', () => {
        drop.style.display = 'flex'
    })
    drop.addEventListener('mouseleave', () => {
        drop.style.display = 'none'
    })

    clear.addEventListener('click', ()=>{
        input.value = '';
        let opt = document.querySelectorAll('#opt')
        if (opt.length !== 0){
            opt.forEach((element) => {
                element.remove()
            })
        }
    })
}

if (select !== null) {
    select.addEventListener('change', () => {
        const option = select.value;
        const currentURL = window.location.href;
        const url= new URL(currentURL)
        url.searchParams.set('act', option)
        const newURL = url.toString()
        window.location.href = newURL
    })
}



function wait(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function animate(){
    if (about !== null){
        for (i=0; i<about_div.length; i++){
            about_div[i].style.display = 'flex'
            about_div[i].style.animation = 'slideInFromLeft 0.25s linear 1'
            await wait(1000)
        } 
    }
}

animate()



if (nav_menu !== null && nav_menu.style.display !== 'none'){
    nav_menu.addEventListener('click', () => {
        nav.style.display = 'flex'
        nav.addEventListener('mouseenter', () => {
            nav.style.display = 'flex'
        })
        nav.addEventListener('mouseleave', () => {
            if (nav_menu.style.display !== 'none'){
                nav.style.display = 'none'
            }
        })
    }) 
}

window.addEventListener('resize', () => { 
    if(window.innerWidth > 768){
        nav.style.display = 'flex'
        nav.addEventListener('mouseenter', () => {
            nav.style.display = 'flex'
        })
        nav.addEventListener('mouseleave', () => {
                nav.style.display = 'flex'
        })
    }
    else{
        nav.style.display = 'none'
    }    
 }) 

let i;
let j = 0

if (text !== null){
    text.addEventListener('input', () => {
        if (text.value !== ''){
            let opt = document.querySelectorAll('#opt')
            // if (opt.length !== 0){
            //     opt.forEach((element) => {
            //         element.remove()
            //     })
            // }
            if (opt.length === 5){
                opt[0].remove()
            }
            if (text.value !== ' ' && text.value !== ''){
                opt = document.createElement('div')
                opt.id = 'opt'
                opt.innerHTML = text.value
                opts.appendChild(opt)
            }
        }
        else{
            let opt = document.querySelectorAll('#opt')
                opt.forEach((element) => {
                    element.remove()
                })
            // document.querySelector('#opt').remove()
        }
    })
    text.addEventListener('keydown', (e) => {
        let options = document.querySelectorAll('#opt')
        if (options.length !== 0){
            i = options.length
            if (e.key === 'ArrowDown'){
                e.preventDefault()
                if (j === i){
                    options[j-1].style.color = 'rgba(255, 255, 255, 0.4)'
                    options[j-1].style.backgroundColor = '#594e5c'
                    j = 0
                    console.log(i)
                }
                console.log(j)
                if (j > 0){
                    options[j-1].style.color = 'rgba(255, 255, 255, 0.4)'
                    options[j-1].style.backgroundColor = '#594e5c'
                }
                options[j].style.color = 'white'
                options[j].style.backgroundColor = '#3e2e2e'
                j++
            }
            if (e.key === 'ArrowUp'){
                e.preventDefault()
                if (j === i){
                    j -= 1
                }
                if (j === 0){
                    options[0].style.color = 'rgba(255, 255, 255, 0.4)'
                    options[0].style.backgroundColor = '#594e5c'
                    j = i
                }
                if (j < i){
                    options[j].style.color = 'rgba(255, 255, 255, 0.4)'
                    options[j].style.backgroundColor = '#594e5c'
                }
                j -= 1
                options[j].style.color = 'white'
                options[j].style.backgroundColor = '#3e2e2e'
            }
        }
    })
}