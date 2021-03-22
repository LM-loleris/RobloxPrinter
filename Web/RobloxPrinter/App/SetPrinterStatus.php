<?php
    include '../Common/get_printer_status.php';

    function HandleRequest(&$db, &$input, &$response){
        $stmt = $db->prepare("UPDATE `PrinterStatus` SET `LastActive`=?,`IsMaintenance`=?,`IsPaperLow`=?,`IsOn`=?,`IpLocal`=?,`IpPublic`=? WHERE 1");
        $stmt->execute([time(), $input["IsMaintenance"], $input["IsPaperLow"], $input["IsOn"], $input["IpLocal"], $input["IpPublic"]]);

        // Return printer status:
        $status = GetPrinterStatus($db);
        foreach ($status as $key => $value) {
            $response[$key] = $value;
        }
    }
?>