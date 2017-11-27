jQuery.noConflict();
jQuery(document).ready(function() {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    jQuery('#post-btn').click(function (e) {
        e.preventDefault();
        $('.fr-view').html("");
        $('.fr-wrapper').addClass('show-placeholder');
        location.href = "#";
        location.href = "#default-form";
    });

    jQuery('.edit-post-btn').click(function (e) {
        e.preventDefault();

        var this_ = jQuery(this);
        var form = jQuery('#default-form');
        var postUpdateUrl = this_.attr('data-href');

        jQuery.ajax({
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

      jQuery('.delete-post-btn').click(function (e) {
        e.preventDefault();
        var this_ = $(this);
          var postUpdateUrl = this_.attr('data-href');
          $.ajaxSetup({
              beforeSend: function (xhr, settings) {
                  if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                      xhr.setRequestHeader("X-CSRFToken", csrftoken);
                  }
              }
          });

        jQuery.ajax({
            url: postUpdateUrl,
            method: "DELETE",
            data: {
                'X-CSRFToken': csrftoken,
                'csrftoken': csrftoken
            },
            success: function (data) {
                $(this_).closest('li').remove();
            },  error: function (data) {console.log(data)}
        });

    });

    jQuery('#default-form').on('submit', function (e) {
        var this_ = $(this);
        if (this_.attr("action") === 'update') {
            e.preventDefault();

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
                success: function (data) {},
                error: function (data) {}
            });
        }
        else {}
    });

    jQuery('.like-btn').click(function (e) {
        e.preventDefault();
        var this_ = $(this);
        var likeUrl = this_.attr('data-href');
        var likeCount = parseInt(this_.attr('data-likes'));
        jQuery.ajax({
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