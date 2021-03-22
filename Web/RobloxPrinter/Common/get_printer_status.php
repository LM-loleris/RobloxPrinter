<?php
    $TIMEZONE = new DateTimeZone("Europe/Vilnius"); # Timezone to use for scheduling

    function _GetUnixOfDailyHour($hour) {
        global $TIMEZONE;
        $day_of_event = new DateTime('now', $TIMEZONE);
        if (intval($day_of_event->format('G')) >= $hour) {
            $day_of_event = new DateTime('tomorrow', $TIMEZONE);
        }
        $day_of_event->setTime($hour, 0);
        return $day_of_event->getTimestamp();
    }

    function GetPrinterStatus(&$db) {

        $ensure_boolean = [
            "IsMaintenance", "IsPaperLow", "IsOn", "IsPrintingActive", "IsStreamActive", "IsScheduled"
        ];

        // Create printer status dictionary out of PrinterStatus and PrinterConfig:
        $stmt = $db->query("SELECT * FROM `PrinterStatus` WHERE 1");
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $status = $stmt->fetch();
        $stmt = $db->query("SELECT * FROM `PrinterConfig` WHERE 1");
        $stmt->setFetchMode(PDO::FETCH_ASSOC);
        $config = $stmt->fetch();
        $result = array_merge($status, $config);

        // Add IsActive member to parse time in this servers timezone:
        $result["IsActive"] = time() - $result["LastActive"] < 8;

        // Add info about the working schedule:
        $next_start_time = _GetUnixOfDailyHour(intval($result["ScheduledStartTime"]));
        $next_stop_time = _GetUnixOfDailyHour(intval($result["ScheduledStopTime"]));
        $result["NextStartTime"] = $next_start_time;
        $result["NextStopTime"] = $next_stop_time;

        foreach ($ensure_boolean as $param) {
            $result[$param] = $result[$param] == TRUE;
        }

        return $result;
    }
?>