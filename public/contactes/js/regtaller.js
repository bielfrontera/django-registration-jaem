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
        if (taller_index > -1){
            addTaller.hide();
            removeTaller.show();
        }else{
            removeTaller.hide();
            addTaller.show();
        }
    });

    addTaller.click(function() {
        var taller_selected = $('#id_taller option:selected')[0];

        $("#tallers_selected").append('<li id="taller' + taller_selected.value + '">' + $(taller_selected).text() + '</li>');

        var tallers_sel = $('#id_tallers').val();
        if (tallers_sel.length > 0)
            tallers_sel += ',';
        tallers_sel += taller_selected.value;
        $('#id_tallers').val(tallers_sel);
        $(this).hide();
        removeTaller.show();
    });

    removeTaller.click(function() {
        var taller_selected = $('#id_taller option:selected')[0];
        $("#tallers_selected").find('#taller' + taller_selected.value).remove();
        var tallers_sel = $('#id_tallers').val().split(',');
        var taller_index = tallers_sel.indexOf(taller_selected.value);
        if (taller_index > -1){
            tallers_sel.splice(taller_index, 1);
        }
        $('#id_tallers').val(tallers_sel.join(','));
        $(this).hide();
        addTaller.show();
    });

});