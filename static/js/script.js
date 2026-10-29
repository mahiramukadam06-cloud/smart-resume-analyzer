// Simple UX enhancement: show the selected file name on the upload box.
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("resume");
    const fileNameLabel = document.getElementById("fileName");

    if (fileInput && fileNameLabel) {
        fileInput.addEventListener("change", function () {
            if (fileInput.files.length > 0) {
                fileNameLabel.textContent = fileInput.files[0].name;
            } else {
                fileNameLabel.textContent = "Choose a PDF, DOCX or TXT file";
            }
        });
    }
});
