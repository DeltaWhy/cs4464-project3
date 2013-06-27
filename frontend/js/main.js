function sortByDate(list) {
    return _.sortBy(list, function(article) {
        return new Date(article.published);
    });
}

function keywordWeights(list) {
    var minRelevance = 0.5;
    var keywords = {};
    _.each(list, function(article) {
        _.each(_.filter(article.keywords, function(keyword) { return parseFloat(keyword.relevance) >= minRelevance; }),
               function(keyword) {
                   if (keywords[keyword.text]) {
                       keywords[keyword.text] += 1;
                   } else {
                       keywords[keyword.text] = 1;
                   }
               });
    });
    return keywords;
}

function filterByKeyword(list, keyword) {
    return _.filter(list, function(article) {
        return (_.find(article.keywords, function(k) {
            return k.text == keyword;
        })) != undefined;
    });
}

function sourcesFromArticles(list) {
    return _.object(_.uniq(_.map(list, function(article) {
        return [article.source, article.sourceUrl];
    })));
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
