<%doc>
    input for estimation/invoice lines
</%doc>
<input class='input-mini' type='text' name="${field.name}" value="${cstruct}" ></input>
<script type="text/javascript">
    deform.addCallback(
        "${field.oid}",
        function (oid) {
            $('#' + oid + " input").blur(function(){
                var row = $(this).parent().parent();
                $(Facade).trigger("linechange", row);
                $(Facade).trigger("totalchange", row);
            }
        )});
</script>
