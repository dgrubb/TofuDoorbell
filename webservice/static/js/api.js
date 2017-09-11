/*
 * File: api.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Defines available API functions provided by the Tofu service.
 */

var API = (function() {
    'use strict';

    function deleteAudioFiles(files, callback) {
        Network.get(
            "/api/file/delete",
            {
                files: files
            },
            callback
        );
    }

    function getAudioList(callback) {
        Network.get(
            "/api/file/getlist",
            {},
            callback
        );
    }

    function rebootSystem(callback) {
        Network.get(
            "/api/system/reboot",
            {},
            callback
        );
    }

    function restartService(callback) {
        Network.get(
            "/api/system/restart_service",
            {},
            callback
        );
    }

    function validateResponse(resp, status) {
        if ("success" != status) {
            console.error(
                "Error validating response. AJAX status not successful: " +
                status
            );
            return false;
        }
        if (!resp || !(resp.responseJSON || resp.responseText)) {
            console.error("Error validating response, no message payload.");
            return false;
        }
        return true;
    }

    var api = {
        deleteAudioFiles: deleteAudioFiles,
        getAudioList: getAudioList,
        rebootSystem: rebootSystem,
        restartService: restartService,
        validateResponse: validateResponse
    };

    return api;
}());

