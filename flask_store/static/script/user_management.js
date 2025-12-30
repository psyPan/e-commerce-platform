function enterCreateUser() {
    const box = document.getElementById("userBox");
    if (!box) {
        console.error("userBox not found");
        return;
    }
    box.classList.add("editing-customer");
    box.classList.remove("editing-owner");
}

function enterCreateOwner() {
    const box = document.getElementById("userBox");
    if (!box) {
        console.error("userBox not found");
        return;
    }
    box.classList.add("editing-owner");
    box.classList.remove("editing-customer");
}

function closeForm() {
    const box = document.getElementById("userBox");
    box.classList.remove("editing-customer", "editing-owner");
}
