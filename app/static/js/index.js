//DataTable.defaults.layout = {
//    topStart: null,
//    topEnd: null,
//    bottomStart: null,
//    bottomEnd: null
//};

// Formatting function for row details - modify as you need
function format(d) {
    // `d` is the original data object for the row
    return (
        '<dl>' +
        '<dt>Development team email:</dt>' +
        '<dd>' +
        d.team_email +
        '</dd>' +
        '<dt>Application Url:</dt>' +
        '<dd>' +
        d.url +
        '</dd>' +
        '<dt>Swagger Link:</dt>' +
        '<dd>' +
        d.swagger_link +
        '</dd>' +
        '</dl>'
    );
}

let table = new DataTable('#applicationTable', {
    ajax: {
    url: '/fetch_all',
    dataSrc: '',
    },
    columns: [
    {
            className: 'dt-control',
            orderable: false,
            data: null,
            defaultContent: ''
        },
        { data: 'name' },
        { data: 'team_name' },
        { data: 'status' }
    ],
//    layout: {
//        topEnd: 'search',
//        bottom: ['info', 'pageLength', 'paging']
//    }

});


// Add event listener for opening and closing details
table.on('click', 'td.dt-control', function (e) {
    let tr = e.target.closest('tr');
    let row = table.row(tr);

    if (row.child.isShown()) {
        // This row is already open - close it
        row.child.hide();
    }
    else {
        // Open this row
        row.child(format(row.data())).show();
    }
});
