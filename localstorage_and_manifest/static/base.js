

function show_test_data(test_data_values) {
    $('#data_list').html('');
    localStorage.setItem('test_data', test_data_values);
    for (i = 0; i < test_data_values.length; i++) {
        $('#data_list').append('<li>' + test_data_values[i] + '</li>');
    }
}

function get_test_data() {
    $('#online_status').removeClass('offline').removeClass('online').html('pending...');
    if(localStorage.test_data !== 'undefined') {
        test_data_values = localStorage.test_data;
    } else {
        test_data_values = [];
    }
    $.ajax({
        url : "/get_data",
        type: "GET",
        dataType: "json",
        data: {'test_data_values': test_data_values},
        success: function(data) {
            $('#online_status').removeClass('offline');
            $('#online_status').addClass('online');
            $('#online_status').html('online');
            show_test_data(data.test_data_values);
        },
        error: function () {
            $('#online_status').addClass('offline');
            $('#online_status').removeClass('online');
            $('#online_status').html('offline');
            show_test_data(test_data_values.split(','));
        }
    });
}

$(document).ready(function() {
    if(typeof(Storage) !== "undefined") {
        $('#clear_localstorage_button').on('click', function() {
            localStorage.removeItem('test_data');
            $('#data_list').html('');
            test_data_values = [];
        });
        $('#load_data_button').on('click', get_test_data);
        get_test_data();
    } else {
        alert('Sorry, your Browser does not support localStorage.');
    }
});
