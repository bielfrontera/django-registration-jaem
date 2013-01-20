$(function() {
    $('#id_date_registration').datepicker({ format: 'dd/mm/yyyy',weekStart: 1 });
    $('#id_date_paid').datepicker({ format: 'dd/mm/yyyy', weekStart: 1 });
    // load_location();


    var btnSendmailClicked = false;
    $('#btn-sendmail').click(function() {
        if (!btnSendmailClicked)
            $.getJSON( URL_MAILTEMPLATE_LOOKUP, function(data) {
                var items = [];
                var itemsDiv = [];
                $.each(data, function(key, val) {
                    linkmail=LINKMAIL;
                    new_link=linkmail.replace("None",val.value);
                    items.push('<li><a href="#' + val.value + '" role="button" data-toggle="modal" >' + val.label + '</a></li>');
                    itemsDiv.push('<div id="'+ val.value +'" class="modal hide fade" tabindex="-1" role="dialog"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="myModalLabel">' + TRADUCTION.sendmail + '</h3></div>'+
                    '<div class="modal-body"><h5>' + TRADUCTION.message_about_to_send +'<br />&nbsp;&nbsp;'+ val.label +'</h5></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true">' + TRADUCTION.close +'</button><button class="btn btn-primary btn-mail" formaction="'+new_link+
                    '" data-loading-text="'+TRADUCTION.sending +'..." >'+ TRADUCTION.sendmail + '</button></div></div>');
               });
                $('<ul/>', {
                    'class': 'dropdown-menu',
                    html: items.join('')
                }).appendTo('#list-sendmail');
                $(itemsDiv.join('')).appendTo('#list-sendmail');
                inicialitzaBotonsMail();
             });
        btnSendmailClicked = true;
    });

    function inicialitzaBotonsMail(){
        $('.btn-mail')
            .click(function () {
                var btn = $(this)
                btn.button('loading')
                $.ajax({
                    url: btn.attr('formaction'),
                    success: function(data) {
                        $('.modal-body h5').html(data);
                    }
                });
         });
    }
    inicialitzaBotonsMail();
});
