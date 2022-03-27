
// simply making a dataTable object and returns it; u have to give table ID
function getDataTable (id) {
    return $(`#${id}`).DataTable({
        "order": [],
        "responsive": true,
        "lengthChange": false,
        "autoWidth": false,
        "language": {
            "infoFiltered": `(${gettext('Filtered ')}_MAX_(${gettext(' records')})`,
            "zeroRecords": gettext('No records found'),
            "info": `${gettext('Showing ')}_START_${gettext(' to ')}_END_${gettext(' of ')}_TOTAL_`,
            "infoEmpty": gettext('No records'),
            "search": gettext('Search'),
            "paginate": {
                "previous": gettext('Previous'),
                "next": gettext('Next'),
            }
        }
    })
}
