const selectedDays = {};

window.onload = function () {
  loadTimezone();
  handleCalendar();
  handleFormSubmit();
  document.getElementById("eventName").value = "";
  document.getElementById("description").value = "";
  document.getElementById("startTimeSelector").selectedIndex = 0;
  document.getElementById("endTimeSelector").selectedIndex = 0;
};

function handleCalendar() {
  const longMonth = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
  };
  const maxSelections = 14;
  const dayParentElement = document.querySelector(".day");
  const headerElement = document.querySelector(".calendar header span");
  let date = new Date();
  let year = date.getFullYear();
  let month = date.getMonth() + 1;

  handleCalendarNav();
  generateCalendar();

  function generateCalendar() {
    let lastDayPrevMonth = new Date(year, month - 1, 0);
    let lastDayCurMonth = new Date(year, month, 0).getDate();
    const lastSundayPrevMonthObj = new Date(lastDayPrevMonth);
    lastSundayPrevMonthObj.setDate(
      lastSundayPrevMonthObj.getDate() - lastDayPrevMonth.getDay()
    );
    lastSundayPrevMonth = lastSundayPrevMonthObj.getDate();
    lastDayPrevMonth = lastDayPrevMonth.getDate();
    headerElement.textContent = longMonth[month] + " " + year;

    for (
      let prevDay = lastSundayPrevMonth;
      prevDay <= lastDayPrevMonth;
      prevDay++
    ) {
      const day = document.createElement("li");
      day.classList.add("not-current-month");
      day.textContent = prevDay;
      dayParentElement.appendChild(day);
    }

    for (let curDay = 1; curDay <= lastDayCurMonth; curDay++) {
      const { formatKey, formatValue } = formatDate(month, curDay, year);
      const day = document.createElement("li");
      day.classList.add("current-month");
      day.textContent = curDay;
      day.id = formatKey;

      if (selectedDays.hasOwnProperty(formatKey)) {
        day.classList.add("selected-day");
      }

      day.addEventListener("click", (event) => {
        if (event.target.classList.toggle("selected-day")) {
          if (Object.keys(selectedDays).length === maxSelections) {
            event.target.classList.remove("selected-day");
            return alert("You can only select up to 14 days.");
          }
          selectedDays[formatKey] = formatValue;
        } else {
          delete selectedDays[formatKey];
        }
      });

      dayParentElement.appendChild(day);
    }

    for (
      let nextDay = 1;
      nextDay < 42 - lastDayCurMonth - (lastDayPrevMonth - lastSundayPrevMonth);
      nextDay++
    ) {
      const day = document.createElement("li");
      day.classList.add("not-current-month");
      day.textContent = nextDay;
      dayParentElement.appendChild(day);
    }

    function formatDate(month, day, year) {
      const date = new Date(year, month - 1, day);
      const monthLong = longMonth[month];
      const dayLong = date.toLocaleDateString("en-US", {
        weekday: "long",
      });
      return {
        formatKey: `${month}-${day}-${year}`,
        formatValue: { month, day, dayLong, monthLong, year },
      };
    }
  }

  function handleCalendarNav() {
    document.querySelectorAll(".calendar-nav button").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();

        if (e.target.id === "prev") {
          if (month === 1) {
            month = 12;
            year -= 1;
          } else {
            month -= 1;
          }
          date = new Date(year, month - 1);
        } else {
          if (month === 12) {
            month = 1;
            year += 1;
          } else {
            month += 1;
          }
          date = new Date(year, month - 1);
        }

        dayParentElement.replaceChildren();
        generateCalendar();
      });
    });
  }
}

function handleFormSubmit() {
  document.querySelector("form").addEventListener("submit", async (event) => {
    event.preventDefault();
    if (Object.entries(selectedDays).length === 0)
      return alert("Meeting days cannot be empty.");
    handleRequest(event);
  });

  document.querySelector("#cancel").addEventListener("click", (event) => {
    event.preventDefault();
    window.location.reload();
  });
}

async function handleRequest(event) {
  const URL = "/api/event/create"
  const formData = new FormData(event.target);
  const sortedSelectedDays = sortDates();
  const formObj = {};

  formData.forEach((value, key) => {
    formObj[key] = value;
  });
  formObj["selectedDays"] = sortedSelectedDays;

  try {
    const response = await fetch(URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formObj),
    });

    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

    const responseData = await response.json();

    if (responseData.redirect_url)
      window.location.href = responseData.redirect_url;
  } catch (error) {
    console.error(error);
  }
}

function sortDates() {
  const sortedSelectedDays = Object.entries(selectedDays);
  sortedSelectedDays.sort((a, b) => {
    const dateA = a[1];
    const dateB = b[1];
    if (dateA.year !== dateB.year) return dateA.year - dateB.year;
    if (dateA.month !== dateB.month) return dateA.month - dateB.month;
    return dateA.day - dateB.day;
  });
  return Object.fromEntries(sortedSelectedDays);
}

function loadTimezone() {
  const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const timezoneSelect = document.getElementById("timezone");
  for (let i = 0; i < timezoneSelect.options.length; i++) {
    if (timezoneSelect.options[i].value === userTimezone) {
      timezoneSelect.selectedIndex = i;
      break;
    }
  }
}
