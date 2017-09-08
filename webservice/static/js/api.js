/*
 * File: api.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Defines available API functions provided by the Tofu service.
 */

var API = (function() {
    'use strict';

    function rebootSystem(callback) {
        Network.get(
            "/api/system/reboot",
            {},
            callback
        );
    }

    function restartService(callback) {
        Network.get(
            "/api/system/restart",
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
        rebootSystem: rebootSystem,
        restartService: restartService,
        validateResponse: validateResponse
    };

    return api;
}());

