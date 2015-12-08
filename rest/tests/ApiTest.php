<?php

require (dirname(__FILE__) . '/../vendor/autoload.php');


// https://github.com/Respect/Rest
class ApiTest extends PHPUnit_Framework_TestCase {
    protected $client;

    protected function setUp() {

        $config = json_decode(file_get_contents(dirname(__FILE__) . '/../../config.json'));

        $this->client = new GuzzleHttp\Client([
            'base_uri' => $config->api->endpoint
        ]);

    }

    public function testGet_Memes() {

        $response = $this->client->get('memes');

        $this->assertEquals(200, $response->getStatuscode());

        $data = json_decode($response->getBody());

        $this->assertObjectHasAttribute('cant', $data);
        $this->assertObjectHasAttribute('lang', $data);
        $this->assertObjectHasAttribute('items', $data);

        // The quantity of elements should match the cant returned in json
        $this->assertCount($data->cant, $data->items);
    }

    public function testGet_Memes_LangEn() {

        $response = $this->client->get('memes/lang/en');

        $this->assertEquals(200, $response->getStatuscode());

        $data = json_decode($response->getBody());

        $this->assertObjectHasAttribute('cant', $data);
        $this->assertObjectHasAttribute('lang', $data);
        $this->assertObjectHasAttribute('items', $data);
        $this->assertEquals($data->lang, 'en');

        // The quantity of elements should match the cant returned in json
        $this->assertCount($data->cant, $data->items);
    }

}
