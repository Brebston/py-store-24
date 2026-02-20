function showErrorPopup(message) {
    const popup = document.getElementById("error-popup");
    popup.innerText = message;
    popup.classList.add("show");

    setTimeout(() => {
        popup.classList.remove("show");
    }, 3000);
}
