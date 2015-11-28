<?php

require ('vendor/autoload.php');

use Respect\Rest\Router;

$r3 = new Router('/v1');


$r3->get('/', function() {

    return 'Router installed';
});

