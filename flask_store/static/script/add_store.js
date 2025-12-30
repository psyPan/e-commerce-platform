function enterAdd() {
    document.querySelector(".dashboard-card").classList.add("editing");
}

function exitAdd() {
    document.querySelector(".dashboard-card").classList.remove("editing");
}

function openDeleteModal(storeId) {
    const modal = document.getElementById("deleteModal");
    const form = document.getElementById("deleteForm");

    form.action = `/store/${storeId}/delete`;
    modal.style.display = "flex";
}

function closeDeleteModal() {
    document.getElementById("deleteModal").style.display = "none";
}
