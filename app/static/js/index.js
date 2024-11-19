DataTable.defaults.layout = {
    topStart: null,
    topEnd: null,
    bottomStart: null,
    bottomEnd: null
};

function format ( d ) {

  return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Development team email:</td>'+
            `<td><a href="mailto:${d[5]}">${d[5]}</a></td>` +
        '</tr>'+
        '<tr>'+
            '<td>Application Url:</td>'+
            `<td><a href="${d[6]}">${d[6]}</a></td>` +
        '</tr>'+
        '<tr>'+
            '<td>Swagger Link:</td>'+
            `<td><a href="${d[7]}">${d[7]}</a></td>` +
        '</tr>'+
    '</table>';
}

  var table = $('#applicationTable').DataTable({
    columnDefs: [
      {
        targets: 0,
        className:      'dt-control',
        orderable:      false,
        data:           null,
        defaultContent: ''
      },
      {
        targets: [5,6,7],
        visible: false
      },
      {
        targets: 3,
        defaultContent: '<div class="spinner-border spinner-border-sm" role="status"></div>',
        render: function (data, type, row, meta) {
            var currentCell = $("#applicationTable").DataTable().cells({"row":meta.row, "column":meta.col}).nodes(0);
            $.ajax({
                url: 'https://jsonplaceholder.typicode.com/todos/1'
            }).done(function (data, textStatus, xhr) {
                xhr.status == 200 ? $(currentCell).html('<i class="bi bi-circle-fill text-success"></i>') : $(currentCell).html('<i class="bi bi-circle-fill text-danger"></i>')
            })
            return null

            }
        }
    ],
  layout: {
        topStart: {
            buttons: ['excel']
        },
        topEnd: 'search',
        bottom: ['info', 'pageLength', 'paging']
  }
  });

    // Add event listener for opening and closing details
    $('#applicationTable').on('click', 'td.dt-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
