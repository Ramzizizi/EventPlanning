const btnAdd = document.querySelector("#btn-add");
const btnDelete = document.querySelector("#btn-delete");

btnDelete.style.display = "none";

 btnAdd.addEventListener("click", function(){
     let clone = in_form2.cloneNode(true)
     clone.children[0].children[1].name = clone.children[0].children[1].name + '_' + (form2.children.length - 1)
     clone.children[1].children[1].name = clone.children[1].children[1].name + '_' + (form2.children.length - 1)
     document.getElementsByClassName("form2")[0].appendChild(clone)
     btnDelete.style.display = "inline-flex";
 });
 btnDelete.addEventListener("click", function(){
    form2.removeChild(form2.lastChild)
    console.log(form2.children)
    if (form2.children.length === 3) btnDelete.style.display = "none";
 });