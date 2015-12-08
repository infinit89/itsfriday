<?php

require ('vendor/autoload.php');

use Respect\Rest\Router;

define('CONFIG_FILE', dirname(__FILE__) . '/../config.json');

$config = json_decode(file_get_contents(CONFIG_FILE));

try {
    $mongodb = new MongoDB\Driver\Manager('mongodb://' . $config->mongodb->server . ':' . $config->mongodb->port);
    $collection = new MongoDB\Collection($mongodb, $config->mongodb->db . '.' . $config->mongodb->memes_collection);
} catch (Exception $e) {

    die(json_encode('Imposible recuperar los memes'));
}

$r3 = new Router('/v1');

/*
 *
 */
$r3->get('/memes/lang/*/*/*', function($lang, $start = 0, $limit = 10) use ($collection)  {

    $cursor = $collection->find(['lang' => $lang]); // ->limit($limit)

    foreach ($cursor as $id => $value) {
        echo $id .' -> ' . $value . '<br />';
    }

    return json_encode('Memes desde el ' . $start . ' hasta el ' . $limit . ' en ' . $lang);
});


/*
 *
 */
$r3->get('/memes/*/*', function($start = 0, $limit = 10) use($collection) {

    $cursor = $collection->find(); // ->limit($limit)

    foreach ($cursor as $id => $value) {
        echo $id .' -> ' . $value . '<br />';
    }

    return json_encode('Memes desde el ' . $start . ' hasta el ' . $limit);
});

