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

$("#submit_delete").click(function(event) {
    console.log("Deleting files");
    var files = Content.getItemsMarkedForDeletion();
    if (!files || !files.length) {
        console.error("No file list retrieved");
        return false;
    }
    API.deleteAudioFiles(files, function(resp, status) {
        if (!API.validateResponse(resp, status)) {
            // TODO: handle error case
            return false;
        }
        Content.populateContent();
    });
});
