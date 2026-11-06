if ($response.statusCode !== 200) {
  $done(null);
}

var { country, city, query: ip, isp } = JSON.parse($response.body);

var title = typeof $environment !== 'undefined' && $environment.params
  ? $environment.params
  : country;

var subtitle = city + ' · ' + isp;
var description = country + '\n' + city + '\n' + isp + '\n' + ip;

$done({ title, subtitle, ip, description });