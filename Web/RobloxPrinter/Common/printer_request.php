<?php
    function IsUserBanned(&$db, $user_id) {
        $stmt = $db->prepare("SELECT * FROM `BannedUsers` WHERE UserId = ? LIMIT 1");
        $stmt->execute([$user_id]);
        $banned_user_info = $stmt->fetch();

        return $banned_user_info != NULL;
    }

    function MakePrinterRequest(&$db, $request_type, $params) {

        $param_definitions = [
            "Admin" => [
                "AdminId",
                "Username",
                "Type",
                "Param",
            ],
            "Special" => [
                "UserId",
                "Username",
                "Type",
                "Param",
                "RobuxPaid",
            ],
            "Image" => [
                "UserId",
                "Username",
                "ImageId",
                "RobuxPaid",
            ],
        ];

        $get_definitions = $param_definitions[$request_type];
        $params_array = array();
        $params_string = "";
        $params_placeholders = "";

        foreach ($get_definitions as $param_name) {
            if (isset($params[$param_name]) == FALSE) {
                trigger_error("Missing param \"" . $param_name . "\" for request type \"" . $request_type . "\"");
            } else {
                array_push($params_array, $params[$param_name]);
                if ($params_string != "") {
                    $params_string .= ", ";
                    $params_placeholders .= ", ";
                }
                $params_string .= '`' . $param_name . '`';
                $params_placeholders .= "?";
            }
        }

        if ($request_type == "Admin") {

            // Checking admin ID:
            $stmt = $db->prepare("SELECT * FROM `Admins` WHERE Id = ?");
            $stmt->execute([$params["AdminId"]]);
            $admin_info = $stmt->fetch();

            if ($admin_info == NULL) {
                trigger_error("Admin with ID \"" . $params["AdminId"] . "\" was not defined");
            }

            // Storing request:
            array_unshift($params_array, $admin_info["UserId"]);
            $params_placeholders .= ", ?";
            $stmt = $db->prepare("INSERT INTO `AdminRequests`(`UserId`, ". $params_string .") VALUES (" . $params_placeholders . ")");
            $stmt->execute($params_array);
            echo "Admin request added\n";
            echo "INSERT INTO `AdminRequests`(`UserId`, ". $params_string .") VALUES (" . $params_placeholders . ")";

        } elseif ($request_type == "Special") {

            // Checking banned users:
            if (IsUserBanned($db, $params["UserId"]) == TRUE) {
                return; // This user is banned
            }

            // Storing request:
            $stmt = $db->prepare("INSERT INTO `SpecialRequests`(". $params_string .") VALUES (" . $params_placeholders . ")");
            $stmt->execute($params_array);

        } elseif ($request_type == "Image") {

            // Checking banned users:
            if (IsUserBanned($db, $params["UserId"]) == TRUE) {
                return; // This user is banned
            }

            // Checking banned images:
            $stmt = $db->prepare("SELECT * FROM `BannedImages` WHERE ImageId = ? LIMIT 1");
            $stmt->execute([$params["ImageId"]]);
            $banned_image_info = $stmt->fetch();

            if ($banned_image_info != NULL) {
                return; // This image is banned
            }

            // Storing request:
            $stmt = $db->prepare("INSERT INTO `ImageRequests`(". $params_string .") VALUES (" . $params_placeholders . ")");
            $stmt->execute($params_array);

        }

    }
?>