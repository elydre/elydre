<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Accueil</title>
        <?php
        if ($_SERVER['REQUEST_URI'] == '/index.php'){
            echo '<link rel="stylesheet" href="css/sombre.css">';
        }
        else if ($_SERVER['REQUEST_URI'] == '/index.php?claire'){
            echo '<link rel="stylesheet" href="css/claire.css">';
        }
        ?>
    </head>
    <body>
        <table class="maintab">
            <td class="maintab">
                <h1> La Nouvelle-Calédonie </h1>
                <ul class="menu">
                    <?php
                        if ($_SERVER['REQUEST_URI'] == '/index.php'){
                            echo '<li> <a href="index.php?claire">claire</a>';
                            echo '<li> <a href="admin.php">admin</a> </li>';
                        }
                        else if ($_SERVER['REQUEST_URI'] == '/index.php?claire'){
                            echo '<li> <a href="index.php">sombre</a>';
                            echo '<li> <a href="admin.php?claire">admin</a> </li>';
                        }
                    ?>
                </ul>
                <img height=50 src="photo/drapeau.svg" alt="Nouvelle-Calédonie">
                <br><br>
                La Nouvelle-Calédonie est une collectivité d'outre-mer française composée d'un ensemble d'îles et d'archipels d'Océanie,
                situés en mer de Corail et dans l'océan Pacifique Sud.
                L'île principale est la Grande Terre, longue de 400 km et comptant 64 km en sa plus grande largeur.
                Proche de son extrémité sud,
                l'aire urbaine du chef-lieu Nouméa compte les deux tiers des habitants du territoire,
                et se situe à 1 407 km à l'est-nord-est de l'Australie,
                à 1 477 km au nord-nord-ouest de la Nouvelle-Zélande,
                et à 130 km au nord du tropique du Capricorne;
                le Vanuatu se trouve à 539 km au nord-nord-est.

                <br><br>
                <table style="margin: 1 1em 1 1em;" align="center">
                    <caption><b>Communautés d'appartenance aux recensements</b>
                    </caption>
                    <tbody><tr>
                    <th colspan="2">Communauté</th>
                    <th>2009</th>
                    <th>2014</th>
                    <th>2019
                    </th></tr>
                    <tr>
                    <td colspan="2">Kanak</a></td>
                    <td align="center">99&#160;078 <small>(40,3&#160;%)</small></td>
                    <td align="center">104&#160;958 <small>(39,1&#160;%)</small></td>
                    <td align="center">111&#160;856 <small>(41,2&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Européenne</td>
                    <td align="center">71&#160;721 <small>(29,2&#160;%)</small></td>
                    <td align="center">73&#160;199 <small>(27,2&#160;%)</small></td>
                    <td align="center">65&#160;488 <small>(24,1&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Plusieurs communautés</td>
                    <td align="center">20&#160;398 <small>(8,3&#160;%)</small></td>
                    <td align="center">23&#160;007 <small>(8,6&#160;%)</small></td>
                    <td align="center">30&#160;758 <small>(11,3&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Wallisienne, Futunienne</td>
                    <td align="center">21&#160;262 <small>(8,7&#160;%)</small></td>
                    <td align="center">21&#160;926 <small>(8,2&#160;%)</small></td>
                    <td align="center">22&#160;520 <small>(8,3&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td rowspan="3">Asiatique</td>
                    <td>Indonésienne</td>
                    <td align="center">3&#160;985 <small>(1,6&#160;%)</small></td>
                    <td align="center">3&#160;859 <small>(1,4&#160;%)</small></td>
                    <td align="center">3&#160;786 <small>(1,4&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td>Vietnamienne</td>
                    <td align="center">2&#160;357 <small>(1,0&#160;%)</small></td>
                    <td align="center">2&#160;506 <small>(0,9&#160;%)</small></td>
                    <td align="center">2&#160;230 <small>(0,8&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td>Autre asiatique</td>
                    <td align="center">1&#160;857 <small>(0,8&#160;%)</small></td>
                    <td align="center">1&#160;177 <small>(0,4&#160;%)</small></td>
                    <td align="center">1&#160;181 <small>(0,4&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Tahitienne</td>
                    <td align="center">4&#160;985 <small>(2,0&#160;%)</small></td>
                    <td align="center">5&#160;608 <small>(2,1&#160;%)</small></td>
                    <td align="center">5&#160;366 <small>(2,0&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Ni-Vanuatu</td>
                    <td align="center">2&#160;327 <small>(0,9&#160;%)</small></td>
                    <td align="center">2&#160;568 <small>(1,0&#160;%)</small></td>
                    <td align="center">2&#160;313 <small>(0,9&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td rowspan="2">Autre</td>
                    <td>Divers<span></a></sup></td>
                    <td align="center">2&#160;566 <small>(1,0&#160;%)</small></td>
                    <td align="center">3&#160;428 <small>(1,3&#160;%)</small></td>
                    <td align="center">5&#160;610 <small>(2,1&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td>Calédonien(ne)<span></a></sup></td>
                    <td align="center">12&#160;177 <small>(5,0&#160;%)</small></td>
                    <td align="center">19&#160;927 <small>(7,4&#160;%)</small></td>
                    <td rowspan="2" align="center">20&#160;299<span></a></sup> <small>(7,5&#160;%)</small>
                    </td></tr>
                    <tr>
                    <td colspan="2">Non déclarée<span></a></sup></td>
                    <td align="center">2&#160;867 <small>(1,2&#160;%)</small></td>
                    <td align="center">6&#160;604 <small>(2,5&#160;%)</small>
                    </td></tr></tbody></table>
            </td>        
        </table>
    </body>
</html>