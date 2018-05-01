function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function voteUp(x, id) {
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    let link = '/answers/' + id + '/voteup/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then( response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().next().show().html('<i class="icon icon-caret-up"></i> ' + data.count);
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));
}

function voteDown(x, id) {
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    let link = '/answers/' + id + '/votedown/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().prev().show().html('<i class="icon icon-caret-up"></i> ' + data.count);
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));
}

function collect(x, id) {
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    let link = '/answers/' + id + '/collect/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then( response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().next().show();
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));
}

function uncollect(x, id) {
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    let link = '/answers/' + id + '/uncollect/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().prev().show();
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));
}

function followAsk(x, id) {
    let link = '/asks/' + id + '/follow/';
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then( response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().next().show();
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));
}

function unfollowAsk(x, id) {
    let link = '/asks/' + id + '/unfollow/';
    let headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then( response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(data => {
        if (!data.r) {
            $(x).hide().prev().show();
        } else {
            alert('error！')
        }
    }).catch(e => console.log(e));

}

function readmore(x, id) {
    let link = '/answers/' + id + '/content/';
    fetch(link, {
        method: 'GET',
        credentials: 'include'
    }).then(response => response.json()
    ).then(data => {
        if (!data.r) {
            $(x).siblings('span').hide();
            $(x).parent().html(data.content).append('<div class="answer-time">编辑于' + data.create_time + '</p>');
        } else {
            alert('error!')
        }
    });
}

function reply(x, answer_id, comment_id) {
    let replyEeditor = $('#replyEditor-' + answer_id);
    $('.reply-btn').show();
    $(x).hide().before(replyEeditor);
    replyEeditor.show().find("input[name='reply_id']").val(comment_id);
}

function cancelReply(x) {
    $(x).parent().hide();
    $('.reply-btn').show();
}

function showComments(x, id) {


    $('#commentList-' + id).show();
    $(x).hide().next().show();
    $('#comments-' + id).append('<i class="icon icon-spin icon-spinner-snake"></i> 加载中...');
    let link = `/comments/answer/${id}/`;
    fetch(link, {
        method: 'GET',
        credentials: 'include'
    }).then(response => {
        if (response.ok) {
            return response.text();
        } else {
            throw new Error('404!')
        }
    }).then(data => {
        $('#comments-' + id).empty();
        $('#comments-' + id).append(data);
    }).catch(e => console.log(e));

}

function hideComments(x, id) {
    $('#commentList-' + id).hide();
    $(x).hide().prev().show();
    $('#comments-' + id).empty();
}

function enter(x) {
    $(x).text('取消关注');
}

function leave(x) {
    $(x).text('  已关注');
}