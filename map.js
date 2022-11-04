


// const url = "https://unpkg.com/world-atlas@2.0.2/countries-50m.json";
// // topojson = lines or arc lines combined = a country
// // geojson = fixed shape of country

// fetch(url).then((result) => result.json().then((datapoint) => { // parsing json to js
//     const countries = ChartGeo.topojson.feature(datapoint, datapoint.objects.countries).features;
     
//     // console.log(countries[0].properties.name);
//     console.log(); // country is a name I chose

//     // setup 
//     const data = {
//     labels: countries.map(country => country.properties.name),
//     datasets: [{
//         label: 'Countries',
//         data: countries.map(country => ({feature: country, value: Math.random()
//             })),
//         }]
//     };

//     // config 
//     const config = {
//         type: 'choropleth',
//         data,
//         options: {
//             showOutline: true, // this is to show OUTLINE of world map
//             scales: {
//                 xy: {
//                     projection: 'equalEarth'
//                 }
//             },
//             plugins: {
//                 legend: {
//                     display: false
//                 }
//             }
//         }
//     };

//     // render init block
//     const myChart = new Chart(
//         document.getElementById('myChart'),
//         config
//     );

// }))

fetch('https://unpkg.com/world-atlas/countries-50m.json').then((r) => r.json()).then((data) => {
      const countries = ChartGeo.topojson.feature(data, data.objects.countries).features;

  const chart = new Chart(document.getElementById("canvas").getContext("2d"), {
    type: 'choropleth',
    data: {
      labels: countries.map((d) => d.properties.name),
      datasets: [{
        label: 'Countries',
        data: countries.map((d) => ({feature: d, value: Math.random()})),
      }]
    },
    options: {
      showOutline: true,
      showGraticule: true,
      plugins: {
        legend: {
          display: false
        },
      },
      scales: {
        xy: {
          projection: 'equalEarth'
        }
      }
    }
  });
});