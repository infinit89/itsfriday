<?php

require ('vendor/autoload.php');

// https://github.com/Respect/Rest
use Respect\Rest\Router;

$r3 = new Router('/v1');

$r3->get('/memes/lang/*/*/*', function($lang, $start = 0, $limit = 10) {


    return json_encode('Memes desde el ' . $start . ' hasta el ' . $limit . ' en ' . $lang);
});

$r3->get('/memes/*/*', function($start = 0, $limit = 10) {


    return json_encode('Memes desde el ' . $start . ' hasta el ' . $limit);
});

