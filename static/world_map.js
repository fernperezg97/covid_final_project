let chart;
let countries;
let userChoice = "Cases";
let countriesList;
let chosen_date;

let user_date = userRecentDate();
console.log("Date Loaded is: ", user_date);

// creation of map
fetch('https://unpkg.com/world-atlas/countries-50m.json')
.then((r) => r.json())
.then((data) => {
    countries = ChartGeo.topojson.feature(data, data.objects.countries).features;
    countriesList = countries.map((d) => d.properties.name);
    sessionStorage.setItem("countriesList", countriesList);

  chart = new Chart(document.getElementById("canvas").getContext("2d"), {
    type: 'choropleth',
    data: {
      labels: countriesList,
      datasets: [{
        label: 'Countries',
        // countries.map forms a list and uses d to iterate through that list and the result is a list with a separate dictionary for each country.
        data: countries.map((d) => ({feature: d})), // feature is country name + geometry of the country | value is num confirmed cases for given country
        borderColor: "grey"
      }]
    },
    options: {
      showOutline: true,
      showGraticule: false,
      layout: {
        padding: {
          right: 60
        }
      },
      plugins: {
        customCanvasBackgroundColor: {
          color: '#F7F7F7'
        },
        legend: {
          display: false
        },
      },
      scales: {
        xy: {
          projection: 'equalEarth'
        },
        color: {
          // interpolate: "orRd",

          interpolate: (v) => {
                if (v < 0.1){
                  return "#ffff4d";
                } else if (v < 0.2){
                  return "#ffd500";
                } else if (v < 0.3){
                  return "#ffbb33";
                } else if (v < 0.4){
                  return "#ffaa00";
                } else if (v < 0.5){
                  return "#ff9933";
                } else if (v < 0.6){
                  return "#ff7733";
                } else if (v < 0.7){
                  return "#ff5500";
                } else if (v < 0.8){
                  return "#cc2200";
                } else if (v < 0.9){
                  return "#991900";
                } else if (v < 1){
                  return "#660000";
                } else {
                  return "#ffffff";
                }
              },
        }
      }
    },
    plugins: [plugin],
  });
  // Initializing map display and populating with date of first COVID case (2020-03-22)
  const date_query_string = new URLSearchParams({date: "2020-03-22"}).toString();
  const query_Url = `/api/get-cases-by-date?${date_query_string}`;

  display_cases_on_map(query_Url);
});

const plugin = {
  id: 'customCanvasBackgroundColor',
  beforeDraw: (chart, args, options) => {
    const {ctx} = chart;
    ctx.save();
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = options.color || '#99ffff';
    ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  }
};

let total_unique_days;
const slider = document.getElementById("myRange");
const output = document.getElementById("date"); // grabs everything within HTML object that has the id "date"

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
  chart.data.datasets[0].data = [];
  chart.update();
}


function dropdownOptions() {
  const mylist = document.getElementById("myList");
  let chosen_date = output.innerHTML;
  const date_query_string = new URLSearchParams({date: chosen_date}).toString();

  userChoice = mylist.options[mylist.selectedIndex].text;

  if (userChoice == "Cases") {
    const query_Url = `/api/get-cases-by-date?${date_query_string}`;
    display_cases_on_map(query_Url); 
  } else {
    const query_Url = `/api/get-deaths-by-date?${date_query_string}`;
    display_cases_on_map(query_Url); // displays the deaths
  }
}

// export { countries };
listOfCountries = sessionStorage.getItem("countriesList").split(","); // get takes in a key from the setItem dictionary you created
// console.log(listOfCountries);

// search bar functionality
const searchBar = document.querySelector("#search-by-country");

searchBar.addEventListener("submit", (evt) => {
  evt.preventDefault();
  let userSearchSelection = document.querySelector("#country-search-bar").value;
  let dateAtTimeOfSearch = document.querySelector("#date").innerHTML;
 

  sessionStorage.setItem("searchValue", userSearchSelection);
  sessionStorage.setItem("dateAtSearch", dateAtTimeOfSearch);
  window.location.href = "country-search";
  return;
})



// search bar autocomplete functionality

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  let currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      let a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      let x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    let x = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

autocomplete(document.getElementById("country-search-bar"), listOfCountries);



// log out button functionality

const logOut = document.querySelector("#logout-button");

logOut.addEventListener("click", () => {
  const recentDate = {
    dateBeforeLogout: output.innerHTML,
  };
  fetch('/save-recent-date', {
    method: "POST",
    body: JSON.stringify(recentDate),
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((r) => r.text())
    .then((dateSaved) => {
      console.log(dateSaved); 
  });

  window.location.href = "login";
  return;
});


// Display greeting that includes user's fname and recently chosen date, so it displays upon login
const welcomeBack = document.getElementById("welcome-back");

function userRecentDate() {
  fetch('/check-recent-date')
  .then((r) => r.text())
  .then((data) => { 
    welcomeBack.innerHTML = data;
    console.log("Date and name: ", data);
    return;
  });
}

// navbar sticky function

window.onscroll = function() {myFunction()};

const navbar = document.querySelector(".header");

const sticky = navbar.offsetTop;

function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky")
  } else {
    navbar.classList.remove("sticky");
  }
}