let games = document.querySelectorAll('.book-entry');
let inp_name = document.getElementById('input_name');
let inp_platform = document.getElementById('input_platform');
let inp_status = document.getElementById('input_status');
let inp_multiplayer = document.getElementById('input_multiplayer');

const trimmed = (s) => s.textContent.trim().toLowerCase();

const filter = () => {
    let q_name = inp_name.value.toLowerCase();
    let q_platform = inp_platform.value.toLowerCase();
    let q_status = inp_status.value.toLowerCase();
    let q_multiplayer = inp_multiplayer.value.toLowerCase();

    for(let game of games) {
        game.style.display = "None";
        let matches_title = trimmed(game.children[0]).includes(q_name);
        let matches_platform = trimmed(game.children[1]).includes(q_platform);
        let matches_status = trimmed(game.children[2]).startsWith(q_status);
        let matches_mp = trimmed(game.children[3]).includes(q_multiplayer);

        if (matches_title && matches_platform && matches_status && matches_mp) {
            game.style.display = "";
        }
    }
}

inp_name.addEventListener('input', filter);
inp_platform.addEventListener('input', filter);
inp_status.addEventListener('input', filter);
inp_multiplayer.addEventListener('input', filter);
