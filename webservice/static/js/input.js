/*
 * File: input.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Attaches handlers and callbacks for input related events.
 */

//$("#").submit(function(event) {
//
//});

$("#reboot_system").click(function(event) {
    console.log("Rebooting system ...");
    API.rebootSystem(function() {
    });
});

$("#restart_service").click(function(event) {
    console.log("Restarting doorbell service ...");
    API.restartService(function() {
    });
});

