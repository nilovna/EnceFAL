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
    
    get_exemplaire = function (event) {

        var identifiant_regex = /id_exemplaires-(\d+)-identifiant/;

        identifiant = django.jQuery('#' + event.target.id).val();
        if (identifiant.length == 0){
            return;
        } 

        nb = identifiant_regex.exec(event.target.id);
        nb = nb[1];

        url = "/exemplaire/?identifiant=" + identifiant + '&nb=' + this.nb;
        django.jQuery.get(url, function(response, status){
            if (status == "success"){

                django.jQuery('#id_exemplaires-' + response.nb + '-titre').val(response.titre);
                django.jQuery('#id_exemplaires-' + response.nb + '-auteur').val(response.auteur);
                django.jQuery('#id_exemplaires-' + response.nb + '-isbn').val(response.isbn);
                django.jQuery('#id_exemplaires-' + response.nb + '-prix').val(response.prix);

            }

        });

    }

    get_isbn = function (event) {

        var isbn_regex = /id_exemplaires-(\d+)-isbn/;

        code = django.jQuery('#' + event.target.id).val();
        if (code.length == 0){
            return;
        } 

        nb = isbn_regex.exec(event.target.id);
        nb = nb[1];

        url = "/livre/?isbn=" + code + '&nb=' + this.nb;
        django.jQuery.get(url, function(response, status){
            if (status == "success"){

                django.jQuery('#id_exemplaires-' + response.nb + '-titre').val(response.titre);
                django.jQuery('#id_exemplaires-' + response.nb + '-auteur').val(response.auteur);
                django.jQuery('#id_exemplaires-' + response.nb + '-prix').focus();

            }

        });

    }

});
