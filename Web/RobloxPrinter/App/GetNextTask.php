<?php
    include '../Common/get_printer_status.php';

    function HandleRequest(&$db, &$input, &$response){

        // PrinterStaus IsPrintingActive must be TRUE to handle tasks:
        $status = GetPrinterStatus($db);
        if ($status["IsPrintingActive"] == FALSE) {
            return;
        }

        // Request types by descending priority:
        $request_tables = [
            ["Name" => "AdminRequests", "Type" => "Admin"],
            ["Name" => "SpecialRequests", "Type" => "Special"],
            ["Name" => "ImageRequests", "Type" => "Image"],
        ];
        
        foreach ($request_tables as $table) {
            $stmt = $db->prepare("SELECT * FROM `" . $table["Name"] . "` WHERE IsPrinted = FALSE ORDER BY Id ASC LIMIT 1");
            $stmt->setFetchMode(PDO::FETCH_ASSOC);
            $stmt->execute();
            $task = $stmt->fetch();

            if ($task) {
                $response["TaskType"] = $table["Type"];
                $response["Task"] = $task;
                $response["ConfirmToken"] = ["Type" => $table["Type"], "Id" => $task["Id"]];
                return;
            }
        }

    }
?>