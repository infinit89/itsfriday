<?php

require ('vendor/autoload.php');

use Respect\Rest\Router;

$config = json_decode(file_get_contents(dirname(__FILE__) . '/../config.json'));

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

    $memes = ['cant' => 0, 'lang' => $lang, 'items' => []];
    foreach ($cursor as $id => $value) {
        echo $id .' -> ' . $value . '<br />';
        $memes['items'][] = $value;
    }

    // 'Memes desde el ' . $start . ' hasta el ' . $limit . ' en ' . $lang
    return json_encode($memes);
});


/*
 *
 */
$r3->get('/memes/*/*', function($start = 0, $limit = 10) use($collection) {

    $cursor = $collection->find(); // ->limit($limit)

    $memes = ['cant' => 0, 'lang' => 'all', 'items' => []];
    foreach ($cursor as $id => $value) {
        echo $id .' -> ' . $value . '<br />';
        $memes['items'][] = $value;
    }

    // 'Memes desde el ' . $start . ' hasta el ' . $limit
    return json_encode($memes);
});

