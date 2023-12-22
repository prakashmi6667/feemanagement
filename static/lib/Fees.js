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

__Balance = 0

function fn_GetCourse() {
    __ID = $('#id_student option:selected').val()
    $.ajax({
        url: "/fees/fee-installment/" + __ID + "/",
    }).done(function(res) {
        console.log(res)
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">Select Course</option>'

            if (fn_TestJSON(res)) {
                __LastData = JSON.parse(res[0]['LastData'])
                __total_installment = JSON.parse(res[0]['total_installment'])
                console.log(__total_installment)

                if (__total_installment == 1) {
                    $('#objInstallment').text('This is your last installment. Do not leave any balance here!')
                    $('#objInstallment').parent().removeAttr('style')
                }

                if (__LastData.length > 0) {
                    balance = parseFloat(__LastData[0].fields.total_amount) - parseFloat(__LastData[0].fields.paid_amount)
                    if (balance > 0) {
                        $('#objPendingAmount').text('Previews Fee Balance : ' + parseFloat(balance).toFixed(2) + ' Added in total.')
                        $('#objPendingAmount').parent().removeAttr('style')
                    }
                    __Balance = parseFloat(balance).toFixed(2)
                } else {
                    balance = 0
                    __Balance = 0
                    $('#objPendingAmount').parent().attr('style', 'display: none;')
                }

                $.each(JSON.parse(res[0]['Data']), function() {
                    $('#id_course').val(this.pk)
                    $('#id_fee, #id_paid_amount, #id_total_amount').val(this.fields.monthly_amount)
                    total = parseFloat(this.fields.monthly_amount) + parseFloat(balance)
                    $('#id_total_amount').val(parseFloat(total).toFixed(2))
                })
            }

        }
    });
}


$(function() {
    $('#id_fine').on('input', function() {
        __fee = $('#id_fee').val()
        __dis = $('#id_fine').val()
        if ($.isNumeric(__dis) && $.isNumeric(__fee)) {
            __total = parseFloat(__fee) + parseFloat(__Balance) + parseInt(__dis)
            $('#id_total_amount').val(parseFloat(__total).toFixed(2))
            $('#id_paid_amount').val(parseFloat(__total).toFixed(2))
        }
    })
})