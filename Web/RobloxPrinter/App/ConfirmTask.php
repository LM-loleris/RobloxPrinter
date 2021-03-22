<?php
    function HandleRequest(&$db, &$input, &$response){

        $request_tables = [
            "Admin" => "AdminRequests",
            "Special" => "SpecialRequests",
            "Image" => "ImageRequests",
        ];

        $confirm_token = $input["ConfirmToken"];

        if (isset($confirm_token) == TRUE) {
            $table_name = $request_tables[$confirm_token["Type"]];
            if (isset($table_name) == TRUE) {

                $stmt = $db->prepare("UPDATE `" . $table_name ."` SET `IsPrinted` = TRUE WHERE Id=?");
                $stmt->execute([$confirm_token["Id"]]);

            }
        }

    }
?>