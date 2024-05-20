let list =document.querySelectorAll(".nav-bar li");

function activeLink(){
    list.forEach((item) => {
        item.classList.remove("hovered");

    });
    this.classList.add("hovered");
}
list.forEach(item => item.addEventListener("mouseover",activeLink));