$(function() {

    var addTaller = $('#add_taller');
    addTaller.remove();
    $('#id_taller').parent().append(addTaller);
    var removeTaller = $('#remove_taller');
    removeTaller.remove();
    $('#id_taller').parent().append(removeTaller);

    $('#id_taller').change(function() {
        var tallers_sel = $('#id_tallers').val().split(',');
        var taller_selected = $(this).find('option:selected')[0];
        var taller_index = tallers_sel.indexOf(taller_selected.value);
        if (taller_index > -1) {
            addTaller.hide();
            removeTaller.show();
        } else {
            removeTaller.hide();
            addTaller.show();
        }
    });

    addTaller.click(function() {
        var taller_selected = $('#id_taller option:selected')[0];

        // Add to hidden value
        var tallers_sel = $('#id_tallers').val();
        if (tallers_sel.length > 0)
            tallers_sel += ',';
        tallers_sel += taller_selected.value;
        $('#id_tallers').val(tallers_sel);

        // Add to visible list
        var position = tallers_sel.split(',').length;
        $("#tallers_selected").append('<li class="btn btn-info" id="taller' + taller_selected.value + '"><span class="preferencia_taller" >' + position + '</span> ' + $(taller_selected).text() + '</li>');

        // Hide add button and show remove button
        $(this).hide();
        removeTaller.show();
    });

    removeTaller.click(function() {
        var taller_selected = $('#id_taller option:selected')[0];

        // Remove item from hidden value
        var tallers_sel = $('#id_tallers').val().split(',');
        var taller_index = tallers_sel.indexOf(taller_selected.value);
        if (taller_index > -1) {
            tallers_sel.splice(taller_index, 1);
        }
        $('#id_tallers').val(tallers_sel.join(','));

        // Remove from visible list
        $("#tallers_selected").find('#taller' + taller_selected.value).remove();
        // Refresh visible list positions
        for (var i = 0, l = tallers_sel.length; i < l; i++) {
            $("#tallers_selected").find('#taller' + tallers_sel[i] + ' span.preferencia_taller').html(i + 1);
        }

        // Hide remove button and show add button
        $(this).hide();
        addTaller.show();
    });

    $("#tallers_selected").sortable({
        cursor: "move",
        stop: function(event, ui) {
            var tallers_sel = $(this).sortable( "toArray" );
            for (var i = 0, l = tallers_sel.length; i < l; i++) {
                $("#tallers_selected").find('#' + tallers_sel[i] + ' span.preferencia_taller').html(i + 1);
            }
            $('#id_tallers').val(tallers_sel.join(',').replace(/taller/g,''));
        }
    });

});