let cmmNameForm = document.getElementById('cmm-name-form');
let cmmNameInput = cmmNameForm.querySelector('input[name=cmm-name]');

// listen for the submit event
cmmNameForm.addEventListener('submit', processCmmNameForm);
function processCmmNameForm(e) {
  e.preventDefault();

  // get our data
  const cmmName  = cmmNameInput.value;

  console.log(cmmName);

  // process the form!
  alert('Processing!');

}