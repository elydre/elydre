<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>PO - online</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <a style = "background-color: black;" href="classe.php">reset</a><br>
    <?php

    // fonction pour convertire un nombre en lettre
    function nb2lettre($nombre)
    {
        $liste = str_split("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
        if ($nombre > 61) {$nombre = 61;}
        return $liste[$nombre];
    }

    // fontion pour convertire une lettre en nombre
    function lettre2nb($lettre)
    {
        $liste = str_split("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz");
        return array_search($lettre, $liste);
    }

    // fonction pour editer $point
    function edit($point, $id)
    {
        $point = str_split($point);
        $point[$id] = nb2lettre(lettre2nb($point[$id]) + 1);

        $sortie = "";
        for ($i = 0; $i < count($point); $i++) {
            $sortie .= $point[$i];
        }
        return $sortie;
    }

    function get_color($pointtable)
    {
        if ($pointtable == "-1") {
            return "style = 'background-color: gray; color: white;'";
        }
        else if ($pointtable == "") {
            return "style = 'background-color: #003D2F; color: white;'";
        }
        else if ($pointtable == "1") {
            return "style = 'background-color: #0ed145; color: white;'";
        }
        else if ($pointtable == "2") {
            return "style = 'background-color: #ff8527; color: white;'";
        }
        else if ($pointtable == "3") {
            return "style = 'background-color: #db0502; color: white;'";
        }
        else if ($pointtable == "4") {
            return "style = 'background-color: #ff52b7; color: white;'";
        }
        else if ($pointtable == "5") {
            return "style = 'background-color: #a127ff; color: white;'";
        }
        else if ($pointtable == "6") {
            return "style = 'background-color: #010ec9; color: white;'";
        }
        else {
            return "style = 'background-color: #FFFFFF; color: black;'";
        }
    }

    // recuperation des données de l'url
    $point = $_SERVER['REQUEST_URI'];
    if (count(explode('?', $point)) == 1)
    {
        $lignes = 6;
        $colonnes = 7;
        $nbtabbles = $lignes * $colonnes;
        $point = str_repeat("0", $nbtabbles);
        header("Location: classe.php?$lignes&$colonnes&$point");
    }
    else
    {
        $args = explode('?', $point)[1];

        $point = explode('&',$args)[2];
        $lignes = explode('&',$args)[0];
        $colonnes = explode('&',$args)[1];

        $nbtabbles = $lignes * $colonnes;

        if (count(str_split($point)) != $nbtabbles)
        {
            $point = str_repeat("0", $nbtabbles);
            header("Location: classe.php?$lignes&$colonnes&$point");
        }
        
    }
    ?>

    <table>
        <?php
        $id = 0;
        for ($l = 0; $l < $lignes; $l++) {
            echo "<tr>";
            for ($c = 0; $c < $colonnes; $c++) {
                echo "<td>";
                $newpoint = edit($point, $id);
                $pointtable = lettre2nb(str_split($point)[$id]) - 1;
                $color = get_color($pointtable);
                if ($pointtable == -1)
                {
                    $pointtable = "";
                }
                else if ($pointtable == 60)
                {
                    $pointtable = "🎇";
                }
                echo "<a $color href='https://pf4.ddns.net/all/po/classe.php?$lignes&$colonnes&$newpoint'>$pointtable</a><br>";
                echo "</td>";
                $id++;
            }
            echo "</tr>";
        }

        ?>
    </table>
</body>