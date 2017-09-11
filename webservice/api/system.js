/*
 * File: system.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Provides an API for system-level commands such as rebooting and 
 * restarting services.
 */

// Module includes
var exec = require("child_process").exec;
var express = require("express");
var path = require("path");
var httpCodes = require("http-codes");

// Variables
var parentDir = path.resolve(__dirname, "..");
var log = require(path.resolve(parentDir, "include", "log"));
var config = require(path.resolve(parentDir, "include", "config"));
var router = express.Router();

router.use(function(req, res, next) {
    next();
});

/******************************************************************************
 * Public API
 *****************************************************************************/

/**
 * Reboots the platform.
 *
 * GET
 *
 * /api/system/reboot
 */
router.get("/reboot", function(req, res, next) {
    log.debug("GET /api/system/reboot");
    exec("shutdown -r now", function(err, stdout, stderr) {
        if (err) {
            return res.status(httpCodes.INTERNAL_SERVER_ERROR).send();
        }
        return res.status(httpCodes.OK).send();
    });
});

/**
 * Restarts the background hardware worker service.
 *
 * GET
 *
 * /api/system/restart_service
 */
router.get("/restart_service", function(req, res, next) {
    log.debug("GET /api/system/restart_service");
    exec("systemctl restart doorbell", function(err, stdout, stderr) {
        if (err) {
            return res.status(httpCodes.INTERNAL_SERVER_ERROR).send();
        }
        return res.status(httpCodes.OK).send();
    });
});

module.exports = router;
