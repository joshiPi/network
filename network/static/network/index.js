document.addEventListener('DOMContentLoaded', () => {

    // document.querySelector("#all_post").addEventListener('click', () => {
    //     document.addEventListener('DOMContentLoaded', () => {

    //         document.querySelector("#all_post").style.background = "grey";

    //     })
    // })
    const like = document.querySelectorAll("#like_button")
    like.forEach(element => {
        element.addEventListener('click', () => {
            //console.log('like')
            const id = parseInt(element.parentElement.previousElementSibling.innerHTML);
            fetch(`/like_unlike/${id}`)
                .then(response => response.json())
                .then(result => {
                    //console.log(result)
                    if (result["error"] == "not found.") {
                        window.alert("login to like post")
                    }
                    if (result["done"] == "increase") {
                        element.innerHTML = `<i class='fas fa-heart' style='font-size:20px;color:red'></i>${result["like_count"]}`
                    }
                    if (result["done"] == "decrease") {
                        element.innerHTML = `<i class='fas fa-heart' style='font-size:20px;color:lightgrey'></i>${result["like_count"]}`
                    }
                })
            //then(console.log("sucess"))

        })
    })

    const edit = document.querySelectorAll("#edit")
    edit.forEach(element => {
        element.addEventListener('click', () => editBlog(element))
    })

    //if event listners to null are defined in index.js so declare them at last so it won't mess with anyother functions declared before it.
    // document.querySelector("#follow").addEventListener('click', () => follow_unfollow("follow"))
    // document.querySelector("#unfollow").addEventListener('click', () => follow_unfollow("unfollow"))


})

function follow_unfollow(query) {
    const a = document.querySelector("#user_name").innerText;
    fetch(`../follow_unfollow/${query}/${a}`)
        .then(response => response.json())
        .then(result => {
            if (result["message"] == "you unfollowed this user") {
                const a = parseInt((document.querySelector("#followed_count").innerText).split(":",)[1])
                const c = a - 1;
                document.querySelector("#followed_count").innerHTML = `<strong>following</strong>: ${c} users`

            }
            if (result["message"] == "you are now following this user") {
                const a = parseInt((document.querySelector("#followed_count").innerText).split(":",)[1])
                const c = a + 1;
                document.querySelector("#followed_count").innerHTML = `<strong>following</strong>: ${c} users`

            }
            console.log(result["message"])
            document.querySelector("#message").innerHTML =
                `<div class="alert alert-info alert-dismissible fade in">
        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
        ${result["message"]}
    </div>`
        })
}

function editBlog(element) {
    const b = element.parentElement
    const id = b.children[4].innerText
    const user = b.children[0].innerText.split(" ")[1]
    fetch(`../edit/${user}/${id}`)
        .then(response => response.json())
        .then(result => {
            if (result["message"] == "ok") {
                const content = b.children[3].innerText;
                const new_div = `<form id="update">
                    <textarea  id="updated_content" style="width:100%"> ${content} </textarea>
                    <input class="btn btn-primary" type="submit" value="update">
                    </form>`
                b.children[3].innerHTML = new_div
                const update = document.querySelector("#update")
                update.addEventListener('submit', (event) => {
                    const updated_content = document.querySelector("#updated_content").value
                    fetch(`../edit/${user}/${id}`, {
                        method: 'POST',
                        body: JSON.stringify({
                            content: updated_content
                        })
                    })
                        .then(response => response.json())
                        .then(result => {
                            if (result["message"] == "successfully updated") {
                                b.children[3].innerText = updated_content;
                            }
                            if (result["message"] == "not_updated") {
                                b.children[3].innerText = content;
                            }
                        });
                    event.preventDefault();
                })
                //new_div.children[1].addEventListener('click', () => { console.log("upadate") })

            }
            if (result["message"] == "not_ok") {
                //document.querySelector("#main_message").innerText = "you can not update someoneelse Post"
                window.alert("you can not edit someone else post")
            }
        })
}