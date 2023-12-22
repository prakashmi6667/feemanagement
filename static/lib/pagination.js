var selected_index = 1;
var total_index = 0;



function fn_display(index = 1) {

    $('#qu_' + index).removeClass('qus')
        // console.log('*/*/*/*', index, $('#qu_' + index))

    selected_index = index

    var objHTML = '';


    for (var i = 1; i <= total_index; i++) {

        objHTML +=
            '<div class="col-md-2 form-group"><button type="button" class="btn btn-default" id="btn_' + i + '">' +
            '                                    <span class="badge badge-light">' + i + '</span></button>' +
            '</div>';
    }
    $('#divClick').empty().append(objHTML)

};


function fn_Next() {

    if (selected_index < total_index) {
        $('#qu_' + selected_index).addClass('qus')

        // var sltbtn = $('input[type = "radio"]').prop('checked', false);
        // console.log('sltbtn', sltbtn)
        if ($('input[type=radio]:checked').size() > 0) {

            var btnNO = $('#btn_' + selected_index);
            var qusNo = $('#qu_' + selected_index);

            var BtnNO = btnNO.attr('id').match(/\d+/);
            var QusNO = qusNo.attr('id').match(/\d+/);

            console.log('*******', QusNO[0], BtnNO[0])

            if (QusNO[0] == BtnNO[0]) {

                $('#btn_' + selected_index).addClass('btn-primary')

            }
        }
        selected_index++;
        $('#qu_' + selected_index).removeClass('qus')
    }


    // selected_index++;
    // $('#qu_' + selected_index).removeClass('qus')


    // console.log('*/*/*/*', $('#qu_' + selected_index))

};


function fn_Previous() {

    if (selected_index >= total_index) {
        $('#qu_' + selected_index).addClass('qus')
        selected_index--;
        $('#qu_' + selected_index).removeClass('qus')
    }

    // console.log('*/*/*/*', $('#qu_' + selected_index))

};

function fn_Submit() {

    // rd = $('input[name="optradio' + selected_index + '"]:checked').val()


    $('input[name="optradio' + selected_index + '"]').prop('disabled', true);

    var btnNO = $('#btn_' + selected_index);
    var qusNo = $('#qu_' + selected_index);

    var BtnNO = btnNO.attr('id').match(/\d+/);
    var QusNO = qusNo.attr('id').match(/\d+/);

    console.log('*******', QusNO[0], BtnNO[0])

    if (QusNO[0] == BtnNO[0]) {

        $('#btn_' + selected_index).addClass('btn-success')

    }

    //var a = $('#qu_' + selected_index)
    // console.log(a, '#qu_' + selected_index, '-=-=-=')

    // $('#qu_' + selected_index).addClass('qus')
    // selected_index++;
    // $('#qu_' + selected_index).removeClass('qus')

    // console.log('*/*/*/*', $('input[name="optradio' + selected_index + '"]:checked'))

};


function fn_check() {



}