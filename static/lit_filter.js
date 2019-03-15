let papers = document.querySelectorAll('.book-entry');

let inp_title = document.getElementById('input_title');
let inp_author = document.getElementById('input_author');
let inp_year = document.getElementById('input_year');
let inp_journal = document.getElementById('input_journal');
let inp_tags = document.getElementById('input_tags');
let inp_synopsis = document.getElementById('input_synopsis');

const filter = () => {
    let q_title = inp_title.value.toLowerCase();
    let q_author = inp_author.value.toLowerCase();
    let q_year = inp_year.value.toLowerCase();
    let q_journal = inp_journal.value.toLowerCase();
    let q_tags = inp_tags.value.toLowerCase();
    let q_synopsis = inp_synopsis.value.toLowerCase();

    for(let paper of papers) {
        paper.style.display = "None";
        let matches_title = paper.children[0].textContent.toLowerCase().includes(q_title);
        let matches_author = paper.children[1].textContent.toLowerCase().includes(q_author);
        let matches_tags = paper.children[2].textContent.toLowerCase().includes(q_tags);
        let matches_year = paper.children[0].textContent.toLowerCase().includes(q_year);
        let matches_journal = paper.children[4].textContent.toLowerCase().includes(q_journal);
        let matches_synopsis = paper.children[5].textContent.toLowerCase().includes(q_synopsis);

        if (matches_title && matches_author && matches_year && matches_journal && matches_tags && matches_synopsis){
            paper.style.display = "";
        }
    }
}

inp_title.addEventListener('input', filter);
inp_author.addEventListener('input', filter);
inp_year.addEventListener('input', filter);
inp_journal.addEventListener('input', filter);
inp_tags.addEventListener('input', filter);
inp_synopsis.addEventListener('input', filter);
