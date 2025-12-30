function enterAdd() {
    document.getElementById("userBox").classList.add("editing");
}

function closeForm() {
    document.getElementById("userBox").classList.remove("editing");
}

function openDelete(id) {
    document.getElementById("delete_user_id").value = id;
    document.getElementById("deleteModal").style.display = "flex";
}

function closeDelete() {
    document.getElementById("deleteModal").style.display = "none";
}
