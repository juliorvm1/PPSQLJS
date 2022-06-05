//console.log('hello world')
let users = [];
let editing = false;
let userIdu = null;

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/users", {
    method: "GET",
  });
  const data = await response.json();
  users = data;
  renderUser(users);
});

const userForm = document.querySelector("#userForm");
userForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = userForm["username"].value;
  const password = userForm["password"].value;
  const email = userForm["email"].value;

  if (!editing) {
    const response = await fetch("api/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    const data = await response.json();

    console.log(data);
    users.unshift(data);
    console.log(users);
  } else {
    console.log("updating");
    const response = await fetch(`/api/users/${userIdu}`, {
      method: "PUT",
      headers:{
          "Content-Type":"application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });
    const updatedUser= await response.json();
    users=users.map(user => user.id === updatedUser.id ? updatedUser: user)    
    editing=false;
    userIdu=null;
  }

  renderUser(users);

  userForm.reset();
});

function renderUser(users) {
  const userList = document.querySelector("#userList");
  userList.innerHTML = "";

  users.forEach((user) => {
    const userItem = document.createElement("li");
    userItem.classList = "list-group-item list-group-item-dark my-2";
    userItem.innerHTML = `
          <header class="d-flex justify-content-between align-items-center">
            <h3>${user.username}</h3>
            <div>
              <button class="btn-delete btn btn-danger btn-sm">delete</button>
              <button class="btn-edit btn btn-secondary btn-sm">edit</button>
            </div>
          </header>
            <p>${user.email}</p>
            <p class="text-truncate">${user.password}</p>
            `;
    //console.log(userItem)
    const btnDelete = userItem.querySelector(".btn-delete");
    btnDelete.addEventListener("click", async () => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: "DELETE",
      });
      const data = await response.json();
      console.log(data);
      //console.log(data)
      //console.log(users)
      users = users.filter((user) => user.id !== data.id);
      //console.log(users)
      renderUser(users);
    });

    const btnEdit = userItem.querySelector(".btn-edit");
    btnEdit.addEventListener("click", async () => {
      const response = await fetch(`/api/users/${user.id}`, {
        method: "GET",
      });
      const data = await response.json();
      username = userForm["username"].value = data.username;
      //password = userForm["password"].value=data.userpa;
      email = userForm["email"].value = data.email;
      editing = true;
      userIdu = data.id;
    });

    userList.append(userItem);
  });
}
