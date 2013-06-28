function sortByDate(list) {
    return _.sortBy(list, function(article) {
        return new Date(article.published);
    });
}

function keywordWeights(list) {
    var minRelevance = 0.4;
    var maxKeywords = 50;
    var blacklist = ["CNN.com Video"];
    var keywords = {};
    _.each(list, function(article) {
        _.each(_.filter(article.keywords, function(keyword) { return parseFloat(keyword.relevance) >= minRelevance; }),
               function(keyword) {
                   if (keywords[keyword.text]) {
                       keywords[keyword.text] += parseFloat(keyword.relevance);
                   } else {
                       keywords[keyword.text] = parseFloat(keyword.relevance);
                   }
               });
    });
    var topKeywords = _.filter(_.sortBy(_.pairs(keywords), _.last).reverse().slice(0, maxKeywords),
                               function (pair) {
                                   return _.find(blacklist, function (word) {
                                       return pair.indexOf(word) !== -1;
                                   }) == null;
                               });
    return _.object(_.sortBy(topKeywords, _.first));
}

function filterByKeyword(list, keyword) {
    return _.filter(list, function(article) {
        return (_.find(article.keywords, function(k) {
            return k.text == keyword;
        })) != undefined;
    });
}

function sourcesFromArticles(list) {
    return _.uniq(_.map(list, function(article) {
        return {name: article.source, link: article.sourceUrl};
    }), false, function(source) { return source.link; });
}

function filterBySource(list, source) {
    return _.filter(list, function(article) {
        return article.source == source;
    });
}

function cityWeights(list) {
    var cities = {};
    _.each(list, function(article) {
        _.each(article.cities, function(city) {
                   if (cities[city]) {
                       cities[city] += 1;
                   } else {
                       cities[city] = 1;
                   }
               });
    });
    return cities;
}

function countryWeights(list) {
    var countries = {};
    _.each(list, function(article) {
        _.each(article.countries, function(country) {
                   if (countries[country]) {
                       countries[country] += 1;
                   } else {
                       countries[country] = 1;
                   }
               });
    });
    return countries;
}

function filterByCity(list, city) {
    return _.filter(list, function(article) {
        return _.contains(article.cities, city);
    });
}

function filterByCountry(list, country) {
    return _.filter(list, function(article) {
        return _.contains(article.countries, country);
    });
}

var currentArticles = sortByDate(articles);


/* MUSTACHE TEMPLATES */
var renderHeadlines = Mustache.compile('{{#entries}}'+
                                 '<a href={{link}} target="_blank"><div class="article">{{title}}</div></a>'+
                                 '{{/entries}}');

var renderSources = Mustache.compile('{{#sources}}'+
                                     '<a href={{link}} target="_blank"><div class="source">{{name}}</div></a>'+
                                     '{{/sources}}');
var renderKeywords = Mustache.compile('{{#keywords}}'+
									  '<a href={{link}} target="_blank"><div class"keyword">{{keyword}}</div></a>'+	
									  '{{/keywords}}');
var renderTags = Mustache.compile('{{#tags}}'+
                                  '<a style="font-size:{{size}}px">{{keyword}}</a>'+
                                  '{{/tags}}');
