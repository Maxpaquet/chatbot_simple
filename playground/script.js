// console.log("Hello from Node.js");
const readline = require('readline');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});


// ######################################################
// rl.question('Are you the boss? (yes/no) ', (answer) => {
//     if (answer.trim().toLowerCase() === 'yes' || answer.trim().toLowerCase() === 'y') {
//         rl.question('How old are you? ', (age) => {
//             console.log(age);
//             rl.close();
//         });
//     } else {
//         console.log('Access denied.');
//         rl.close();
//     }
// }
// );

// ######################################################
// rl.question('Are you the boss? (yes/no) ', function (answer) {
//     if (answer.trim().toLowerCase() === 'yes' || answer.trim().toLowerCase() === 'y') {
//         rl.question('How old are you? ', function (age) {
//             console.log(age);
//             rl.close();
//         });
//     } else {
//         console.log('Access denied.');
//         rl.close();
//     }
// });

// ######################################################
// let sum = 0;

// function ask(sum) {
//     if (sum >= 20) {
//         console.log('Sum: ' + sum);
//         rl.close();
//         return;
//     }
//     rl.question('Enter a number (empty or 0 to finish): ', (input) => {
//         const value = Number(input);
//         if (!input || !value) {
//             console.log('Sum: ' + sum);
//             rl.close();
//             return;
//         }
//         sum += value;
//         ask(sum);
//     });
// }

// ask(sum);

// ######################################################
// function sayHi(name) {   // (1) create
//     str_ = "Hello" + ' ' + name
//     console.log(str_);
//     return str_
// }

// let func = sayHi;    // (2) copy

// res = func("Max"); // Hello     // (3) run the copy (it works)!

// console.log("After fun called\n" + res)

// ######################################################

let user = {
  name: "John",
  age: 30
};

let key = prompt("What do you want to know about the user?", "name");

// access by variable
console.log( user[key] );