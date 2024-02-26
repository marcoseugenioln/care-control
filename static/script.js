updateItems = function(){
    for (let index = 0; index < document.getElementsByClassName("update-item").length; index++) {
        document.getElementsByClassName("update-item")[index].submit();
    }
}