/**
 * exports of express and formidable module
 * @type {Object}
 */
var express = require('express');
var formidable = require('formidable');

/**
 * express router for frontend/backend interaction
 * @type {Function}
 */
var router = express.Router();

router.get('/', function(req, res) {
  res.render('test');
});

module.exports = router;
