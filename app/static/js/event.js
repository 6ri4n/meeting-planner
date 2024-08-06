let user = undefined;
const renderGrid = handleGrid();

renderGrid("view-main-content");
handleSignIn();

function handleGrid() {
  const meetingElement = document.getElementById("meeting");
  const meeting = JSON.parse(meetingElement.textContent);
  const selectedDays = Object.entries(meeting.days);

  return renderGrid;

  function renderGrid(parentElement, listenersObj) {
    const availableDays = document.querySelector(
      `#${parentElement} #available-days`
    );
    const availableTimes = document.querySelector(
      `#${parentElement} #available-times`
    );
    const displayTimes = document.querySelector(
      `#${parentElement} #display-times`
    );

    for (const time of meeting.times) {
      const displayTime = document.createElement("div");
      displayTime.id = displayTime.textContent = time;
      displayTimes.appendChild(displayTime);
    }

    for (let [colIndex, [dateKey, dateObj]] of selectedDays.entries()) {
      const availableDay = document.createElement("div");
      const month = document.createElement("div");
      const week = document.createElement("div");
      month.textContent = `${dateObj.monthLong.substring(0, 3)} ${dateObj.day}`;
      week.textContent = `${dateObj.dayLong.substring(0, 3)}`;
      availableDay.className = "available-day";
      availableDay.append(month, week);
      availableDays.appendChild(availableDay);

      const container = document.createElement("div");
      container.className = "available-time-col";
      for (const [rowIndex, _] of meeting.times.entries()) {
        const availableTime = document.createElement("div");
        availableTime.id = dateKey;
        availableTime.className = "available-time";
        availableTime.setAttribute("data-col", colIndex + 1);
        availableTime.setAttribute("data-row", rowIndex + 1);

        // for (const [eventType, eventListener] of Object.entries(listenersObj)) {
        //   availableTime.addEventListener(eventType, eventListener);
        // }

        container.appendChild(availableTime);
      }
      availableTimes.appendChild(container);
    }
  }
}

function handleSignIn() {
  document
    .getElementById("signin")
    .addEventListener("submit", async (event) => {
      event.preventDefault();
      const username = document.getElementById("username");
      if (username.value === "") return alert("Username cannot be empty.");
      // handleRequest(event);
      // validate request
      user = username.value;

      if (user) {
        const signIn = document.getElementById("signin");
        signIn.remove();
        renderEditHTML();
        renderGrid("edit-main-content");
      }
    });
}

async function handleRequest(event) {
  const URL = "http://localhost:5000/api/event/signin";
  const formData = new FormData(event.target);
  const formObj = {};

  formData.forEach((value, key) => {
    formObj[key] = value;
  });

  console.log(formObj);

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

    console.log(responseData);
  } catch (error) {
    console.error(error);
  }
}

function renderEditHTML() {
  const availableDays = document.createElement("div");
  availableDays.id = "available-days";
  const filler = document.createElement("div");
  filler.className = "filler";
  availableDays.appendChild(filler);

  const timeContainer = document.createElement("div");
  timeContainer.id = "time-container";
  const displayTimes = document.createElement("div");
  displayTimes.id = "display-times";
  const availableTimes = document.createElement("div");
  availableTimes.id = "available-times";
  timeContainer.appendChild(displayTimes);
  timeContainer.appendChild(availableTimes);

  const section = document.createElement("section");
  section.id = "edit-main-content";
  section.appendChild(availableDays);
  section.appendChild(timeContainer);

  const mainContent = document.getElementById("main-content");
  const viewMainContent = document.getElementById("view-main-content");
  mainContent.insertBefore(section, viewMainContent);
}
