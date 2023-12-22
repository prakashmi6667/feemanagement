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


function fn_GetCourse() {
    __ID = $('#id_student option:selected').val()
    $.ajax({
        url: "/fees/course/" + __ID + "/",
    }).done(function(res) {
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select Course</option>'

            if (fn_TestJSON(res)) {
                $.each(res, function() {
                    $('#id_course').val(this.pk)
                    $('#id_course').val(this.pk).trigger('change')
                })
            }

        }
    });
}

function fn_GetExam() {
    __ID = $('#id_course option:selected').val()
    $.ajax({
        url: "/exams/course/" + __ID + "/",
    }).done(function(res) {
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select Exam</option>'
            if (fn_TestJSON(res)) {
                $.each(res, function() {
                    objHTML += '<option value="' + this.pk + '">' + this.fields.name + '</option>'
                })
            }
            $('#id_exam').empty().append(objHTML)
        }
    });
}

$(function() {
    $('#id_discount').on('input', function() {
        __fee = $('#id_fee_amount').val()
        __dis = $('#id_discount').val()
        if ($.isNumeric(__dis) && $.isNumeric(__fee)) {
            __total = __fee - __dis
            $('#id_total_amount').val(__total)
        }
    })

    $('#id_monthly_amount').on('input', function() {
        if ($.isNumeric($('#id_monthly_amount').val())) {
            var tot = $('#id_total_amount').val();
            var mon = $('#id_monthly_amount').val();
            var inst = tot / mon;
            $('#id_total_installment').val(parseFloat(inst));
        } else {
            $('#id_total_installment').val(0);
        }
    })

    $('#id_total_installment').on('input', function() {
        if ($.isNumeric($('#id_total_installment').val())) {
            if ($('#id_total_installment').val() > 0) {
                var tot = $('#id_total_amount').val();
                var int = $('#id_total_installment').val();
                var mon = tot / int;
                $('#id_monthly_amount').val(parseFloat(mon).toFixed(2));
            } else {
                $('#id_monthly_amount').val(parseFloat(0).toFixed(2));
            }
        }
    })
})