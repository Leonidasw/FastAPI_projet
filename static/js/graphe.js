function get_score(){
  const url = 'http://127.0.0.1:8000/profile_page/get_score'
  fetch(url,{
    method: "post",
    headers: {
      "Content-Type": "application/json",
    },
  })
  .then(response => response.json())
  .then(data => {publie_score(data)});
}

function publie_score(data){
  [facile,moyen,difficile] = data
  Highcharts.chart('container', {

    title: {
      text: 'Temps au démineur'
    },
  
    subtitle: {
      text: ''
    },
  
    yAxis: {
      title: {
        text: 'Votre temps (en secondes)'
      }
    },
  
    xAxis: {
      accessibility: {
        rangeDescription: 'Range: 2010 to 2017'
      }
    },
  
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle'
    },
  
    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        },
        pointStart: 1
      }
    },
  
    series: [{
      name: 'Facile',
      data: facile
    }, {
      name: 'Moyen',
      data: moyen
    }, {
      name: 'Difficile',
      data: difficile
    }],
  
    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
          }
        }
      }]
    }
  });
}

get_score()