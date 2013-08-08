django.jQuery(document).ready(function () {

    django.jQuery('#id_code_carte_etudiante').change(function () {

        code = django.jQuery('#id_code_carte_etudiante').val();
        if (code.length == 0){
            return;
        } 

        url = "/vendeur/?code=" + code;
        django.jQuery.get(url, function(response, status){
            if (status == "success"){

                django.jQuery('#id_code_permanent').val(response.code_permanent);
                django.jQuery('#id_prenom').val(response.prenom);
                django.jQuery('#id_email').val(response.email);
                django.jQuery('#id_nom').val( response.nom);

            }
        });


    });

    function get_isbn(){

        code = django.jQuery('#id_exemplaires-' + this.nb + '-isbn').val();
        if (code.length == 0){
            return;
        } 

        url = "/livre/?isbn=" + code + '&nb=' + this.nb;
        django.jQuery.get(url, function(response, status){
            if (status == "success"){

                django.jQuery('#id_exemplaires-' + response.nb + '-titre').val(response.titre);
                django.jQuery('#id_exemplaires-' + response.nb + '-auteur').val(response.auteur);
                django.jQuery('#id_exemplaires-' + response.nb + '-prix').focus();

            }

        });

    }

    var i = 0;
    id = 'id_exemplaires-' + i + '-isbn';
    input = document.getElementById('id_exemplaires-' + i + '-isbn');

    while(input){
        input.onchange = get_isbn.bind({nb:i});
        i++;
        input = document.getElementById('id_exemplaires-' + i + '-isbn');
    }

});
