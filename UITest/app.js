// take care of dependencies

/**
 * exports of express module
 * @type {Object}
 */
var express = require('express');

/**
 * exports of path module
 * @type {Object}
 */
var path = require('path');

/**
 * instance of express
 * @type {Function}
 */
var app = express();



// setting up route variables

/**
 * backend index functionality
 * @type {Object}
 */
const route_index = require('./routes/index');
const route_test = require('./routes/test');

/**
 * port to allow connections on
 * @type {Number}
 */
const port = 4000;



// setting up view engine
app.set('views', path.join(__dirname, 'views'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

// setting up static folder
app.use(express.static(path.join(__dirname, 'public')));

// assigning routes to app
app.use('/', route_index);
app.use('/index', route_index);
app.use('/test', route_test);

// expose public port
app.listen(port);

console.log("MonArc has started on port " + port);
