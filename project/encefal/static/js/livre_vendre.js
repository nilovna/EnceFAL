$(document).ready(function () {

    document.getElementById('id_code_carte_etudiante').onchange = function () {

        code = document.getElementById('id_code_carte_etudiante').value;

        var query = new XMLHttpRequest();
        query.onreadystatechange=function(){
            if (query.readyState == 4 && query.status != 404){
                infos = JSON.parse(query.responseText);

                document.getElementById('id_code_permanent').value = JSON.parse(query.responseText).code_permanent;
                document.getElementById('id_prenom').value = JSON.parse(query.responseText).prenom;
                document.getElementById('id_email').value = JSON.parse(query.responseText).email;
                document.getElementById('id_nom').value = JSON.parse(query.responseText).nom;

            } else if (query.readyState == 4 && query.status == 404){
                // Ecrire un message d'erreur pour que l'employee entre les infos
            }
        };
        url = "../vendeur/?code=" + code;
        query.open("GET",url,true);
        query.send();

    };

});
