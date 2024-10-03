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

    document.getElementById("novaReserva").addEventListener('click', function(){
 
    
        const buttons = document.getElementById("newButtonsContainer");
        buttons.style.display = "none";
       
        const formReserva = document.getElementById("formReserva");
        formReserva.style.display = "block";  
       
    });

    function newReservation(){
        const checkIn = document.getElementById("CheckIn").value;
        console.log(checkIn)
        const checkOut = document.getElementById("CheckOut").value;
        const quantity = document.getElementById("quantity").value;
        const animals = document.getElementById("animals").value;
        const balcony = document.getElementById("balcony").value;
        const hidromassagem = document.getElementById("Hidromassagem").value;

        if(checkIn && checkOut  && quantity && animals && balcony && hidromassagem){
            searchRoomsAvailable()
        } else {
            alert('Por favor, preencha as datas de check-in e check-out.');
        }
    }

    document.getElementById("novaReserva").addEventListener('click', function() {
        const buttons = document.getElementById("newButtonsContainer");
        buttons.style.display = "none";
        
        const formReserva = document.getElementById("formReserva");
        formReserva.style.display = "block";  
        
        // Adicionar event listeners para os inputs do formulário
        addFormListeners();
    });
    
    function addFormListeners() {
        const requiredFields = [
            document.getElementById("CheckIn"),
            document.getElementById("CheckOut"),
            document.getElementById("quantity"),
            document.getElementById("animals"),
            document.getElementById("balcony"),
            document.getElementById("Hidromassagem")
        ];
    
        requiredFields.forEach(field => {
            field.addEventListener('input', checkFormCompletion);
        });
    }
    
    function checkFormCompletion() {
        const checkInInput = document.getElementById("CheckIn");
        const checkOutInput = document.getElementById("CheckOut");
        const quantity = document.getElementById("quantity").value;
        const animals = document.getElementById("animals").value;
        const balcony = document.getElementById("balcony").value;
        const hidromassagem = document.getElementById("Hidromassagem").value;
    
        // Verifica se todos os campos obrigatórios estão preenchidos
        if (checkInInput.value && checkOutInput.value && quantity && animals && balcony && hidromassagem) {
            searchRoomsAvailable();
        }
    }
    

    
    function searchRoomsAvailable() {
        const formData = getFormData();
        console.log(formData);
        fetch(`/api/roomsAvailable?${formData}`)
            .then((response) => response.json())
            .then((data) => {
                updateRoomNumberDropdown(data);
            })
            .catch((error) => {
                console.error("Erro ao buscar os quartos:", error);
            });
    }
    
    function getFormData() {
        const checkIn = document.getElementById("CheckIn").value;
        const checkOut = document.getElementById("CheckOut").value;
        const quantity = document.getElementById("quantity").value;
        const animals = document.getElementById("animals").value;
        const balcony = document.getElementById("balcony").value;
        const hidromassagem = document.getElementById("Hidromassagem").value;
    
        return `checkIn=${checkIn}&checkOut=${checkOut}&quantity=${quantity}&animals=${animals}&balcony=${balcony}&hidromassagem=${hidromassagem}`;
    }

    function updateRoomNumberDropdown(data) {
        const roomDropdown = document.getElementById("roomNumberId");
        roomDropdown.innerHTML = '';  // Limpar a dropdown
    
        roomDropdown.disabled = false; // Tornar o select possível
    
        const button = document.getElementById("buttonReservar");
    
        button.disabled = false;

        // Preenche o dropdown com os quartos disponíveis
        data.forEach(room => {
            const option = document.createElement('option');
            option.value = room;
            option.text = `${room}`; 
            roomDropdown.appendChild(option);
        });
    } 


    function validarCheckIn() {
        const checkInInput = document.getElementById('CheckIn');
        const dataSelecionada = new Date(checkInInput.value);
        const dataAtual = new Date();
  
        // Define a data de hoje sem horas (apenas dia, mês, ano)
        dataAtual.setHours(0, 0, 0, 0);
  
        // Converte a data atual para o formato YYYY-MM-DD
        const ano = dataAtual.getFullYear();
        const mes = String(dataAtual.getMonth() + 1).padStart(2, '0'); // Adiciona zero à esquerda
        const dia = String(dataAtual.getDate()).padStart(2, '0'); // Adiciona zero à esquerda
        const dataFormatada = `${ano}-${mes}-${dia}`;
  
        if (dataSelecionada < dataAtual) {
          alert("A data escolhida não pode ser anterior a hoje!");
          
          // Ajusta o campo da data para o dia de hoje 
          checkInInput.value = dataFormatada;
        }
      }

      function validarCheckOut(){
        const checkInInput = document.getElementById('CheckIn');
        const checkOutInput = document.getElementById('CheckOut');
        const dataSelecionada = new Date(checkInInput.value);
        const dataCheckoutSelecionada = new Date(checkOutInput.value);
        const dataAtual = new Date();
  
        dataAtual.setHours(0, 0, 0, 0);
  
        const ano = dataAtual.getFullYear();
        const mes = String(dataAtual.getMonth() + 1).padStart(2, '0'); // Adiciona zero à esquerda
        const dia = String(dataAtual.getDate()).padStart(2, '0'); // Adiciona zero à esquerda
        const dataFormatada = `${ano}-${mes}-${dia}`;
  
        // Validar o Check-In
        if (dataSelecionada < dataAtual) {
          alert("A data de Check-In não pode ser anterior a hoje. A data será ajustada.");
          checkInInput.value = dataFormatada; // Ajusta Check-In para a data de hoje
        }
  
        // Validar o Check-Out
        if (dataCheckoutSelecionada < dataSelecionada) {
          alert("A data de Check-Out não pode ser anterior a Check-In. A data será ajustada para um dia após o Check-In.");
  
          // Ajusta o Check-Out para um dia após o Check-In
          dataSelecionada.setDate(dataSelecionada.getDate() + 1);
          const novoCheckOut = dataSelecionada.toISOString().split('T')[0]; // Formato YYYY-MM-DD
          checkOutInput.value = novoCheckOut; // Definir o novo valor de Check-Out
        }
      }

      function reservar(){

      }