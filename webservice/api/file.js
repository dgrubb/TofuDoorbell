/*
 * File: file.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Provides an API for managing audio samples.
 */

// Module includes
var exec = require("child_process").exec;
var fs = require("fs");
var express = require("express");
var path = require("path");
var httpCodes = require("http-codes");
var formidable = require("formidable");

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
 * Retrieves a list of installed audio samples.
 *
 * GET
 *
 * /api/file/getlist
 */
router.get("/getlist", function(req, res, next) {
    log.debug("GET /api/file/getlist");
    var files = [];
    fs.readdir(config.audioSamplesPath, function(err, list) {
        if (err) {
            return res.status(httpCodes.INTERNAL_SERVER_ERROR).send();
        }
        for (var i in list) {
            if (path.extname(list[i]) === ".mp3") {
                files.push(list[i]);
            }
        }
        return res.status(httpCodes.OK).send(files);
    });
});

/**
 * Deletes specified audio samples.
 *
 * GET
 *
 * /api/file/delete
 */
router.post("/delete", function(req, res, next) {
    log.debug("GET /api/file/delete");
    if (!req.body || !req.body.files || !Array.isArray(req.body.files)) {
        log.error("Delete requested without file arguments");
        return res.status(httpCodes.BAD_REQUEST).send("No files specified");
    }
    req.body.files.forEach(function(file, idx) {
        var filePath = "";
        if (file[0] === "/" || file.search(/../g)) {
            // Somebody is attempting to change our directory path by inserting
            // either root or a relative path. Naughty.
            log.error("Bad behaviour detected");
            return;
        }
        try {
            filePath = path.resolve(config.audioSamplesPath, file);
            if (filePath) {
                log.debug("Deleting: " + filePath);
                fs.unlinkSync(filePath);
            }
        } catch (e) {
            log.error("Error [" + e + "] deleting file: " + filePath);
        }
    });
    return res.status(httpCodes.OK).send("Success");
});


router.post("/upload", function(req, res, next) {
    log.debug("GET /api/file/upload");
    var form = new formidable.IncomingForm();
    form.parse(req, function(err, fields, files) {
        var tmpPath = files.fileUpload.path;
        var uploadPath = path.resolve(config.audioSamplesPath, files.fileUpload.name);
        fs.rename(tmpPath, uploadPath, function(err) {
            if (err) {
                log.error("Error uploading file: " + err);
                return res.status(httpCodes.INTERNAL_SERVER_ERROR).send(err);
            }
            return res.status(httpCodes.OK).send("Success");
        });
    });
});

module.exports = router;
