<?php

require (dirname(__FILE__) . '/../vendor/autoload.php');


// https://github.com/Respect/Rest
class ApiTest extends PHPUnit_Framework_TestCase {
    protected $client;

    protected function setUp() {

        $this->client = new GuzzleHttp\Client([
            'base_uri' => 'http://localhost/v1/'
        ]);

    }

    public function testGet_Memes() {

        $response = $this->client->get('memes');

        $this->assertEquals(200, $response->getStatuscode());


        $data = $response->getBody();

        $this->assertArrayHasKey('cant', $data);
        $this->assertArrayHasKey('lang', $data);
        $this->assertArrayHasKey('items', $data);

        // The quantity of elements should match the cant returned in json
        $this->assertCount($data['cant'], $data['items']);
    }

    public function testGet_Memes_LangEn() {
        $response = $this->client->get('/memes'. [
                'query' => [
                    'lang' => 'en'
                ]
            ]);

        $this->assertEquals(200, $response->getStatuscode());

        $data = $response->getBody();

        $this->assertArrayHasKey('cant', $data);
        $this->assertArrayHasKey('lang', 'en');
        $this->assertArrayHasKey('items', $data);

        // The quantity of elements should match the cant returned in json
        $this->assertCount($data['cant'], $data['items']);
    }

}
