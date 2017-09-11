/*
 * File: log.js
 * Author: dgrubb
 * Date: 09/08/2017
 *
 * Provides an interface for consistent logging throughout the application.
 */

var winston = require("winston");
var rightpad = require("right-pad");

module.exports = new (winston.Logger)({
    transports: [
        new (winston.transports.Console)({
            timestamp: function() {
                return (new Date)
                    .toISOString()
                    .replace(/T/, ' ')
                    .replace(/\..+/, '');
            },
            formatter: function(options) {
                var logLevel = options.level.toUpperCase();
                return '[ ' + options.timestamp() + ' ]' +
                    ' [ ' + rightpad(logLevel, 8, " ") + ' ] ' +
                    (options.message ? options.message : '') +
                    (options.meta && Object.keys(options.meta).length ?
                    '\n\t' + JSON.stringify(options.meta) :
                    '');
            },
            padRight: function(str, padStr) {
                return (str + padStr).substring(0, padStr.length);
            }
        })
    ]
});

