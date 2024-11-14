DataTable.defaults.layout = {
    topStart: null,
    topEnd: null,
    bottomStart: null,
    bottomEnd: null
};

new DataTable('#applicationTable', {
    layout: {
        topEnd: 'search',
        bottom: ['info', 'pageLength', 'paging']
    }
});
