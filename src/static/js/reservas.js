document.getElementById("menu").addEventListener("click", function () {
    window.location.href = "/start"; //VER MELHOR
  });

  document.getElementById("checkIn").addEventListener("click", function () {
      fetchReservations("checkin");
  });

  document.getElementById("checkOut").addEventListener("click", function () {
      fetchReservations("checkout");
  });

  function fetchReservations(action) {
      const buttonContainer = document.getElementById("newButtonsContainer");
      buttonContainer.innerHTML = "";

      fetch("/api/reservas-dia")
          .then((response) => response.json())
          .then((data) => {
              displayReservations(data, action);
          })
          .catch((error) => {
              console.error("Erro ao buscar as reservas:", error);
          });
  }

  function displayReservations(reservations, action) {
      const buttonContainer = document.getElementById("newButtonsContainer");
      let reservationsHTML = `
          <h2 style="color: #693c01; font-weight: bold;">Reservas</h2>
          <div class="reservations-container">
              <table class="reservations-table">
                  <thead>
                      <tr>
                          <th>Quarto</th>
                          <th>ID da Reserva</th>
                          <th>Nome do Cliente</th>
                          <th>Tipo de Quarto</th>
                          <th>Número de Pessoas</th>
                          <th>Número de Camas</th>
                          <th>Check-In</th>
                          <th>Check-Out</th>
                      </tr>
                  </thead>
                  <tbody>
      `;

      reservations.forEach((reservation) => {
          const checkInEmoji = reservation[6] ? "✅" : "❌"; // Check-In
          const checkOutEmoji = reservation[7] ? "✅" : "❌"; // Check-Out
          reservationsHTML += `
               <tr data-reservation='${JSON.stringify(reservation)}'>
                  <td style="color: #6f4f28; font-weight: bold;">${reservation[0]}</td>
                  <td>${reservation[1]}</td>
                  <td>${reservation[2]}</td>
                  <td>${reservation[3]}</td>
                  <td>${reservation[4]}</td>
                  <td>${reservation[5]}</td>
                  <td class="checkin-status">${checkInEmoji}</td> 
                  <td class="checkout-status">${checkOutEmoji}</td> 
              </tr>
          `;
      });

      reservationsHTML += `
                  </tbody>
              </table>
          </div>
          <button id="menuButton" class="menuButton" onclick="menu()">Menu</button>
      `;

      buttonContainer.innerHTML = reservationsHTML;

      // Adiciona o event listener para cada linha da tabela
      document.querySelectorAll(".reservations-table tbody tr").forEach((row) => {
          row.addEventListener("click", () => {
              const checkInCell = row.querySelector(".checkin-status");
              const checkOutCell = row.querySelector(".checkout-status");
              const reservaId = row.cells[1].textContent; // id da reserva (índice 1)

              if (action === "checkin" && checkInCell.textContent === "❌") {
                  checkInCell.textContent = "✅";
                  processCheckIn(reservaId);
              } else if (action === "checkout" && checkOutCell.textContent === "❌") {
                  checkOutCell.textContent = "✅";
                  processCheckOut(reservaId);
              }
          });
      });
  }

  function processCheckIn(reservaId) {
  const value = 0; 
  console.log(reservaId)
  fetch(`/api/reserva/check/${reservaId}?value=${value}`, { // Adicionar o valor como parâmetro no URL
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      //body: JSON.stringify({ checkin: true }),
  })
      .then((response) => {
          if (!response.ok) {
              throw new Error("Erro ao realizar check-in");
          }
          return response.json();
      })
      .then((data) => {
          console.log("Check-in realizado com sucesso:", data);
      })
      .catch((error) => {
          console.error("Erro ao realizar check-in:", error);
          alert("Erro ao realizar check-in: " + error.message);
      });
}
  function processCheckOut(reservaId) {
      const value = 1; 
      fetch(`/api/reserva/check/${reservaId}?value=${value}`, {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ checkout: true, value: 1 }),
      })
          .then((response) => {
              if (!response.ok) {
                  throw new Error("Erro ao realizar check-out");
              }
              return response.json();
          })
          .then((data) => {
              console.log("Check-out realizado com sucesso:", data);
          })
          .catch((error) => {
              console.error("Erro ao realizar check-out:", error);
              alert("Erro ao realizar check-out: " + error.message);
          });
  }

  function menu() {
      window.location.href = "/reservas";
  }