<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload File</title>
</head>
<body>
    <a href="index.php">Retour à la page d'accueil</a><br>
    <a href="crawl.log">Voir le fichier de log</a><br>
    <br>
    <form action="dev.php" method="post" enctype="multipart/form-data">
        <input type="file" name="file" id="fileInput">
        <button type="submit">Upload</button>
    </form>
    <br>
</body>
</html>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Vérifier si le fichier a été téléchargé sans erreur
    if (isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
        $fileTmpPath = $_FILES['file']['tmp_name'];
        $fileName = $_FILES['file']['name'];
        $fileSize = $_FILES['file']['size'];
        $fileExtension = pathinfo($fileName, PATHINFO_EXTENSION);

        // Liste des extensions autorisées
        $allowedfileExtensions = array('csv');

        if (in_array($fileExtension, $allowedfileExtensions)) {
            // verifier src.csv existe deja et le supprimer
            if (file_exists("src.csv")) {
                unlink("src.csv");
            }          

            if (move_uploaded_file($fileTmpPath, "src.csv")) {
                echo 'Le fichier a été téléchargé avec succès.<br>';
                exec("python3 crawl.py > crawl.log 2> err.log &");

                echo 'Traitement en cours...';
            } else {
                echo 'Il y a eu une erreur en déplaçant le fichier téléchargé.';
            }
        } else {
            echo 'Le fichier téléchargé n\'est pas un fichier CSV.';
        }
    } else {
        if (isset($_FILES['file'])) {
            echo 'Il y a eu une erreur lors du téléchargement du fichier.';
        } else {
            echo 'Aucun fichier n\'a été téléchargé.';
        }
    }
} else {
    echo 'Aucun fichier n\'a été téléchargé.';
}
?>
