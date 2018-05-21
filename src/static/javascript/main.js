{


  document.querySelector("#thread-content").onkeyup = function(e) {
    // if (e.which == 77) {
    //   alert("M key was pressed");
    // } else if (e.ctrlKey && e.which == 66) {
    //   alert("Ctrl + B shortcut combination was pressed");
    // } else if (e.ctrlKey && e.altKey && e.which == 89) {
    //   alert("Ctrl + Alt + Y shortcut combination was pressed");
    if ((e.shiftKey && e.which == 220) || e.which == 27) {
      let link = document.querySelector("#url").innerHTML;
      console.log(link);
      var tref = document.querySelector(
        `[href="${link.trim()}"]`
        // "[href='{% url 'threads:detail' slug=obj.slug %}']"
      );
      console.log(`[href="${link.trim()}"]`);
      console.log(tref.focus());
    }
  };

  function getMoreUserInfo(object, event) {
    var threadContent = document.querySelector("#thread-content");
    var mainContent = document.querySelector("#main-content");
    console.log(event);

    object.classList.toggle("show-caret");
    if (document.querySelectorAll(".show-caret").length > 1) {
      for (obj of document.querySelectorAll(".show-caret"))
        if (obj != object) {
          console.log(obj);
          obj.classList.remove("show-caret");
        }
    }
    var links = document.querySelectorAll(".show-thread-detail");
    for (link of links) {
      link.classList.toggle("thread-detail-grid");
    }

    if (document.querySelector(".show-caret")) {
      mainContent.style.setProperty("grid-column", "2/4 ");
      threadContent.style.setProperty("grid-column", "4/ span 5 ");
      threadContent.style.setProperty("width", "100% ");
      threadContent.style.setProperty("display", "flex ");
      threadContent.focus();
      // threadContent.style.setProperty("opacity", 0);
    } else {
      mainContent.style.removeProperty("grid-column");
      // threadContent.style.removeProperty("0");
      threadContent.style.setProperty("opacity", 1);

      threadContent.style.removeProperty("display");
    }

    //https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django
    // The websocket protocol comes in secure & secure flavors, we need to choose the correct one
  var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
  // // Shim for routers that time-out, ensures that socket automatically reconnects. source: https://github.com/heroku-examples/python-websockets-chat
  // var chat_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    if (window.fetch) {
      console.log(object.target);
      fetch(object.href, {
        credentials: 'include'
      }).then(function(data) {
        console.log(data);
        var dummyDiv = document.querySelector("#thread-content");
        data.text().then(function(text) {
          dummyDiv.innerHTML = text;
        });
      });
    }
    event.preventDefault ? event.preventDefault() : (event.returnValue = false);



  }
}
