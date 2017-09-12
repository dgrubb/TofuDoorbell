/*
 * File: content.js
 * Author: dgrubb
 * Date: 09/11/2017
 *
 * Functionality for fetching and parsing the local content.
 */

var Content = (function() {
    'use strict';

    const tableTemplate = "<thead><tr>" +
        "<th>#</th>" +
        "<th>Name</th>" +
        "<th>Select</th>" +
        "</tr></thead>" +
        "<tbody></tbody>";

    var deleteItems = [];

    function populateContent() {
        API.getAudiolist(function(resp, status) {
            if (!API.validateResponse(resp, status)) {
                // TODO: handle error case
                return false;
            }
            if (!resp.responseJSON || !Array.isArray(resp.responseJSON)) {
                // These are not the droids we're looking for
                return false;
            }

        });
    }

    function clearTable() {
        $("#file_list_table thead").remove();
        $("#file_list_table tbody").remove();
    }

    function drawTable(audioList) {
        clearTable();
        $("#file_list_table").append($(tableTemplate));
        var $audioListTable = $("#file_list_table tbody");
        audioList.forEach(function(item, idx) {
            $audioListTable.append(newAudioTableEntry(item, idx));
        });
    }

    function newAudioTableEntry(audioItem, idx) {
        var $audioItem = $("<tr>");
        $audioItem.append($("<td>").text(idx));
        $audioItem.append($("<td>").text(item.fileName));
        $audioItem.append($("td")
            .append($(
                "<input type=\"checkbox\" id=\"check_" +
                item.fileName +
                "\"></input>"
            ).change(function() {
                Content.markForDeletion(
                    this.id.replace("check_", ""),
                    this.checked
                );
            }))
        );
        return $audioItem;
    }

    function markForDeletion(fileName, mark) {
        if (mark) {
            if (deleteItems.includes(fileName)) {
                return;
            }
            deleteItems.append(fileName);
        } else {
            deleteItems = _.without(deleteItems, fileName);
        }
    }

    function getItemsMarkedForDeletion() {
        return deleteItems;
    }

    var api = {
        getItemsMarkedForDeletion: getItemsMarkedForDeletion,
        markForDeletion: markForDeletion,
        populateContent: populateContent
    };

    return api;
}());

