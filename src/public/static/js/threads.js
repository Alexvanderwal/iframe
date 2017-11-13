
$(document).ready(function() {
    $('#post-btn').click(function (e) {
        e.preventDefault();

        location.href = "#";
        location.href = "#default-form";

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
    });


    $('.edit-post-btn').click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        var form = $('#default-form');
        var postUpdateUrl = this_.attr('data-href');
        $.ajax({
            url: postUpdateUrl,
            method: "GET",
            data: {},
            success: function (data) {
                $('.fr-view').html(data.content);
                $('.fr-wrapper').removeClass('show-placeholder');
                $(form).attr('action', 'update');
                $(form).attr('data-href', $(this_).attr('data-href'));
            }
        });
        location.href = "#";
        location.href = "#default-form";
    });

    $('#default-form').on('submit', function (e) {
        var this_ = $(this);
        if (this_.attr("action")) {
            e.preventDefault();
            console.log($(this_).attr('data-id'));
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.ajax({
                url: $(this_).attr('data-href'),
                method: "PUT",
                data:
                    {
                        'content': $('.fr-view').html(),
                        'X-CSRFToken': csrftoken,
                        'csrftoken': csrftoken
                    },
                success: function (data) {
                    console.log(data)
                },
                error: function (data) {
                    console.log(data);
                    console.log('{{ csrf_token }}');
                }
            });

        }
        else {
        }
    });

    $('.like-btn').click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        var likeUrl = this_.attr('data-href');
        var likeCount = parseInt(this_.attr('data-likes'));
        $.ajax({
            url: likeUrl,
            method: "GET",
            data: {},
            success: function (data) {
                var newLikes;
                var verb;
                if (data.liked) {
                    newLikes = likeCount + 1;
                    verb = 'Unlike'
                }
                else {
                    newLikes = likeCount - 1;
                    verb = 'Like'
                }
                updateText(this_, newLikes, verb)
            }, error: function (error) {
            }
        });

        function updateText(btn, newLikes, verb) {
            btn.text(newLikes + " " + verb);
            btn.attr('data-likes', newLikes);

        }
    });
});