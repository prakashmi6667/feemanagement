function fn_EncryptResponse(response) {
    try {
        if (response.status >= 200 && response.status < 300) {
            let clone = response.clone();
            var data = clone.json();
            return Promise.resolve(data).then(function(res) { return res });
        } else {
            return Promise.reject(new Error(response.statusText))
        }
    } catch (objErrorText) {
        console.log(objErrorText)
    }
}



function fn_OpenAdmitMdl(id = 0, pk = 0, fr = 0) {

    $('#mldadmitcard').modal('show');
    fetch('/exams/api/get/exam/' + id + '/').then(fn_EncryptResponse).then(function(res) {
        var objHTML = '<option value="0">Select Exam</option>';
        $.each(res, function() {
            objHTML +=
                '<option value="' + this.id + '">' + this.name + '</option>';

        });
        $('#ddlexam').empty().append(objHTML)

        $('#txtstudent').val(pk)
        $('#txtcourse').val(id)
        $('#txtfranchise').val(fr)

    })


}


function fn_SaveMdl() {

    var date1 = $('#txtdate').val()
    var exam1 = $('#ddlexam').val()

    if (date1 != '' && exam1 != '' && exam1 != 0) {

        let obj = {
            'student': $('#txtstudent').val(),
            'course': $('#txtcourse').val(),
            'franchise': $('#txtfranchise').val(),
            'exam': $('#ddlexam option:selected').val(),
            'date': $('#txtdate').val()
        }

        fetch('/exams/api/set/admit-card/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(obj)
        }).then(fn_EncryptResponse).then(function(res) {
            var objHTML = ''
            if (JSON.parse(res).isSaved == true) {
                $('#mldadmitcard').modal('hide');
                alert('Data  saved')
            } else {
                alert('Validation Error! data Not saved')
            };

            console.log(JSON.parse(res).isSaved)

        })
    } else {
        alert('Please fill the box!')
    }

}

function fn_isActivated(id) {

    fetch('/exams/api/activated/' + id + '/').then(fn_EncryptResponse).then(function(res) {
        if (JSON.parse(res).code != '') {
            $('#col_' + id).find('.act').remove()
            $('#col_' + id).find('.rev-card').remove()
            $('#col_' + id).append('<span>' + JSON.parse(res).code + '</span>')
                // $('#txtactivated').text(JSON.parse(res).code)

        } else {
            alert('Validation Error!')
        };
    })

}