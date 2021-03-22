<?php
    include '../Common/printer_request.php';

    function HandleRequest(&$db, &$input, &$response){

        $request_types = [
            "Special" => TRUE,
            "Image" => TRUE,
            "Admin" => TRUE,
        ];

        $request_type = $input["TaskType"];
        $request_params = $input["TaskParams"];

        if (isset($request_params) == TRUE) {
            if ($request_types[$request_type] == TRUE) {
                try {
                    MakePrinterRequest($db, $request_type,  $request_params);
                } catch (Exception $e) {
                    $response["Error"] = "BadRequestParams";
                }
            } else {
                $response["Error"] = "BadRequestType";
            }
        }

    }
?>