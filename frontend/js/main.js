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

function articlesWithKeyword(list, keyword) {
    return _.filter(list, function(article) {
        return (_.find(article.keywords, function(k) {
            return k.text == keyword;
        })) != undefined;
    });
}
