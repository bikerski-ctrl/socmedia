function showMore() {
    var pageCur = Number(document.getElementById('page-current').value);
    var pageNum = Number(document.getElementById('page-number').value);
    pageCur += 1
    fetch("?page=" + pageCur, {
        headers: {
            'x-requested-with': 'XMLHttpRequest'
        }
    })
        .then(response => {
            console.log(response)
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text()
        })
        .then(data => {
            document.getElementsByClassName("post-container")[0].innerHTML += data
            document.getElementById('page-current').value = pageCur;
            if (pageCur == pageNum) {
                document.getElementById("show-more").style.display = "none";
            }
        })
        .catch(error => console.log('Error: ', error));
}