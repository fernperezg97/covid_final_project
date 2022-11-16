let chart;
let countries;
let userChoice = "Cases";

fetch('https://unpkg.com/world-atlas/countries-50m.json')
.then((r) => r.json())
.then((data) => {
    countries = ChartGeo.topojson.feature(data, data.objects.countries).features;

  chart = new Chart(document.getElementById("canvas").getContext("2d"), {
    type: 'choropleth',
    data: {
      labels: countries.map((d) => d.properties.name),
      datasets: [{
        label: 'Countries',
        // countries.map forms a list and uses d to iterate through that list and the result is a list with a separate dictionary for each country.
        data: countries.map((d) => ({feature: d})), // feature is country name + geometry of the country | value is num confirmed cases for given country
      }]
    },
    options: {
      showOutline: true,
      showGraticule: false,
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
  // Initializing map display and populating with date of first COVID case (2020-03-22)
  const date_query_string = new URLSearchParams({date: "2020-03-22"}).toString();
  const query_Url = `/api/get-cases-by-date?${date_query_string}`;

  display_cases_on_map(query_Url);
});


let total_unique_days;
const slider = document.getElementById("myRange");
const output = document.getElementById("demo");
output.innerHTML = "2020-03-22"; // Display the default slider value
fetch('/api/get-list-days')
.then((r) => r.json())
.then((data) => { 
  slider.setAttribute("max", data['total_unique_days']-1); // gives you all of your slider values
  total_unique_days = data['list_unique_dates'];
});


// Update the current slider value (each time you drag the slider handle)

slider.oninput = function() {
  output.innerHTML = total_unique_days[this.value]; // value dependent on where user drags slider
}


// Update cases on map based on user chosen date
slider.onchange = function() {
  let chosen_date = total_unique_days[this.value];
  const date_query_string = new URLSearchParams({date: chosen_date}).toString()

  if (userChoice == "Cases") {
    const query_Url = `/api/get-cases-by-date?${date_query_string}`;
    display_cases_on_map(query_Url) 
  } else {
    const query_Url = `/api/get-deaths-by-date?${date_query_string}`;
    display_cases_on_map(query_Url) // displays deaths
  } 
}

// To both intialize map when first presented on webpage and to change values as user changes slider.
function display_cases_on_map(query_Url) {
  fetch(query_Url)
  .then((r) => r.json())
  .then((data) => {
    removeData(chart);
    let keys = Object.keys(data);
    let per_country_data = countries.map((d) => ({feature: d, value: data[d.properties.name]})); // setting per_country_data = a list a mini dicts
    addData(chart, keys, per_country_data);
    console.log(chart.data);
  }); 
}

function addData(chart, label, provided_data) {
  // chart.data.labels.push(label); // update list of countries
  chart.data.datasets[0].data = provided_data; // updating the properties that hold geometry,country name, and value to now include a value where math.random() was (geometry and country name are not changed)
  // chart.data.datasets.forEach((dataset) => {
  //     dataset.data.push(data);
  // });
  chart.update();
}

function removeData(chart) {
  // chart.data.labels = [];
  // console.log(chart.data.labels);
  chart.data.datasets[0].data = [];
      // console.log(chart.data.datasets);
  chart.update();
}


function dropdownOptions() {
  const mylist = document.getElementById("myList");
  let chosen_date = output.innerHTML;
  const date_query_string = new URLSearchParams({date: chosen_date}).toString();

  userChoice = mylist.options[mylist.selectedIndex].text;
  console.log("Person chose: ", userChoice);
  console.log("Date: ", chosen_date);

  if (userChoice == "Cases") {
    const query_Url = `/api/get-cases-by-date?${date_query_string}`;
    display_cases_on_map(query_Url); 
  } else {
    const query_Url = `/api/get-deaths-by-date?${date_query_string}`;
    display_cases_on_map(query_Url); // displays the deaths
  }
}