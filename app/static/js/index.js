DataTable.defaults.layout = {
    topStart: null,
    topEnd: null,
    bottomStart: null,
    bottomEnd: null
};

function format ( d ) {
//This function return the data to be presented in the child row of the grid for a parent row
  return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
            '<td>Development team email:</td>'+
            `<td><a href="mailto:${d[7]}">${d[7]}</a></td>` +
        '</tr>'+
        '<tr>'+
            '<td>Application Url:</td>'+
            `<td><a href="${d[8]}">${d[8]}</a></td>` +
        '</tr>'+
        ( d[9] !== 'None' ?
        '<tr>'+
            '<td>Swagger:</td>'+
            `<td><a href="${d[9]}">${d[9]}</a></td>` +
        '</tr>' : '')
        + '<tr>'+
            '<td>Bitbucket:</td>'+
            `<td><a href="${d[10]}">${d[10]}</a></td>` +
        '</tr>'+
        ( d[11] !== 'None' ?
        '<tr>'+
            '<td>Extra Info:</td>'+
            `<td>${d[11]}</td>` +

        '</tr>' : '')

    + '</table>';
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
            targets: 6,
            className: 'dt-body-right'
      },
      {
        targets: [7,8,9,10,11],
        visible: false
      },
      {
        targets: 4,
        defaultContent: '<div class="spinner-border spinner-border-sm" role="status"></div>',
        render: function (data, type, row, meta) {
            var currentCell = $("#applicationTable").DataTable().cells({"row":meta.row, "column":meta.col}).nodes(0);
            $.ajax({
                url: data,
            }).done(function (data, textStatus, xhr) {
                xhr.status == 200 ? $(currentCell).html('<i class="bi bi-circle-fill text-success"></i>') : $(currentCell).html('<i class="bi bi-circle-fill text-danger"></i>')
            }).fail(function () {
                $(currentCell).html('<i class="bi bi-circle-fill text-danger"></i>')
            })
            return null

            }
        }
    ],
  layout: {
        topStart: {
            buttons: [
                {
                  extend: 'excelHtml5',
                  exportOptions: {
                      columns: [1,2,3, 6, 7, 8, 9, 10]
                  }
                },
            ]

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

var table2 = $('#serverTable').DataTable({
    columnDefs: [
        {
            targets: 4,
            className: 'dt-body-right'
        }
      ],
    layout: {
            topStart: {
                buttons: [
                    {
                        extend: 'excelHtml5',
                        exportOptions: {
                            columns: [0,1,2,3]
                        }
                    }
                ]
            },
            topEnd: 'search',
            bottom: ['info', 'pageLength', 'paging']
      }
})
