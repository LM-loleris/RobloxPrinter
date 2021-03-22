<?php
    function HandleRequest(&$db, &$input, &$response){
        $signals = [
            "RestartApp", "ShutdownApp", "ShutdownDevice"
        ];

        $requested_signal = $input["PrinterSignal"];

        if (array_search($requested_signal, $signals) === FALSE) {
            $response["Error"] = "BadSignalType";
        } else {
            $db->query("UPDATE `PrinterSignal` SET `" . $requested_signal . "` = TRUE WHERE 1");
        }
    }
?>