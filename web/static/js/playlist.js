function rowhandlers() {
    var table = document.getElementById("playlist");
    var rows = table.getElementsByTagName("tr");
    for (i = 0; i < rows.length; i++) {
        var currentRow = table.rows[i];
        var createClickHandler = function(row) {
            return function() {
                alert("id:" + row);
            };
        };
        console(i);
        currentRow.onclick = createClickHandler(currentRow);
    }
}
