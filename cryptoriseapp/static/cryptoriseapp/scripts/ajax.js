"use scrict"

function $(c) {
    return document.getElementById(c);
}

let _tkn = $('us_tkn').children[0].getAttribute('value')

// home invest button fuction

function homeinvest(param){
    let inter = param
    let test = param.parentElement
    let childs = test.children

    let plantype = childs[0];
    let percent = childs[1];
    let price = childs[4];

    let new_plan = plantype.innerHTML
    let main_plan = new_plan.replace(/ /g, '')

    var main_percent = percent.innerHTML
    var new_percent = main_percent.replace('%',"")
    var till =  new_percent.replace('.', '')
    let dobble = '0'+'0'
    var last = till.replace(dobble,'')

    let main_price = price.innerHTML
    let first_price = main_price.replace('$','')
    var price_text = 'Min :'
    let send_priice = first_price.replace(price_text, '')
    let last_price = send_priice.replace(',', '')
    let  final_price = last_price.replace(/ /g, '')

    var url = '/place_invest/';
    var form_data = new FormData();
    form_data.append('plan', main_plan);
    form_data.append('percent', last);
    form_data.append('price', final_price);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': _tkn
        },
        body: form_data,
    })
    .then(response => response.json())
    .then(data => {
        if(data.S){
            console.log(data.S)
            window.location.replace(`/plan/selection/${main_plan}=${final_price}`)
        }
        else{
            console.log('post error')
        }
    })
    .catch((error) => {
        console.log('an error occured')
    })

}

function deposite(param){
    let inter = param
    param.style.backgroundColor = '#35edfdb4';
    let test = param
    let childs = test.children

    let plantype = childs[0];
    let percent = childs[1];
    let price = childs[3];
    let price_child = price.children[0]
    let new_plan = plantype.innerHTML
    let main_plan = new_plan.replace(/ /g, '')

    var main_percent = percent.innerHTML
    var new_percent = main_percent.replace('%',"")
    var till =  new_percent.replace('.', '')
    var last = till

    let main_price = price_child.innerHTML
    let first_price = main_price.replace('$','')
    var price_text = 'Min:'
    let send_priice = first_price.replace(price_text, '')
    let last_price = send_priice.replace(',', '')
    let  final_price = last_price.replace(/ /g, '')

    var url = '/place_invest/';
    var form_data = new FormData();
    form_data.append('plan', main_plan);
    form_data.append('percent', last);
    form_data.append('price', final_price);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': _tkn
        },
        body: form_data,
    })
    .then(response => response.json())
    .then(data => {
        if(data.S){
            console.log(data.S)
            $('amount').value = last_price;
            let _tps = $('amount').offsetTop;
            const dist_tp =Number(_tps);
            window.scrollTo({ top: dist_tp, behavior: 'smooth' });
            $('checkout').onclick = function() {
                window.location.replace(`/plan/selection/${main_plan}=${final_price}`)
            }
        }
        else{
            console.log('post error')
        }
    })
    .catch((error) => {
        console.log('an error occured')
    })
}

function new_img() {
    let img = $('user_img')
    if (!img.files[0]) {
        showmsg('e_flash', 'Please add an image')
    }
    else{
    var url = '/update_img/';
    var form_data = new FormData();
    form_data.append('image', img.files[0]);
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': _tkn
        },
        body: form_data,
    })
    .then(response => response.json())
    .then(data => {
        if(data.S){
           showmsg('s_flash', data.S)
           setTimeout(() => {
            window.location.reload()
           }, 200);
        }else if(data.E){
            showmsg('e_flash', data.E)
        }else{
            showmsg('e_flash', 'Post error occured')
        }
    })
    .catch((error) => {
        showmsg('e_flash', 'Can not get url or you are not connected to the internet..')
    })
    }
}


datalist = $('country')
datalist.addEventListener("change", () =>{
    _sele_cur_inner = datalist.value;
    var _cont_ls = datalist.children, _crc_val = '', _crname_val ='';
    for (const elem of _cont_ls) {
        const _it_map = new Map();
        const _crc_map = new Map();
        _it_map.set(`${elem.getAttribute('value')}`);
        _crc_map.set(`${elem.getAttribute('cr_c')}`);
                    
                    _sele_opt = _it_map.has(_sele_cur_inner);
                    for (const key of _it_map.keys()) {
                        if(_sele_opt === true){
                            _crname_val = key;
                        }
                    }
                    for (const _crkey of _crc_map.keys()) {
                        if(_sele_opt === true){ 
                            _crc_val = _crkey;
                        }
                    }
                }
                $('c_code').value = _crc_val;
                console.log(_crc_val)
        });


function showmsg(clas, msg){
    $('float_msg').innerHTML = `<aside class="${clas}" id="${clas}">${msg}
<span onclick="close_msg(this)">
<svg xmlns="http://www.w3.org/2000/svg" height="10px" viewBox="0 -960 960 960" width="10px" fill="currentcolor" style="cursor:pointer;">
<path d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"/></svg>
</span>
</aside>`;
let _tps = $('float_msg').offsetTop;
const dist_tp2 =Number(_tps);
window.scrollTo({ top: dist_tp2, behavior: 'smooth'});
}

function close_msg(params) {
    let get = params.parentElement;
    get.style.display = 'none';
} 

function inputvalidator(){
    let inputs = document.querySelectorAll('input')
    inputs.forEach(input => {
        let inputvalue = input.value;
        console.log(inputvalue)
    })
}

function update_profile(){
    var full_name = $('f_name'), phone = $('phone'), email = $('new_email'), country = $('country'), c_code = $('c_code'), bitwallet = $('btc'), litwallet = $('lit'), ethwallet = $('eth'), tronwallet = $('tron'), trcwallet = $('trc'), ercwallet = $('erc');
    
    var url = '/update_profile/';
    var form_data = new FormData();
    form_data.append('fname', full_name.value);
    form_data.append('phone', phone.value);
    form_data.append('email', email.value);
    form_data.append('country', country.value);
    form_data.append('code', c_code.value);
    form_data.append('bit', bitwallet.value);
    form_data.append('lit', litwallet.value);
    form_data.append('eth', ethwallet.value);
    form_data.append('tron', tronwallet.value);
    form_data.append('trc', trcwallet.value);
    form_data.append('erc', ercwallet.value);
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': _tkn
        },
        body: form_data,
    })
    .then(response => response.json())
    .then(data => {
        if(data.S){
           showmsg('s_flash', data.S)
           setTimeout(() => {
            window.location.reload()
           }, 200);
        }else if(data.E){
            showmsg('e_flash', data.E)
        }else{
            showmsg('e_flash', 'Post error occured')
        }
    })
    .catch((error) => {
        showmsg('e_flash', 'Can not get url or you are not connected to the internet..')
    })
}

function update_password(){
    var newpassword = $('new-pass'), conf_passwd = $('re-pass');
    if (newpassword.value.trim().length < 6) {
        showmsg('e_flash', 'Password is too short')
    }
    else if (conf_passwd.value!==newpassword.value) {
        showmsg('e_flash', 'Passwords does not match')
    }else{
    var url = '/update_pass/';
    var form_data = new FormData();
    form_data.append('passwd', newpassword.value);
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': _tkn
        },
        body: form_data,
    })
    .then(response => response.json())
    .then(data => {
        if(data.S){
           showmsg('s_flash', data.S)
           setTimeout(() => {
            window.location.reload()
           }, 200);
        }else if(data.E){
            showmsg('e_flash', data.E)
        }else{
            showmsg('e_flash', 'Post error occured')
        }
    })
    .catch((error) => {
        showmsg('e_flash', 'Can not get url or you are not connected to the internet..')
    })
    }
}


function get_errortag(input, msgbox, msg) {
    $(input).classList.add('highlight')
    $(msgbox).innerText = msg;
    setTimeout(() => {
        $(input).classList.remove('highlight');
        $(msgbox).innerText = ``;
    }, 5000);
    let _tps = $(input).offsetTop;
    const dist_tp =Number(_tps-130);
    window.scrollTo({ top: dist_tp, behavior: 'smooth' }); 
}

function register_user() {
    var em =/^[A-Za-z\._\-0-9]*[@][A-Za-z]*[\.][a-z]{2,4}$/ 
    let username = $('username'), full_name = $('fullname'), phone = $('number'), email = $('email'), country = $('country'), c_code = $('c_code'), bitwallet = $('bitcoin'), litwallet = $('litecoin'), ethwallet = $('ethereum'), tronwallet = $('tron'), trcwallet = $('tron1'), ercwallet = $('tron2'), password = $('password'), repas = $('repassword');
    if (!username.value.match(/\w+/)){
        get_errortag('username', 'u_msg', 'Enter a valid username')
    }
    else if (!full_name.value.match(/\w+/)) {
        get_errortag('fullname', 'f_msg', 'Enter fullname')
    }
    else if(!email.value.match(em)){
        get_errortag('email', 'e_msg', 'Invalid email')
    }
    else if(!country.value.match(/\w+/)){
        get_errortag('country', 'c_msg', 'Select a valid country')
    }
    else if(!phone.value.match(/^\+?[1-9]\d{1,14}$/)){
        get_errortag('number', 'ph_msg', 'Enter a valid phone number')
    }
    else if(!password.value.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{6,}$/)){
        get_errortag('password', 'p_msg', 'Password must contain at least 6 characters, including uppercase, lowercase letters and numbers')
    }
    else if(repas.value!==password.value){
        get_errortag('repassword', 'rp_msg', 'Passwords does not match')
    }else{
        var url = '/new_user/';
        var form_data = new FormData();
        form_data.append('uname', username.value);
        form_data.append('fname', full_name.value);
        form_data.append('phone', phone.value);
        form_data.append('email', email.value);
        form_data.append('country', country.value);
        form_data.append('code', c_code.value);
        form_data.append('bit', bitwallet.value);
        form_data.append('lit', litwallet.value);
        form_data.append('eth', ethwallet.value);
        form_data.append('tron', tronwallet.value);
        form_data.append('trc', trcwallet.value);
        form_data.append('erc', ercwallet.value);
        form_data.append('passwd', password.value);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': _tkn
            },
            body: form_data,
        })
        .then(response => response.json())
        .then(data => {
            if(data.S){
               animatedText('<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentcolor"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Z"/></svg>', data.S, 'login_animeted')
               setTimeout(() => {
                window.location.reload()
               }, 1500);
            }else if(data.E){
                showmsg('e_flash', data.E)
            }else{
                showmsg('e_flash', 'Post error occured')
            }
        })
        .catch((error) => {
            showmsg('e_flash', 'Can not get url or you are not connected to the internet..')
        }) 
    }
}

function animatedText(icon, text, cls){
    $('float_msg').classList.add(cls)
    $('float_msg').innerHTML = `<div>${icon} <span>${text}</span></div>`;
}


function login_user() {
    let user = $('username'), password = $('password');
    if(!user.value.match(/\w+/)){
        get_errortag('username', 'u_msg', 'Enter a valid username')
    }else{
        var url = '/log_user/';
        var form_data = new FormData();
        form_data.append('uname', user.value);
        form_data.append('passwd', password.value);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': _tkn
            },
            body: form_data,
        })
        .then(response => response.json())
        .then(data => {
            if(data.S){
               animatedText('<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="currentcolor"><path d="m424-296 282-282-56-56-226 226-114-114-56 56 170 170Zm56 216q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Z"/></svg>', data.S, 'login_animeted')
               setTimeout(() => {
                window.location.reload()
               }, 1500);
            }else if(data.E){
                showmsg('e_flash', data.E)
            }else{
                showmsg('e_flash', 'Post error occured')
            }
        })
        .catch((error) => {
            showmsg('e_flash', 'Can not get url or you are not connected to the internet..')
        }) 
    }
}
