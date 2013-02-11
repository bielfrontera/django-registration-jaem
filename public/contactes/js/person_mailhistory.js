$(function() {

    var tabMailHistoryClicked = false;

    function formatDate(isodate){
        try{
            var d = new Date(isodate);
            var date_day = d.getDate();
            var date_month = d.getMonth();
            date_month++;
            var date_year = d.getFullYear();
            return date_day + "/" + date_month + "/" + date_year;
        } catch(err) {
            return isodate;
        }

    }

    function getMailHistory(){
        tabMailHistoryClicked = true;
        $('#mail_history_loading').show();
        $('#mail_history_error').hide();
        $.getJSON( URL_GET_MAILHISTORY, function(data) {
            if (data.error){
                $('#mail_history_error span').html(data.error_message);
                $('#mail_history_error').show();
            }else{
                var messages = [];
                $.each(data.messages, function(key, val) {
                    mail_date = '<span class="mail_date">' + formatDate(val.date) + '</span> ';
                    mail_from = '<span class="mail_from">' + val.from + '</span> ';
                    mail_subject = '<span class="mail_subject">' + val.subject + '</span> ';
                    mail_body = '<span class="mail_body">' + val.body + '</span> ';
                    messages.push('<li>' + mail_date + mail_from + mail_subject + mail_body + '</li>');
                });
                $('<ul/>', {
                    html: messages.join('')
                }).appendTo('#mail_history_list');
           }
        })
        .complete(function(){ $("#mail_history_loading").hide();});
    }

    $('#mail_history_tab').click(function() {
        if (!tabMailHistoryClicked)
            getMailHistory();
    });
});
