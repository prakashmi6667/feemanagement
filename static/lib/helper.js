function fn_TestJSON(text) {
    if (typeof text == "string") {
        return false;
    }
    try {
        text = JSON.stringify(text)
        JSON.parse(text);
        return true;
    } catch (error) {
        console.log(error)
        return false;
    }
}

function fn_GetDistricts() {
    __ID = $('#id_state option:selected').val()
    $.ajax({
        url: "/settings/districts/" + __ID + "/",
    }).done(function(res) {
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select District</option>'
            if (fn_TestJSON(res)) {
                $.each(res, function() {
                    objHTML += '<option value="' + this.pk + '">' + this.fields.name + '</option>'
                })
            }
            $('#id_district').empty().append(objHTML)
        }
        $('#id_district').selectpicker('refresh');
    });
}

function fn_GetCourse() {
    __ID = $('#id_student').val()
    console.log(__ID)
    $.ajax({
        url: '/fees/course/fee/' + __ID + '/',
    }).done(function(res) {


        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select Course </option>'
            if (fn_TestJSON(res)) {
                console.log(res)
                $.each(res, function() {
                    objHTML += '<option value="' + this.pk + '">' + this.fields.name + '</option>'
                })
            }
            $('#id_course').empty().append(objHTML)
        }
    });
}

function fn_GetCourseAmount() {
    __ID = $('#id_course').val()
    $.ajax({
        url: '/fees/course/amount/' + __ID + '/',
    }).done(function(res) {

        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select Course </option>'
            if (fn_TestJSON(res)) {
                console.log(res)
                $.each(res, function() {
                    objHTML += '<option value="' + this.pk + '">' + this.fields.name + '</option>'
                })
            }
            $('#id_course').empty().append(objHTML)
        }
    });
}