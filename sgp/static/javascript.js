function procura() {


    
    var projetos_lista = JSON.parse($("#dataa"));

    // var projetos_lista = JSON.parse('{{ projetos_lista | safe}}');
    $("#busca").autocomplete({
        source: projetos_lista,
        minLength: 1,
        autoFocus: true,

        select: function (event, ui) {
            event.preventDefault();
            $("#form").show();

            $('#busca').val(ui.item.label);
            //$("input[name='id']").val(ui.item.id);
            $("input[name='cliente_nome']").val(ui.item.value.cliente_nome);
            $("input[name='telefone']").val(ui.item.value.telefone);
            $("input[name='endereço']").val(ui.item.value.endereço);
            $("input[name='data_entrada']").val(ui.item.value.data_entrada);
            $("input[name='data_medição']").val(ui.item.value.data_medição);
            $("input[name='data_final']").val(ui.item.value.data_final);
            $("input[name='fotos_medição']").val(ui.item.value.fotos_medição);
            //$("input[name='promobe_arquivos']").val(ui.item.value.promobe_arquivos);
            //$("input[name='renders_jpg']").val(ui.item.value.renders_jpg);
            //$("input[name='medidas_pdf']").val(ui.item.value.medidas_pdf);
            $("input[name='data_apresentação']").val(ui.item.value.data_apresentação);
            $("input[name='aprovação']").val(ui.item.value.aprovação);
            $("input[name='orçamento']").val(ui.item.value.orçamento);
            $("input[name='pagamento']").val(ui.item.value.pagamento);
            $("#ambientes").val(ui.item.value.ambientes[0])
            for (var i = 1; i < ui.item.value.ambientes.length; i++) {
                console.log(ui.item.value.ambientes[i]);
                $("#ambientes_ul").append(
                    $('<li></li>').append(
                        $('<input name="ambientes" type="text" placeholder="ambientes" value="">')
                            .val(ui.item.value.ambientes[i])
                    )
                );
            };
            //$("input[name='ambientes']").val(ui.item.value.ambientes[0].comodo);


        },
        focus: function (event, ui) {
            event.preventDefault();

        },
        change: function (event, ui) {
            event.preventDefault();
        },
    }).autocomplete("instance")._renderItem = function (ul, item) {
        return $("<li class=\"list-group-item\" >")
            .append(item.label)
            .appendTo(ul);
    };


    $("button>i").click(function () {
        this.parentElement.parentElement.firstElementChild.disabled = false;
        this.after($('<i class="bi bi-check-square"></i>'));
    })


}