function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
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
    var headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    var link = '/answers/' + id + '/voteup/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(function (data) {
        if (!data.r) {
            $(x).hide().next().show().html('<i class="icon icon-caret-up"></i> ' + data.count);
        } else {
            alert('error！')
        }
    }).catch(function (e) {
        alert(e);
    });
}

function voteDown(x, id) {
    var headers = new Headers();
    headers.append('X-CSRFToken', getCookie('csrftoken'));
    var link = '/answers/' + id + '/votedown/';
    fetch(link, {
        headers: headers,
        method: 'POST',
        credentials: 'include'
    }).then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error(response)
        }
    }).then(function (data) {
        if (!data.r) {
            $(x).hide().prev().show().html('<i class="icon icon-caret-up"></i> ' + data.count);
        } else {
            alert('error！')
        }
    }).catch(function (e) {
        alert(e);
    });
}

function readmore(x, id) {
    var link = '/answers/' + id + '/content/';
    fetch(link, {
        method: 'GET',
        credentials: 'include'
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        if (!data.r) {
            $(x).siblings('span').hide();
            $(x).parent().html(data.content).append('<div class="answer-time">编辑于' + data.create_time + '</p>');
        } else {
            alert('error!')
        }
    });
}

function reply(x, answer_id, comment_id) {
    var replyEeditor = $('#replyEditor-' + answer_id);
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
}

function hideComments(x, id) {
    $('#commentList-' + id).hide();
    $(x).hide().prev().show();
}

function enter(x) {
    $(x).text('取消关注');
}

function leave(x) {
    $(x).text('  已关注');
}