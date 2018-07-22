'use strict';

var switchButton 			= document.querySelector('.switch-button');
var switchBtnRight 			= document.querySelector('.switch-button-case.right');
var switchBtnLeft 			= document.querySelector('.switch-button-case.left');
var activeSwitch 			= document.querySelector('.active');
var createAddressLink           = document.querySelector('.address-create');
var newAddress           = document.querySelector('.new-address');

function switchLeft(){
	switchBtnRight.classList.remove('active-case');
	switchBtnLeft.classList.add('active-case');
	activeSwitch.style.left 						= '0%';
}

function switchRight(){
	switchBtnRight.classList.add('active-case');
	switchBtnLeft.classList.remove('active-case');
	activeSwitch.style.left 						= '50%';
}

function createAddress() {

}

switchBtnLeft.addEventListener('click', function(){
	switchLeft();
}, false);

switchBtnRight.addEventListener('click', function(){
	switchRight();
}, false);

createAddressLink.addEventListener('click', function(){

})


const Client = require("bitcoin-client");
const client = new Client({ network: 'regtest' });

