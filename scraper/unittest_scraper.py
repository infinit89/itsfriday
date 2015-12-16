import unittest,json,urllib2;

class testing(unittest.TestCase):

    def setUp(self):
        self.API_KEY_BING = 'XJ4NbYb5R6ui4CL2WbfDcnBtil91K/TwhpNVNzjZW+A';
        self.json = '../config.json';

    # Comprueba apertura de json
    def test_open_json(self):
        try:
             with open(self.configJson) as configJson:
                json_data = json.load(configJson);
        except:
            # Error Open File
            self.assertFalse(False);
        else:
            # No error
            self.assertTrue(True);


    def test_json_init_variables(self):
        try:
            with open(self.configJson) as configJson:
                json_data = json.load(configJson);

                self.assertIs(type(json_data['mongodb']['server']), str);
                self.assertIs(type(json_data['mongodb']['port']), int);
                self.assertIs(type(json_data['mongodb']['db']), str);
                self.assertIs(type(json_data['mongodb']['memes_collection']), str);
        except:
            self.assertFalse(False);

    def test_getImagesBing(self):

        search = 'memes its friday';
        search = search.replace(" ","%20");
        end = 10;
        start = 0;

        url = ('https://api.datamarket.azure.com/Bing/Search/Image?$format=json&Query=%27' + search + '%27&$top=' + str(end) + '&$skip=' + str(start))

        credentialBing = 'Basic ' + (':%s' % self.API_KEY_BING).encode('base64')[:-1]
        request = urllib2.Request(url)
        request.add_header('Authorization', credentialBing)
        requestOpener = urllib2.build_opener()
        response = requestOpener.open(request)

        results = json.load(response);

        self.assertGreater(len(results['d']['results']), 0);


if __name__ == '__main__':
    unittest.main()