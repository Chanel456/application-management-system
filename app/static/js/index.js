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
            `<td><a href="mailto:${d[6]}">${d[6]}</a></td>` +
        '</tr>'+
        '<tr>'+
            '<td>Application Url:</td>'+
            `<td><a href="${d[7]}" target="_blank">${d[7]}</a></td>` +
        '</tr>'+
        ( d[8] !== '' ?
        '<tr>'+
            '<td>Swagger:</td>'+
            `<td><a href="${d[8]}" target="_blank">${d[8]}</a></td>` +
        '</tr>' : '')
        + '<tr>'+
            '<td>Bitbucket:</td>'+
            `<td><a href="${d[9]}" target="_blank">${d[9]}</a></td>` +
        '</tr>'+
        ( d[10] !== '' ?
        '<tr>'+
            '<td>Extra Info:</td>'+
            `<td>${d[10]}</td>` +
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
            targets: 5,
            className: 'dt-body-right'
      },
      {
        targets: [6,7,8,9,10],
        visible: false
      },
    ],
  layout: {
        topStart: {
            buttons: [
                {
                  extend: 'excelHtml5',
                  exportOptions: {
                      columns: [1,2,3,4, 6, 7, 8, 9, 10]
                  },
                  title:'Asset Management System - Applications'
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
                        },
                        title:'Asset Management System - Servers'
                    }
                ]
            },
            topEnd: 'search',
            bottom: ['info', 'pageLength', 'paging']
      }
})

const textarea = document.getElementById('extra_info');
const charCount = document.getElementById('charCount');
const maxLength = textarea.getAttribute('maxlength');

textarea.addEventListener('input', () => {
    const remaining = maxLength - textarea.value.length; charCount.textContent = `${remaining} characters remaining`;
});
