<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Accueil</title>
        <?php
            if ($_SERVER['REQUEST_URI'] == '/admin.php'){
                echo '<link rel="stylesheet" href="css/sombre.css">';
            }
            else if ($_SERVER['REQUEST_URI'] == '/admin.php?claire'){
                echo '<link rel="stylesheet" href="css/claire.css">';
            }
        ?>
    </head>
    <body align="center">
        <table class="maintab">
            <td class="maintab">
                <h1> La Nouvelle-Calédonie </h1>
                <ul class="menu">
                    <?php
                        if ($_SERVER['REQUEST_URI'] == '/admin.php'){
                            echo '<li> <a href="admin.php?claire">claire</a>';
                            echo '<li> <a href="index.php">accueil</a> </li>';
                        }
                        else if ($_SERVER['REQUEST_URI'] == '/admin.php?claire'){
                            echo '<li> <a href="admin.php">sombre</a> </li>';
                            echo '<li> <a href="index.php?claire">accueil</a> </li>';
                        }
                    ?>
  
                </ul>
                <img height=50 src="photo/drapeau.svg" alt="Nouvelle-Calédonie">
                <br><br>
                
                <form method="post">
                    mot de passe:
                    <input type="password" name="mdp" id="mdp">
                    <input type="submit" value="Valider">
                </form>
                <?php
                    $post = $_POST;
                    if (empty($post['mdp'])){
                        echo "entrer un mdp ^^";
                    }
                    else{
                        if ($post["mdp"] == "1234") {
                            header("Location: index.php");
                        }
                        else if ($post["mdp"] != ""){
                            header("Location: admin.php?claire");
                            echo "mot de passe incorrect le mode claire va vous aidé a trouver le mdp ^^";
                        }
                    }
                ?>
            </td>
        </table>
    </body>
</html>