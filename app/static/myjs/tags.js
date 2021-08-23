function displayTagDescription(){
    var tags= $('#tag_data').data("tags");
    var text = tags[$('#select_tag').val()];
    $('#textArea_tag').val( text);
}