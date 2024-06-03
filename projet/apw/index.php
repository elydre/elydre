<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>salut</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <script>
        function submitForm() {
            var needles = document.getElementById("needles").value;
            var type = document.getElementById("type").value;
            var wool = document.getElementById("wool").value;
            var tmp_href = "?needles=" + needles;
            if (type != 0) {
                tmp_href += "&type=" + type;
            }
            if (wool != 0) {
                tmp_href += "&wool=" + wool;
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
                var selectElement = document.getElementById("needles");
                selectElement.value = selectedValue;
            }

            selectedValue = getQueryParam("type");
            if (selectedValue) {
                var selectElement = document.getElementById("type");
                selectElement.value = selectedValue;
            }

            selectedValue = getQueryParam("wool");
            if (selectedValue) {
                var selectElement = document.getElementById("wool");
                selectElement.value = selectedValue;
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
// Read the JSON file
$json = file_get_contents("data.json");

// Decode the JSON file
$json_data = json_decode($json,true);

$suggestion = [];

for ($i = 0; $i < count($json_data); $i++) {
    // check if $json_data[$i]["needles"] is in the array $suggestion
    if (!in_array($json_data[$i]["needles"], $suggestion)) {
        // if not, add it to the array
        $suggestion[] = $json_data[$i]["needles"];
    }
}

// sort the array
sort($suggestion);

// display the array
foreach ($suggestion as $value) {
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
$suggestion = [];

for ($i = 0; $i < count($json_data); $i++) {
    if ($json_data[$i]["wool"] == null) {
        continue;
    }
    for ($j = 0; $j < count($json_data[$i]["wool"]); $j++) {
        if (!in_array($json_data[$i]["wool"][$j], $suggestion)) {
            $suggestion[] = $json_data[$i]["wool"][$j];
        }
    }
}

sort($suggestion);

foreach ($suggestion as $value) {
    // replace underscores with spaces
    $user_value = str_replace("_", " ", $value);
    echo "<option value=\"$value\">$user_value</option>";
}

?>
                </select>
            </td>
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

$needle = $_GET["needles"];

$TAB_LINE_COUNT = 6; // const
$count = 0;

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
    echo " (" . $json_data[$i]["needles"] . ")</td>";
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
