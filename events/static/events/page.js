const btn1 = document.querySelector("#btn1");
const btn2 = document.querySelector("#btn2");
const btn3 = document.querySelector("#btn3");

const form1 = document.querySelector(".form1");
const form2 = document.querySelector(".form2");
const form3 = document.querySelector(".form3");
const in_form2 = document.querySelector(".in_form2");

form2.style.display = "none";
form3.style.display = "none";

 btn1.addEventListener("click", function(){
    form1.style.display = "block";
    form2.style.display = "none";
    form3.style.display = "none";
    document.getElementById('text_form_2').value = '';
    document.getElementById('select_form_2').value = '';
    document.getElementById('text_form_3').value = '';
    clear_form2();
 });

 btn2.addEventListener("click", function(){
    form1.style.display = "none";
    form2.style.display = "block";
    form3.style.display = "none";
    document.getElementById('text_form_1').value = '';
    document.getElementById('text_form_3').value = '';
 });

  btn3.addEventListener("click", function(){
    form1.style.display = "none";
    form2.style.display = "none";
    form3.style.display = "block";
    document.getElementById('text_form_1').value = '';
    document.getElementById('text_form_2').value = '';
    document.getElementById('select_form_2').value = '';
    clear_form2();
 });

 function clear_form2() {
    let children = Array.from(form2.children).slice(3)
    while (children.length > 0){
        form2.removeChild(form2.lastElementChild);
        children.splice(-1);
    }
    btnDelete.style.display = "none";
 }