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

                $("#chat-window").append(`
                <div class="d-flex align-items-center">
                    <div class="text-left pr-1"><img src="https://img.icons8.com/color/40/000000/guest-female.png" width="30" class="img1" /></div>
                    <div class="pr-2 pl-1">
                        <span class="name">ChatBotRetriever</span>
                        <p class="msg">`+ finalSpeach +`</p>
                    </div>
                </div>
                `);

                table_content = $("#answers-tbody");

                table_content.empty();

                response.answers.forEach(element => {

                    table_content.append(`
                    <tr>
                        <th scope="row">`+element.answer+`</th>
                        <td>`+element.score+`</td>
                    </tr>
                    `)

                });


            },
            error: function(error){

                $('#ask-button').prop('disabled', false);

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
                <p class="msg">`+ data[0].value +`</p>
            </div>
            <div><img src="{{url_for('static',filename='user_image.png')}}" width="30" class="img1" /></div>
        </div>
        `)

        $('#ask-button').prop('disabled', true);

        event.preventDefault();
        ajax_answer();
    });


});
