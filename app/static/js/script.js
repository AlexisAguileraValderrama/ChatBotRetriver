$(document).ready(function () {

    function ajax_answer() {
        $.ajax({
            url: '/ajax-answer',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log("estamos aca " + response.finalSpeach);
                finalSpeach = response.finalSpeach;

                $("#chat-window").append(`
                <div class="d-flex align-items-center">
                    <div class="text-left pr-1"><img src="https://img.icons8.com/color/40/000000/guest-female.png" width="30" class="img1" /></div>
                    <div class="pr-2 pl-1">
                        <span class="name">Serapf</span>
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
                <span class="name">Dr. Hendrikson</span>
                <p class="msg">`+ data[0].value +`</p>
            </div>
            <div><img src="https://i.imgur.com/HpF4BFG.jpg" width="30" class="img1" /></div>
        </div>
        `)

        event.preventDefault();
        ajax_answer();
    });


});
