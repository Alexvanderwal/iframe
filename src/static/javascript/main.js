{
    function getMoreUserInfo(object, event){
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

        if (window.fetch) {
            console.log(object.target)
            fetch(object.href).then(function (data) {
                console.log(data);
                var dummyDiv = document.querySelector("#thread-content");
                data.text().then(function (text) {
                    dummyDiv.innerHTML = text;
                })
            })
        }
         event.preventDefault ? event.preventDefault() :  (event.returnValue = false)
    }
}