
// simply making a dataTable object and returns it; u have to give table ID
function getDataTable (id) {
    return $(`#${id}`).DataTable({
        "responsive": true,
        "lengthChange": false,
        "autoWidth": false,
        "language": {
            "infoFiltered": "(Отфильтровано _MAX_ записей)",
            "zeroRecords": "Записей не найдено",
            "info": "Показано с _START_ по _END_ из _TOTAL_",
            "infoEmpty": "Нет записей",
            "search": "Поиск",
            "paginate": {
                "previous": "Предыдущая",
                "next": "Следующая",
            }
        }
    })
}
