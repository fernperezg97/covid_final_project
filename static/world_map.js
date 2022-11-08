fetch('https://unpkg.com/world-atlas/countries-50m.json')
.then((r) => r.json())
.then((data) => {
      const countries = ChartGeo.topojson.feature(data, data.objects.countries).features;

  const chart = new Chart(document.getElementById("canvas").getContext("2d"), {
    type: 'choropleth',
    data: {
      labels: countries.map((d) => d.properties.name),
      datasets: [{
        label: 'Countries',
        data: countries.map((d) => ({feature: d, value: Math.random(), date: "202x-xx-xx"})),
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
  console.log(chart.data.datasets[0].data);
});

let total_unique_days;
var slider = document.getElementById("myRange");
var output = document.getElementById("demo");
output.innerHTML = slider.value; // Display the default slider value
fetch('/api/get-list-days')
.then((r) => r.json())
.then((data) => { 
  console.log(data);
  slider.setAttribute("max", data['total_unique_days']); // gives you all of your slider values
  total_unique_days = data['list_unique_dates'];
});


// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = total_unique_days[this.value]; // value dependent on where user drags slider
  console.log(total_unique_days[this.value]);
}


// Update cases on map based on user chosen date
slider.onchange = function() {
  let chosen_date = total_unique_days[this.value];
  const date_queried = new URLSearchParams({date: chosen_date}).toString()
  const query_Url = `/api/get-cases-by-date?${date_queried}`;

  fetch(query_Url)
  .then((r) => r.json())
  .then((data) => {
    console.log(data);
    
  });
}
