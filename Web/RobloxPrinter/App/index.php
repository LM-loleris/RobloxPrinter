<?php
    // POST {Password = password, RequestType = request_type, ...}
    // Finds the php file with the name of "RequestType.php" and runs it

    include '../Common/db.php'; // $db, $APP_PASSWORD

    header('Content-Type: application/json');

    $InputRaw = file_get_contents("php://input");
    $Input = (strlen($InputRaw) > 0) ? json_decode($InputRaw, true) : NULL;

    if ($Input != NULL && json_last_error() == JSON_ERROR_NONE) {
        if ($Input["Password"] == $APP_PASSWORD) {

            $safe_request_string = preg_replace("/[^a-zA-Z0-9]+/", "", strval($Input["RequestType"]));
            $request_module_path = dirname(__FILE__) . "/" . $safe_request_string . ".php";

            if (file_exists($request_module_path) == TRUE) {
                include $request_module_path;
                $response = [];
                HandleRequest($db, $Input, $response);
                if (isset($response["Error"]) == FALSE) {
                    $response["Success"] = TRUE;
                }
                echo json_encode($response);
            } else {
                echo json_encode(["Error" => "BadRequest"], true);
            }

        } else {
            echo json_encode(["Error" => "AccessDenied"], true);
        }
    } else {
        echo json_encode(["Error" => "AccessDenied"], true);
    }
?>