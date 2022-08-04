$(document).ready(function () {

    function ajax_answer() {
        $.ajax({
            url: '/ajax-answer',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log("estamos aca " + response.finalSpeach);

                $('#ask-button').prop('disabled', false);

                finalSpeach = response.finalSpeach;

                $("#writing-notif").remove()

                $("#chat-window").append(`
                <div class="d-flex align-items-center">
                    <div class="text-left pr-1"><img src="static/robot_image.png" width="30" class="img1" /></div>
                    <div class="pr-2 pl-1">
                        <span class="name">ChatBotRetriever</span>
                        <p class="msg">`+ finalSpeach +`</p>
                    </div>
                </div>
                `);

                table_content = $("#answers-tbody");

                table_content.empty();

                response.answers.forEach(element => {

                    score = element.score.toFixed(3);

                    console.log(score)

                    table_content.append(`
                    <tr>
                        <th scope="row">`+element.answer+`</th>
                        <td>`+score+`</td>
                    </tr>
                    `)

                });


            },
            error: function(error){

                $('#ask-button').prop('disabled', false);

                $("#writing-notif").remove()

                $("#chat-window").append(`
                <div class="d-flex align-items-center">
                    <div class="text-left pr-1"><img src="static/robot_image.png" width="30" class="img1" /></div>
                    <div class="pr-2 pl-1">
                        <span class="name">Serapf</span>
                        <p class="msg">Sorry i couldn't answer, my silly programmer did something wrong, try it latter</p>
                    </div>
                </div>
                `);

                console.log("estamos por errr" + error);
            }
        });
    }

    $("#answer-form").submit(function(event){

        data = $('form').serializeArray()

        msg = data[0].value

        $("#chat-window").append(`
        <div class="d-flex align-items-center text-right justify-content-end ">
            <div class="pr-2">
                <span class="name">User</span>
                <p class="msg">`+ msg +`</p>
            </div>
            <div><img src="static/user_image.png" width="30" class="img1" /></div>
        </div>
        `)

        $("#chat-window").append(`
        <div id = "writing-notif" class="d-flex align-items-center">
            <div class="text-left pr-1"><img src="static/robot_image.png" width="30" class="img1" /></div>
            <div class="pr-2 pl-1">
                <span class="name">Serapf</span>
                <p class="msg"><i class="fa-solid fa-ellipsis"></i></p>
            </div>
        </div>
        `);

        $('#ask-button').prop('disabled', true);

        event.preventDefault();
        ajax_answer();

        $("#question-window").val("")
    });


});
