function TreeData(data, select) {
    var main = document.querySelector(select);
    var treecanvas = document.createElement('div');
    treecanvas.className = 'tree';

    var treeCode = buildTree(data, 'None'); 
    treecanvas.innerHTML = treeCode;
    main.appendChild(treecanvas);

    $("#refresh-tree").click(function() {
        location.reload();
    });
}

function buildTree(data, parent) {
    var html = "<ul>";
    var hasChildren = false;

    for (var i = 0; i < data.length; i++) {
        if (data[i].parent === parent) {
            hasChildren = true;
            html += "<li><a href='#'>" + data[i].name + " - " + data[i].masteruser + "</a>";
            html += buildTree(data, data[i].name);
            html += "</li>";
        }
    }
    html += "</ul>";
    return hasChildren ? html : "";
}

document.addEventListener("DOMContentLoaded", function() {
    $(".vDateField").flatpickr({
        dateFormat: "d-m-Y",
    })
    $(".vTimeField").flatpickr({
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        time_24hr: true
    })
    $(document).ready(function() {
        $("span.datetimeshortcuts").detach(); 
    });

    $(".datetime").addClass("d-block mt-4");
    $(".datetime > input").addClass("my-3");
});
