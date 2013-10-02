$(function () {
    var allWords = JSON.parse($('#all-words').text());
    var tfIdf = JSON.parse($('#tf-idf').text());
    var users = $.map(tfIdf, function(_, user) { return user; });

    var series = [];
    $.each(users, function(_, user) {
        var data = $.map(allWords, function(word) {
                       return tfIdf[user][word] ? tfIdf[user][word] : 0;
                   });
        series.push({
            name: user,
            data: data
        });
    });

    $('#container').highcharts({
        chart: {
            type: 'bar',
            inverted: true
        },
        title: { text: 'TF-IDF Scoring Based on Tweets'},
        subtitle: { text: 'Demo' },
        xAxis: {
            categories: allWords,
            title: { text: null }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'TF-IDF Score',
                align: 'high'
            },
            labels: { overflow: 'justify' }
        },
        plotOptions: {
            bar: {
                dataLabels: { enabled: true }
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 100
        },
        credits: { enabled: false },
        series: series
    });
});
