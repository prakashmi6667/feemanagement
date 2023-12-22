
window.addEventListener('load', function () {
    (function ($) {

        $('#other_facilities_set-group').find('fieldset').find('div.add-row').find('a').on('click', function () {
            // console.log('hi', $('#other_facilities_set-group').find('fieldset').find('div.dynamic-other_facilities_set'))

            var sets = $('#other_facilities_set-group').find('fieldset').find('div.dynamic-other_facilities_set')
            var last_ID = []
            $.each(sets, function () {
                let __set = this
                if (last_ID.length > 0) {
                    $.each(last_ID, function () {
                        let id = this[0]
                        $(__set).find('select').find('option[value="' + id + '"]').prop('disabled', true);
                    })
                }

                if ($(__set).find('select option:selected').index() > 0) {
                    last_ID.push($(__set).find('select').val())
                }

                $(__set).find('select').off('change')
                $(__set).find('select').on('change', fn_onchange)
            })
        })

        var sets = $('#other_facilities_set-group').find('fieldset').find('div.dynamic-other_facilities_set')
    })(jQuery);


    function fn_onchange() {
        var sets = $('#other_facilities_set-group').find('fieldset').find('div.dynamic-other_facilities_set')
        var last_ID = []

        $.each(sets, function () {
            let __set = this
            if (last_ID.length > 0) {
                
                $.each(last_ID, function () {
                    let id = this[0]
                    // $(this).find('select option:eq(0)').prop('selected', true);
                    $(__set).find('select').find('option[value="' + id + '"]').prop('selected', false);

                    // $(__set).find('select').find('option:disabled').prop('disabled', false);
                    $(__set).find('select').find('option[value="' + id + '"]').prop('disabled', true);
                })
            }

            if ($(__set).find('select option:selected').index() > 0) {
                last_ID.push($(__set).find('select').val())
            }
        })
    }
});

