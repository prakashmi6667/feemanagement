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

function fn_GetDistrict() {

    __ID = $('#id_state').val()
    $.ajax({
        url: '/franchise/district/' + __ID + '/',
    }).done(function(res) {
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">select Drstrict </opction>'
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