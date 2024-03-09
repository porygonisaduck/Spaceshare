// ***********************************************
// This file is for creating custom commands and
// overwriting existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//

// Create a cy.login() command which takes two arguments, `username` and `password`.
Cypress.Commands.add("login", (username, password) => {
  cy.request({
    method: "POST",
    url: "/accounts/",
    form: true,
    body: {
      username,
      password,
      operation: "login",
    },
  });
  Cypress.log({
    name: "login",
    message: `Submitted a request to login with username=${username} and password=${password}`,
  });
});
