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

function fn_timer(dt) {
    // Set the date we're counting down to
    var countDownDate = new Date(dt).getTime();

    // Update the count down every 1 second
    var x = setInterval(function() {

        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Display the result in the element with id="demo"
        document.getElementById("demo").innerHTML = days + "d ";
        document.getElementById("demo1").innerHTML = hours + "h ";
        document.getElementById("demo2").innerHTML = minutes + "m ";
        document.getElementById("demo3").innerHTML = seconds + "s ";

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById("demo").innerHTML = "00";
            document.getElementById("demo1").innerHTML = "00";
            document.getElementById("demo2").innerHTML = "00";
            document.getElementById("demo3").innerHTML = "00";
            $('#divSTExam').show();
            $('#aStart').attr('href', '/exams/exam-start/' + $('#txtExamCode').val() + '/')
        }
    }, 1000);
}

function fn_verification() {

    var code = $('#txtExamCode').val()

    fetch('/exams/api/verification/' + code + '/').then(fn_EncryptResponse).then(function(res) {
        var objHTML = '';
        res = res[0]
            // console.log(res, '------')
        var date = res.date;
        // console.log(date)
        $('#divTime').show();
        fn_timer(date)


    })

}


function fn_DateDiffrence(dateNow, dateExam) {
    // get total seconds between the times
    var _TodayDate = new Date(dateNow);
    var dt = new Date(dateExam);
    var delta = Math.abs(dt - _TodayDate) / 1000;

    // calculate (and subtract) whole days
    var days = Math.floor(delta / 86400);
    delta -= days * 86400;

    // calculate (and subtract) whole hours
    var hours = Math.floor(delta / 3600) % 24;
    delta -= hours * 3600;

    // calculate (and subtract) whole minutes
    var minutes = Math.floor(delta / 60) % 60;
    delta -= minutes * 60;

    // what's left is seconds
    var seconds = delta % 60; // in theory the modulus is not required

    return { Days: days, Hours: hours, Minutes: minutes, Seconds: seconds }
}

function fn_exam() {

    var exam = $('#txtexamhidden').val()
    fetch('/exams/exam-question/get/api/' + exam + '/').then(fn_EncryptResponse).then(function(res) {
        var objHTML = '',
            count = 1;

        $.each(res, function() {
            objHTML +=

                '<div class="col-md-8 qus" id="qu_' + count + '" >' +
                '                        <div class="card">' +
                '                                    <div class="card-header">' +
                '' +
                '                                        <h2>Question ' + count + ' :  ' + this.name + ' </h2>' +
                '                                    </div>' +
                '                                    <div class="card-body">' +
                '                                        <blockquote class="blockquote mb-0">' +
                '                                            <div class="col-md-10">' +
                '                                                <div class="col-md-5">' +
                '                                                    <div class="form-check-inline">' +
                '                                                        <label class="form-check-label">' +
                '                                                              <input type="radio" class="form-check-input" name="optradio' + count + '"> ' + this.option1 + '' +
                '                                                            </label>' +
                '                                                    </div>' +
                '                                                </div>' +
                '                                                <div class="col-md-4">' +
                '                                                    <div class="form-check-inline">' +
                '                                                        <label class="form-check-label">' +
                '                                                              <input type="radio" class="form-check-input" name="optradio' + count + '"> ' + this.option2 + '' +
                '                                                            </label>' +
                '                                                    </div>' +
                '                                                </div>' +
                '                                                <div class="col-md-5">' +
                '                                                    <div class="form-check-inline">' +
                '                                                        <label class="form-check-label">' +
                '                                                              <input type="radio" class="form-check-input" name="optradio' + count + '"> ' + this.option3 + '' +
                '                                                            </label>' +
                '                                                    </div>' +
                '                                                </div>' +
                '                                                <div class="col-md-4">' +
                '                                                    <div class="form-check-inline">' +
                '                                                        <label class="form-check-label">' +
                '                                                              <input type="radio" class="form-check-input" name="optradio' + count + '"> ' + this.option4 + '' +
                '                                                            </label>' +
                '                                                    </div>' +
                '                                                </div>' +
                '' +
                '                                           </div>' +
                '' +
                '                           </blockquote>' +
                '                    </div>' +
                '         </div>' +
                '</div>';



            count += 1;
        })

        $('#divqust').empty().append(objHTML)
        console.log(res, '------', total_index)

        total_index = res.length;


        fn_display()


    })
}