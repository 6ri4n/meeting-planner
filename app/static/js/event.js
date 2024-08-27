const meetingElement = document.getElementById("meeting");
const meeting = JSON.parse(meetingElement.textContent);
const participantsElement = document.getElementById("participants");
const participants = JSON.parse(participantsElement.textContent);
const renderGrid = handleGrid();
const { select, setSelection } = selectionState();
const eventId = window.location.pathname.substring(1);
const debouncedHandleUpdateReq = debounce(handleUpdateReq, 3000);
let user = undefined;

window.onload = function () {
  renderGrid("view-main-content");
  handleSignIn();
};

function handleGrid() {
  return renderGrid;

  function renderGrid(parentEle) {
    const selectedDays = Object.entries(meeting.days);
    const availDays = document.querySelector(`#${parentEle} #available-days`);
    const availTimes = document.querySelector(`#${parentEle} #available-times`);
    const displayTimes = document.querySelector(`#${parentEle} #display-times`);

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
      availDays.appendChild(availableDay);

      const container = document.createElement("div");
      container.className = "available-time-col";
      for (const [rowIndex, _] of meeting.times.entries()) {
        const availableTime = document.createElement("div");
        const col = (colIndex + 1).toString();
        const row = (rowIndex + 1).toString();
        availableTime.id = dateKey;
        availableTime.className = "available-time";
        availableTime.setAttribute("data-col", col);
        availableTime.setAttribute("data-row", row);
        availableTime.addEventListener("dragstart", (event) => {
          event.preventDefault();
        });

        if (parentEle === "edit-main-content") {
          container.appendChild(initHighlight(availableTime, col, row));
        } else if (parentEle === "view-main-content") {
          // TODO: handle view-main-content
          container.appendChild(availableTime);
        }
      }
      availTimes.appendChild(container);
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

      let response = await handleRequest("/event/signin", {
        eventId,
        eventId,
        username: username.value,
      });

      if (!response.ok) return;

      user = username.value;
      if (response.status === 201) {
        participants[user] = {};
      }

      document.getElementById("signin").remove();
      renderEditHTML();
      renderGrid("edit-main-content");
      setupListeners("#edit-main-content", handleDragSelection());
    });

  function handleDragSelection() {
    return {
      mousedown: function handleMouseDown(event) {
        const element = event.target;
        const row = event.target.getAttribute("data-row");
        const col = event.target.getAttribute("data-col");
        setSelection("down", element, col, row);
      },
      mouseup: function handleMouseUp(event) {
        const element = event.target;
        const row = event.target.getAttribute("data-row");
        const col = event.target.getAttribute("data-col");
        setSelection("up", element, col, row);
        handleHighlight();
        debouncedHandleUpdateReq();
      },
    };
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
}

async function handleRequest(URL, payload) {
  try {
    const response = await fetch(`http://localhost:5000/api${URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
    return response;
  } catch (error) {
    console.error(error);
  }
}

function setupListeners(parent, listenersObj) {
  document
    .querySelectorAll(`${parent} #available-times div`)
    .forEach((availableTime) => {
      if (availableTime.classList.contains("available-time-col")) return;
      for (const [eventType, eventListener] of Object.entries(listenersObj)) {
        availableTime.addEventListener(eventType, eventListener);
      }
    });
}

function selectionState() {
  const select = {
    down: { element: undefined, col: undefined, row: undefined },
    up: { element: undefined, col: undefined, row: undefined },
  };
  function setSelection(type, element, col, row) {
    if (type === "down" || type === "up") {
      select[type] = { element, col, row };
    }
  }
  return { select, setSelection };
}

function initHighlight(element, col, row) {
  if (!participants[user][element.id]) return element;
  if (!participants[user][element.id].length) return element;
  for (const time of participants[user][element.id]) {
    if (time.col === col && time.row === row) {
      element.classList.add("highlight-time");
    }
  }
  return element;
}

function handleHighlight() {
  const { element: downElement, col: downCol, row: downRow } = select.down;
  const { col: upCol, row: upRow } = select.up;
  const startCol = Math.min(downCol, upCol);
  const endCol = Math.max(downCol, upCol);
  const startRow = Math.min(downRow, upRow);
  const endRow = Math.max(downRow, upRow);
  const isHighlight = downElement.classList.contains("highlight-time");
  const times = document.querySelectorAll(
    "#edit-main-content #available-times div"
  );
  const numRows = meeting.times.length;

  for (let col = startCol; col <= endCol; col++) {
    const startRowIndex = col * (numRows + 1) - numRows;
    const start = startRowIndex + startRow - 1;
    const end = startRowIndex + endRow - 1;
    for (let row = start; row <= end; row++) {
      updateUserData(isHighlight, times[row]);
    }
  }

  function updateUserData(isHighlight, element) {
    const row = element.getAttribute("data-row");
    const col = element.getAttribute("data-col");
    if (isHighlight) {
      element.classList.remove("highlight-time");
      const updatedArr = participants[user][element.id].filter(
        (time) => time.col !== col || time.row !== row
      );
      participants[user][element.id] = updatedArr;
    } else {
      element.classList.add("highlight-time");
      if (participants[user][element.id]) {
        participants[user][element.id].push({ col, row });
      } else {
        participants[user][element.id] = [{ col, row }];
      }
    }
  }
}

async function handleUpdateReq() {
  try {
    const response = await handleRequest("/event/update", {
      username: user,
      eventId: eventId,
      selectedTimes: participants[user],
    });

    if (!response.ok) {
      alert("Server Error, Reloading Page.");
      window.location.reload();
    }
  } catch (error) {
    console.error(error);
    alert("Server Error, Reloading Page.");
    window.location.reload();
  }
}

function debounce(cb, delay) {
  let timeout;

  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      cb(...args);
    }, delay);
  };
}
