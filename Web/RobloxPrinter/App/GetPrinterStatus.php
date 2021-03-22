<?php
    include '../Common/get_printer_status.php';

    function HandleRequest(&$db, &$input, &$response){
        // Return printer status:
        $status = GetPrinterStatus($db);
        foreach ($status as $key => $value) {
            $response[$key] = $value;
        }
    }
?>