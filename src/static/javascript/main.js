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
        credentials: "include"
      }).then(function(data) {
        console.log(data);
        var dummyDiv = document.querySelector("#thread-content");
        data.text().then(function(text) {
          dummyDiv.innerHTML = text;
          var script = document.createElement("script");
          script.innerHTML = `
      
          console.log(document.querySelectorAll(".form-class")[1])
          var threadSocket = new WebSocket(
          'ws://' + window.location.host + '/ws/thread/${object.id}/');
          document.querySelectorAll(".form-class")[1].onsubmit = function (e) {
              e.preventDefault()
              console.log(e)
               threadSocket.send(JSON.stringify({
                      'content': document.querySelectorAll("textarea")[1].value,
                      'id': document.getElementById('thread-id').innerHTML
                  }))
      
                 e.preventDefault()
             }
          console.log(threadSocket)
          threadSocket.onmessage = function(e) {
              var data = JSON.parse(e.data);
              var li = document.createElement('li')
              li.id = data.post_id
            
              var userContent = document.createElement('div')
              userContent.classList.add("user-content")
              var userLink = document.createElement('a')
              userLink.classList.add('user-preview')
              userLink.classList.add('preview-thread-content')
              userLink.href = '/'
              var userImage = document.createElement('div')
              userImage.classList.add('user-image-display')
              var thumbnailImage = document.createElement('div')
              thumbnailImage.classList.add('thumbnail-image')
              thumbnailImage.style.backgroundImage = "url(" + data.user.avatar + ")"
              var dot = document.createElement('span')
              userImage.appendChild(thumbnailImage)
              userImage.appendChild(dot)
      
              var nameDisplay = document.createElement('div')
              nameDisplay.classList.add('name-display')
              var fullName = document.createElement('div')
              var startedBy = document.createElement('span')
              startedBy.innerHTML = 'Started by '
              var userName = document.createElement('span')
              userName.classList.add('user-name')
              userName.innerHTML = data.user.username
              var onDate = document.createElement('span')
              onDate.innerHTML = ' ' + data.user.time
              fullName.appendChild(startedBy)
              fullName.appendChild(userName)
              fullName.appendChild(onDate)
              nameDisplay.appendChild(fullName)
              var userDesc = document.createElement("div")
              userDesc.classList.add('user-description')
              userDesc.innerHTML = data.user.description
              nameDisplay.appendChild(userDesc)

              userLink.appendChild(userImage)
              userLink.appendChild(nameDisplay)
              console.log(data)
              textContainer = document.createElement('div')
              textContainer.classList.add('text-container')
              textContainer.innerHTML = data.message
      
            
              userContent.appendChild(userLink)
              userContent.appendChild(textContainer)
              console.log(li)
                    
              li.appendChild(userContent)
              var ul = document.getElementById('thread-messages')
              ul.appendChild(li)
          };
      
      
     `;
          document.body.appendChild(script);
        });
      });
    }
    event.preventDefault ? event.preventDefault() : (event.returnValue = false);
  }
}
