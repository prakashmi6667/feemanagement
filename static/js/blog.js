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




function fn_GetSubcategory() {

    __ID = $('#id_category').val()
    $.ajax({
        url: '/subcategory/' + __ID + '/',
    }).done(function(res) {
        if (fn_TestJSON(res)) {
            var objHTML = '<option value="0">select subcategory </opction>'
            if (fn_TestJSON(res)) {
                $.each(res, function() {
                    objHTML += '<option value="' + this.pk + '">' + this.fields.name + '</option>'
                })
            }
            $('#id_sub_category').empty().append(objHTML)
        }
    });
}