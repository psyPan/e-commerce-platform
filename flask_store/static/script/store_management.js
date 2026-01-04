function enterAdd() {
    document.querySelector(".dashboard-card").classList.add("editing");
}

function exitAdd() {
    document.querySelector(".dashboard-card").classList.remove("editing");
}

function openDelete(id) {
    document.getElementById("delete_store_id").value = id;
    document.getElementById("deleteModal").style.display = "flex";
}

function closeDelete() {
    document.getElementById("deleteModal").style.display = "none";
}

