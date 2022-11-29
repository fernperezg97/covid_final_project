// page that will display the search result country data

// import { countries } from './world_map.js'
// console.log("Countries are:", countries);

const countrySearched = sessionStorage.getItem("searchValue");
const dateSearched = sessionStorage.getItem("dateAtSearch");

document.getElementById("country-name").innerHTML = countrySearched;
document.getElementById("dateAtSearch").innerHTML = dateSearched;

console.log("The value saved was named: ", countrySearched);
console.log("The date saved is : ", dateSearched);

const queryString = new URLSearchParams({ "country": countrySearched }).toString();
const url = `/api/get-country-search-stats?${queryString}`;

fetch(url)
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        document.querySelector('#population').innerHTML = data['population'];
        document.querySelector('#cases').innerHTML = data['total_cases_stats'];
        document.querySelector('#active').innerHTML = data['active_cases'];
        document.querySelector('#cases-1m').innerHTML = data['cases_1m'];
        document.querySelector('#deaths').innerHTML = data['total_deaths_stats'];
        document.querySelector('#deaths-1m').innerHTML = data['deaths_1m'];
        document.querySelector('#tests').innerHTML = data['total_tests'];
        document.querySelector('#tests-1m').innerHTML = data['tests_1m'];
});


// const config = {
//     type: 'line',
//     data: data,
//   };

// const labels = Utils.months({count: 7});
// const data = {
//   labels: labels,
//   datasets: [{
//     label: 'My First Dataset',
//     data: [65, 59, 80, 81, 56, 55, 40],
//     fill: false,
//     borderColor: 'rgb(75, 192, 192)',
//     tension: 0.1
//   }]
// };

const lineGraphUrl = `/api/get-line-graph-stats?${queryString}`;

fetch(lineGraphUrl)
    .then((countryData) => countryData.json())
    .then((casesAndDeathsData) => {
        console.log(casesAndDeathsData);

        new Chart(document.getElementById("line-chart"), {
            type: 'line',
            data: {
              labels: casesAndDeathsData["dates"],
              datasets: [{
                label: 'Cases',
                data: casesAndDeathsData["cases"],
                fill: false,
                borderColor: 'rgb(0, 0, 255)',
                tension: 0.1 
              }, 
                {
                label: 'Deaths',
                data: casesAndDeathsData["deaths"],
                fill: false,
                borderColor: 'rgb(255, 0, 0)',
                tension: 0.1 
                }]
            },
            options: {
                plugins: {
                    title: {
                        display: true,
                        text: 'COVID-19 Cases and Deaths from March 22, 2020 - Present'
                  }
                },
                scales: {
                    xAxes: {
                        // type: 'time',
                        ticks: {
                            // autoSkip: true,
                            maxTicksLimit: 10,
                        }
                    }
                },
            }
        });
})