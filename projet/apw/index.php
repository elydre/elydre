<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🐑 Pattern Library</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <script>
        function submitForm() {
            var needles = document.getElementById("needles").value;
            var type = document.getElementById("type").value;
            var wool = document.getElementById("wool").value;
            var collec = document.getElementById("collec").value;
            var tmp_href = "?needles=" + needles;
            if (type != 0) {
                tmp_href += "&type=" + type;
            }
            if (wool != 0) {
                tmp_href += "&wool=" + wool;
            }
            if (collec != 0) {
                tmp_href += "&collec=" + collec;
            }
            window.location.href = tmp_href;
        }

        function getQueryParam(param) {
            var urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(param);
        }

        document.addEventListener("DOMContentLoaded", function() {
            var selectedValue;

            selectedValue = getQueryParam("needles");
            if (selectedValue) {
                document.getElementById("needles").value = selectedValue;
            }

            selectedValue = getQueryParam("type");
            if (selectedValue) {
                document.getElementById("type").value = selectedValue;
            }

            selectedValue = getQueryParam("wool");
            if (selectedValue) {
                document.getElementById("wool").value = selectedValue;
            }

            selectedValue = getQueryParam("collec");
            if (selectedValue) {
                document.getElementById("collec").value = selectedValue;
            }
        });
    </script>
    <body>
        <table><tbody>
            <tr>
                <td>       
                <select name="needles" id="needles">
                    <option value="all">All Needles</option>
<?php

// Decode the JSON file
$json_data = json_decode(file_get_contents("types.json"), true);

// display the array
foreach ($json_data["needles"] as $value) {
    echo "<option value=\"$value\">$value</option>";
}

?>
                </select>
            </td>
            <td><div class="select-container">
                <select name="type" id="type">
                    <option value="0">All Types</option>
                    <option value="1">Cardigan</option>
                    <option value="2">Débardeur</option>
                    <option value="3">Pull</option>
                    <option value="4">Veste longue</option>
                    <option value="5">Top été</option>
                    <option value="6">Châle</option>
                    <option value="7">Col</option>
                    <option value="8">Gants</option>
                    <option value="9">Chaussettes</option>
                    <option value="10">Bonnet</option>
                </select>
            </div></td>
            <td>
                <select name="wool" id="wool">
                    <option value="0">All Wools</option>
<?php

foreach ($json_data["wools"] as $value) {
    echo "<option value=\"$value\">" . str_replace("_", " ", $value) . "</option>";
}

?>
                </select>
            </td>
            <td>
                <select name="collec" id="collec">
                    <option value="0">All Collections</option>
                    <option value="1">Extra</option>
<?php

foreach ($json_data["collec"] as $value) {
    echo "<option value=\"$value\">" . str_replace("_", " ", $value) . "</option>";
}

?>
                </select>
            <td>
            <button onclick="submitForm()">Search!</button>
            </td>
        </tbody></table></tr>
        <?php

if (!isset($_GET["needles"])) {
    $_GET["needles"] = "all";
}

if (!isset($_GET["type"])) {
    $_GET["type"] = 0;
}

if (!isset($_GET["wool"])) {
    $_GET["wool"] = "0";
}

if (!isset($_GET["collec"])) {
    $_GET["collec"] = "0";
}

$needle = $_GET["needles"];

$TAB_LINE_COUNT = 6; // const
$count = 0;

// Decode the JSON file
$json_data = json_decode(file_get_contents("data.json"), true);

echo "<table><tbody><tr>";

for ($i = 0; $i < count($json_data); $i++) {
    if ($json_data[$i]["needles"] != $needle && $needle != "all") {
        continue;
    }
    if ($json_data[$i]["type"] != $_GET["type"] && $_GET["type"] != 0) {
        continue;
    }
    if ($_GET["wool"] != "0") {
        if ($json_data[$i]["wool"] == null) {
            continue;
        }
        if (!in_array($_GET["wool"], $json_data[$i]["wool"])) {
            continue;
        }
    }
    if ($_GET["collec"] != "0") {
        if ($json_data[$i]["collec"] == null) {
            if ($_GET["collec"] != "1") {
                continue;
            }
        } else if (!in_array($_GET["collec"], $json_data[$i]["collec"])) {
            continue;
        }
    }

    if ($count % $TAB_LINE_COUNT == 0 && $count != 0) {
        echo "</tr><tr>";
    }

    $count++;
    echo "<td>";
    if ($json_data[$i]["url"] != null) {
        echo "<a href='" . $json_data[$i]["url"] . "'>";
    }

    if ($json_data[$i]["image"] != null) {
        echo "<div class='image-container'><img src='" . $json_data[$i]["image"] . "'></div><br>";
    } else {
        echo "<div class='image-container'><img src='default.png'></div><br>";
    }

    if ($json_data[$i]["url"] != null) {
        echo "</a>";
    }
    echo "<b>" . $json_data[$i]["name"] . "</b><br>" . $json_data[$i]["author"];
    echo " (" . $json_data[$i]["needles"] . ")";
    if ($json_data[$i]["collec"] != null) {
        foreach ($json_data[$i]["collec"] as $value) {
            echo "<br><a href=?collec=$value><i>" . str_replace("_", " ", $value) . "</i></a>";
        }
    }
    echo "</td>";
}

// complete the table
if ($count % $TAB_LINE_COUNT != 0) {
    for ($i = 0; $i < $TAB_LINE_COUNT - $count % $TAB_LINE_COUNT; $i++) {
        echo "<td>
        <div class='image-container'><img src='empty.png'></div><br>
        </td>";
    }
}

echo "</tr></tbody></table>";

?>
    </body>
</html>
