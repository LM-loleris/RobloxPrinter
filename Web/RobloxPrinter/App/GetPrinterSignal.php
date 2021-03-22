<?php
    function HandleRequest(&$db, &$input, &$response){
        $signals = [
            "RestartApp", "ShutdownApp", "ShutdownDevice"
        ];

        $stmt = $db->query("SELECT * FROM `PrinterSignal` WHERE 1");
        $signal_data = $stmt->fetch();

        $reset_query = "";
        $signal_received = NULL;

        foreach ($signals as $signal_name) {
            $reset_query .= (empty($reset_query) == TRUE ? "" : ", ") . "`" . $signal_name . "` = FALSE";
            if ($signal_received == NULL && $signal_data[$signal_name] == TRUE) {
                $signal_received = $signal_name;
            }
        }

        if ($signal_received != NULL) {
            $response["PrinterSignal"] = $signal_received;
            $db->query("UPDATE `PrinterSignal` SET " . $reset_query . " WHERE 1");
        }
    }
?>